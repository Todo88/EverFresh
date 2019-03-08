from datetime import timedelta, datetime

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
        sandbox=settings.IS_SANDBOX,
        session_manager=session_manager,
        consumer_key=settings.QUICKBOOKS_CLIENT_ID,
        consumer_secret=settings.QUICKBOOKS_CLIENT_SECRET,
        company_id=settings.QUICKBOOKS_COMPANY_ID,
        minorversion=4
    )


def get_next_service_date():
    # Current day of the week represented from Monday (0) to Sunday (6)
    # If Fri(4), Sat(5), Sun(6), Mon(0), we need to deliver on next available Tuesday(2)
    # If Tues(1), Weds(2), Thurs(3), service date next available Friday(4)
    current_date = datetime.today()
    current_weekday = current_date.weekday()

    if current_weekday == 0 or 4 or 5 or 6:
        # Returns datetime for next Tuesday
        return current_date + timedelta(days=(8 - current_weekday))
    elif current_weekday == 1 or 2 or 3:
        # Returns datetime for next Friday
        return current_date + timedelta(days=(11 - current_weekday))
