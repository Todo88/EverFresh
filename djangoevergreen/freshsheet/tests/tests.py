from freezegun import freeze_time
import datetime
import unittest
from utils import get_next_service_date


# class TestServiceDates(unittest.TestCase):
#     def test_service_date_works_all_week(self):
#         # Monday
#         self.assertEquals(get_next_service_date(0), datetime.datetime(2019, 4, 2))
#         print('Created on a Monday, Service Date is Tuesday')
#
#         # Tuesday
#         assert get_next_service_date(1) == datetime.datetime(2019, 4, 26)
#         print('Created on a Tuesday, Service Date is Friday')
#
#         # Wednesday
#         assert get_next_service_date(2) == datetime.datetime(2029, 11, 2)
#         print('Created on a Wednesday, Service Date is Friday')
#
#         # Thursday
#         assert get_next_service_date(3) == datetime.datetime(2019, 12, 13)
#         print('Created on a Thursday, Service Date is Friday')
#
#         # Friday
#         print(get_next_service_date(4))
#         assert get_next_service_date(4) == datetime.datetime(2021, 10, 19)
#         print('Created on a Friday, Service Date is Tuesday')
#
#         # Saturday
#         print(get_next_service_date(5))
#         assert get_next_service_date(5) == datetime.datetime(2029, 7, 17)
#         print('Created on a Saturday, Service Date is Tuesday')
#
#         # Sunday
#         print(get_next_service_date(6))
#         assert get_next_service_date(6) == datetime.datetime(2030, 10, 1)
#         print('Created on a Sunday, Service Date is Tuesday')
#
#
# if __name__ == "__main__":
#     unittest.main()

@freeze_time("2019-04-01", as_arg=True)
def test(frozen_time):
    # Monday
    assert get_next_service_date() == datetime.datetime(2019, 4, 2)
    print('Created on a Monday, Service Date is Tuesday')

    # Tuesday
    frozen_time.move_to("2019-04-23")
    assert get_next_service_date() == datetime.datetime(2019, 4, 26)
    print('Created on a Tuesday, Service Date is Friday')

    # Wednesday
    frozen_time.move_to("2029-10-31")
    assert get_next_service_date() == datetime.datetime(2029, 11, 2)
    print('Created on a Wednesday, Service Date is Friday')

    # Thursday
    frozen_time.move_to("2019-12-12")
    assert get_next_service_date() == datetime.datetime(2019, 12, 13)
    print('Created on a Thursday, Service Date is Friday')

    # Friday
    frozen_time.move_to("2021-10-15")
    assert get_next_service_date() == datetime.datetime(2021, 10, 19)
    print('Created on a Friday, Service Date is Tuesday')

    # Saturday
    frozen_time.move_to("2029-07-14")
    assert get_next_service_date() == datetime.datetime(2029, 7, 17)
    print('Created on a Saturday, Service Date is Tuesday')

    # Sunday
    frozen_time.move_to("2030-09-29")
    assert get_next_service_date() == datetime.datetime(2030, 10, 1)
    print('Created on a Sunday, Service Date is Tuesday')


test()

# 1. Setup circleci, you'll need a circle.yaml telling it to use Python and install
# your requirements, see chahub for example or compeittions v2
# 2. Setup pytest, pytest-django -- you'll need to make a pytest.ini. Put this in your root folder next
# to manage.py
# 3. Move this file into some folder and tell pytest.ini how to find it -- it will find it by default
# if you put it in /apps/some_django_app/tests/<here>
# 4. Check pytest docs for how to name test so it can find it

