from django.conf import settings

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

    session_manager.start_session()
    session_manager.refresh_access_tokens()

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
