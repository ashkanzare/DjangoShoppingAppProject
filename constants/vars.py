"""
    vars.py is a python file that contain constants for using in project

"""
import webcolors

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
MANAGER = 'مدیر'
PRICE = 'قیمت'
DISCOUNT = 'تخفیف'
FACTOR_PROPERTY = 'ویژگی کلیدی'
VALUE = 'مقدار'
FACTOR_PROPERTY_VALUES = 'مقادیر ویژگی های کلیدی'
QUANTITY = 'موجودی'
PRICE_IMPACT = 'تاثیر بر قیمت'
QUANTITY_HELP_TEXT = 'در صورت صفر بودن تعداد محصول از طریق تعداد در ویژگی های کلیدی محاسبه میشود'
COLOR = 'رنگ'
COLOR_LINK = 'لینک به رنگ'
CART = 'سبد خرید'
AVENUE = 'کوچه'
STREET = 'خیابان'
BUILDING_NUMBER = 'پلاک خانه'
BUILDING_UNIT = 'واحد'
CITY = 'شهر'
STATE = 'استان'
POSTAL_CODE = 'کد پستی'
STATUS = 'وضعیت'
NUMBER = 'تعداد'
ACTIVE = 'فعال'
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
ADD_PRODUCT_ERROR = 'لطفا ویژگی انتخاب شده مربوط به محصول را درست انتخاب کنید'
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

ORDER_STATUS = [
    ('PENDING', 'pending'),
    ('SENT', 'sent'),
    ('CANCELED', 'canceled')
]

CART_STATUS = [
    ('active', 'active'),
    ('saved', 'saved')
]

""" States name """

STATES = {'آذربايجان شرقي': 0,
          'آذربايجان غربي': 1,
          'اردبيل': 2,
          'اصفهان': 3,
          'ايلام': 4,
          'بوشهر': 5,
          'تهران': 6,
          'چهارمحال وبختياری': 7,
          "خراسان جنوبي": 8,
          'خراسان رضوئ': 9,
          'خراسان شمالي': 10,
          'خوزستان': 11,
          'زنجان': 12,
          'سمنان': 13,
          'سيستان وبلوچستان': 14,
          'فارس': 15,
          'قزوين': 16,
          'قم': 17,
          'البرز': 18,
          'كردستان': 19,
          'كرمان': 20,
          'كرمانشاه': 21,
          'كهكيلويه و بويراحمد': 22,
          'گلستان': 23,
          'گيلان': 24,
          'لرستان': 25,
          'مازندران': 26,
          'مركزي': 27,
          'هرمزگان': 28,
          'همدان': 29,
          'یزد': 30}

STATES_TUPLE = [(v, k) for k, v in STATES.items()]

""" factor_property choices """

COLOR_CHOICES = [(v, k) for k, v in webcolors.HTML4_NAMES_TO_HEX.items()]

SIZES = [(k, k) for k in ['XS', 'S', 'L', 'XL', 'XXL', 'XXXL']]
