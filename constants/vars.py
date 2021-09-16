"""
    vars.py is a python file that contain constants for using in project

"""

""" Variables """
USER = 'کاربر'
FIRST_NAME = NAME = 'نام'
LAST_NAME = 'نام خانوادگی'
AGE = 'سن'
EMAIL = 'ایمیل'
PHONE = 'شماره تلفن'
PERSONAL_ID = 'شماره شناسنامه'
USERNAME = 'نام کاربری'
PASSWORD = 'رمز عبور'
PHOTO = 'عکس'
ADDRESS = 'آدرس'
BIRTHDAY = 'تاریخ تولد'
ENTRY_DATE = 'تاریخ ورود'
STUDY_FIELD = 'رشته تحصیلی'
USERNAME_HELP_TEXT = 'حداکثر ۱۵۰ حرف و میتواند شامل حروف و اعداد و @/./+/-/_ باشد'
PHONE_HELP_TEXT = 'شماره تلفن خود را بدون صفر وارد کنید. مانند : ۹۱۲۱۲۳۴۵۶۷'
PHOTO_HELP_TEXT = 'انتخاب عکس اختیاری است'
REGISTER_DATE = 'تاریخ ثبت نام'
REGISTER_CONFIRM = 'تایید ثبت نام'
MAX_UNITS = 'حداکثر تعداد واحد'
USER_TYPE = 'سطح کاربر'
CUSTOMER = 'مشتری'
NO_NAME = 'بدون نام'
DISCOUNT_CODE = 'کد تخفیف'
END_DATE = 'تاریخ انقضا'
END_DATE_HELP_TEXT = 'تاریخ به طور خودکار تا یک ماه دیگر تنظیم شده است'
SEARCH_FOR_USER_HELP_TEXT = 'روی علامت جستجو کلیک کرده و مشتری را بر اساس شماره تلفن پیدا کنید'
PARENT = 'والد'
CATEGORY = 'دسته'
DESCRIPTION = 'توضیحات'
PROPERTY = 'ویژگی'
PRODUCT = 'محصول'
USER_AUTH_CODE = 'کد تاییدیه'
EXP_TIME = 'زمان انقضا'

""" Errors """
INVALID_USERNAME = 'نام کاربری در سیستم موجود است'
INVALID_PHONE = 'شماره تماس در سیستم موجود است'
INVALID_EMAIL = 'ایمیل در سیستم موجود است'
INVALID_FORM = 'لطفا مقادیر فیلد های فرم را به درستی پر کنید'
INVALID_PERSON_ID = 'شماره شناسنامه در سیستم موجود است'
INVALID_USERNAME_PASSWORD = 'نام کاربری یا رمز عبور اشتباه است'
INVALID_LEVEL = 'شما اجازه ی دسترسی به این سطح کاربری را ندارید'
INVALID_RENT_COUNT = 'شما نمیتوانید بیشتر از 5 کتاب امانت بگیرید'
RENT_REMAIN = 'تعداد انتخاب های باقیمانده ی شما: '
ERROR_TO_CODE = {
    "user with this phone already exists.": 0,
    PHONE_HELP_TEXT: 2
}
""" Register Confirmation """
REGISTER_SUCCESS = 'ثبت نام شما با موفقیت انجام شد'

""" DAYS NAME """
SATURDAY = 'شنبه', 'saturday'
SUNDAY = 'یک شنبه', 'sunday'
MONDAY = 'دو شنبه', 'monday'
THURSDAY = 'سه شنبه', 'thursday'
WEDNESDAY = 'چهارشنبه', 'wednesday'
TUESDAY = 'پنج شنبه', 'tuesday'

""" Choose user's type """
USER_TYPE_CHOICES = [
    ('manager', 'مدیر'),
    ('staff', 'کارمند'),
    ('customer', 'مشتری'),
]

USER_TYPE_REVERSE = {
    'مدیر': 'manager',
    'کارمند': 'staff',
    'مشتری': 'customer',
}
