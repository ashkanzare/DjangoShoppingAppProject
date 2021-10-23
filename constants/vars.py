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
POSTAL_CODE_HELP_TEXT = 'کدپستی باید ۱۰ رقم و بدون خط تیره باشد'
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
POSTAL_ADDRESS = 'آدرس پستی'
RECEIVER_FIRST_NAME = 'نام گیرنده'
RECEIVER_LAST_NAME = 'نام خانوادگی گیرنده'
RECEIVER_PHONE = 'شماره گیرنده'
BUILDING_NUMBER = 'پلاک خانه'
BUILDING_UNIT = 'واحد'
CITY = 'شهر'
STATE = 'استان'
POSTAL_CODE = 'کد پستی'
STATUS = 'وضعیت'
NUMBER = 'تعداد'
ACTIVE = 'فعال'
SHIPPING_TYPE = 'نوع ارسال'
ORDER_STATUS = 'وضعیت سفارش'
DATE = 'تاریخ'
COIN = 'سکه'
PAYMENT_METHOD = 'نحوه ی پرداخت'
STAFF = 'کارمند'
""" Errors """
INVALID_USERNAME = 'نام کاربری در سیستم موجود است'
INVALID_PHONE = 'شماره تماس در سیستم موجود است'
INVALID_EMAIL = 'ایمیل در سیستم موجود است'
INVALID_FORM = 'لطفا مقادیر فیلد های فرم را به درستی پر کنید'
INVALID_PERSON_ID = 'شماره شناسنامه در سیستم موجود است'
INVALID_USERNAME_PASSWORD = 'نام کاربری یا رمز عبور اشتباه است'
INVALID_LEVEL = 'شما اجازه ی دسترسی به این سطح کاربری را ندارید'
INVALID_PASSWORD_MATCH = 'مقادیر رمز عبور و تایید آن باید باهم مطابقت داشته باشند'
INVALID_PERSONAL_ID = 'کد ملی وارد شده نادرست است'
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
INITIAL = 'INITIAL'
WAITING_FOR_PAY = 'WAITING_FOR_PAY'
PROCESSING = 'PROCESSING'
SENT = 'SENT'
DELIVERED = 'DELIVERED'
CANCELED = 'CANCELED'

ORDER_STATUS_CHOICES = [
    (INITIAL, 'INITIAL'),
    (WAITING_FOR_PAY, 'WAITING_FOR_PAY'),
    (PROCESSING, 'PROCESSING'),
    (SENT, 'SENT'),
    (DELIVERED, 'DELIVERED'),
    (CANCELED, 'CANCELED'),

]

ONLINE = 'ONLINE'
CASH_ON_DELIVERY = 'CASH_ON_DELIVERY'
MECOIN = 'MECOIN'

ORDER_PAYMENT_CHOICES = [
    (ONLINE, 'ONLINE'),
    (CASH_ON_DELIVERY, 'CASH_ON_DELIVERY'),
    (MECOIN, 'MECOIN'),
]

ORDER_PAYMENT_REVERSE = {
    'cash-on-delivery': CASH_ON_DELIVERY,
    'online-payment': ONLINE,
    'mecoin-payment': MECOIN,
}

ORDER_PAYMENT_PERSIAN_REVERSE = {
    CASH_ON_DELIVERY: 'پرداخت در محل (با کارت بانکی)',
    ONLINE: 'پرداخت آنلاین',
    MECOIN: 'پرداخت با میکوین',
}

SHIPPING_TYPE_CHOICES = [
    ('MESHOP', 'meshop'),
    ('POST', 'post'),
]

SHIPPING_TYPE_PERSIAN_REVERSE = {
    'MESHOP': 'ارسال توسط میشاپ',
    'POST': 'ارسال پستی',
}

CART_ACTIVE = 'active'
CART_SAVED = 'saved'

CART_STATUS = [
    ('active', 'active'),
    ('inactive', 'inactive'),
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

""" shipping prices """
MESHOP_SHIPPING = 30000
NORMAL_SHIPPING = 20000

SHIPPING_TYPE_TO_PRICE = {
    SHIPPING_TYPE_CHOICES[0][0]: MESHOP_SHIPPING,
    SHIPPING_TYPE_CHOICES[1][0]: NORMAL_SHIPPING
}

""" min price for free shipping """
FREE_SHIPPING_MIN_PRICE = 300000

""" MeCoin Unit per Toman """
MECOIN_PER_TOMAN = 10000
TOMAN_PER_MECOIN = 0.0001

PRODUCT_MECOIN_UNIT = 100

""" map default coordinate """
MAP_X = 51.33776109571264
MAP_Y = 35.70000461459449

""" Order Created Successfully sms generator"""


def order_sms(order):
    text = f""" میشاپ
{order['name']} عزیز
سفارشتان ثبت شد و درحال پردازش آن هستیم.
شما میتوانید وضعیت آن را از نشانی زیر پیگیری کنید:
شماره سفارش: {order['order']}
کد تحویل: {order['code']}
لینک پیگیری:{order['link']} """
    return text
