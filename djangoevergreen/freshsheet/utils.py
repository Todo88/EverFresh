from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now

from quickbooks import QuickBooks, Oauth2SessionManager


def get_qb_client():
    from .models import User

    master_user = User.objects.get(qb_master_user=True)

    session_manager = Oauth2SessionManager(
        client_id=settings.QUICKBOOKS_CLIENT_ID,
        client_secret=settings.QUICKBOOKS_CLIENT_SECRET,
        access_token=master_user.qb_access_token,
        refresh_token=master_user.qb_refresh_token,
    )

    expire_time_with_buffer = (master_user.qb_expires_in or now()) - timedelta(seconds=60)
    if now() > expire_time_with_buffer:
        session_manager.refresh_access_tokens()
        master_user.qb_expires_in = now() + timedelta(seconds=session_manager.expires_in)

    session_manager.start_session()

    master_user.qb_access_token = session_manager.access_token
    master_user.qb_refresh_token = session_manager.refresh_token
    master_user.save()

    return QuickBooks(
        sandbox=True,
        session_manager=session_manager,
        consumer_key=settings.QUICKBOOKS_CLIENT_ID,
        consumer_secret=settings.QUICKBOOKS_CLIENT_SECRET,
        company_id=settings.QUICKBOOKS_COMPANY_ID,
    )
