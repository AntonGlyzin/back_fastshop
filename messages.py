from settings import LANGUAGE_CODE

SHOP_DESK = """
Список API для быстрого взаимодействия с магазином. 🚀

"""

MESSAGES_RUS = {
    'products': 'Товары',
    'product': 'Товар',
    'desk_all_prod': 'Выводит список товаров по страницам.',
    'desk_detail_prod': 'Выводит конкретный товаров.',
    'page': 'Страница',
    'limit_all_prod': 'Количество товаров на странице',
    'id': 'Идентификатор',
    'title': 'Заголовок',
    'desk': 'Описание',
    'price': 'Цена',
    'photo': 'Фото',
    'currency': 'Валюта',
    'quantity': 'Количество',
    'products_not_found': 'Нет товаров',
    'list_products': 'Список товаров',
    'shop_name': 'Магазин товаров',
    'shop_desk': SHOP_DESK,
    'desk_error': 'Описание ошибки',
    'api_desk_not_found': 'Ничего не найдено',
    'basket': 'Корзина',
    'add_product': 'Добавить в корзину',
    'delete_product': 'Убрать товар из корзины',
    'minus_product': 'Уменьшить кол-во товара в корзине',
    'not_access': 'Доступ ограничен.',
    'not_user': 'Такого пользователя нет.',
    'not_product': 'Такого товара не существует.',
    'auth': 'Авторизация',
    'login': 'Логин',
    'users': 'Пользователи',
    'incorrect_email_pass': 'Проблема авторизации: email или пароль не вернны.',
    'success_auth': 'Успешная авторизация',
    'api_401_desk': 'Неудачная авторизация',
    'auth_token_access': 'Авторизация для получеия токена доступа',
    'access_token': 'Токен доступа',
    'type_token': 'Тип токена',
    'sum': 'Сумма',
    'username': 'Username',
    'password': 'Пароль',
    'error_add_prod': 'Ошибка при добавление товара.',
    'desk_add_prod': 'Добавление товара в корзину.',
    'delete_product_basket': 'Товар удален из корзины.',
    'minimum_product_basket': 'Вы достигли минимального количества продуктов в корзине.',
    'product_delete_basket': 'Товар удален из корзины.',
    'minimum_product': 'Минимальное кол-во продукта.',
    'profile': 'Профиль',
    'first_name': 'Имя',
    'last_name': 'Фамилия',
    'photo': 'Фото',
    'email': 'E-mail',
    'set_photo_profile': 'Установить фото на профиль',
    'photo_profile': 'Фото профиля',
    'link_photo': 'Ссылка на фото',
    'no_auth': 'Пользователь не авторизован',
    'need_image': 'Файл должен быть изображением.',
    'error_size_photo': 'Размер файла превышает.',
    'inccorect_file': 'Файл не соответсвует нормам.',
    'not_search_user': 'Такой пользователь не найден.',
    'registration': 'Регистрация.',
    'success_regist': 'Успешная регистрация.',
    'not_eq_pass': 'Пароли не совподают.',
    'reapit_email': 'На этот email уже зарегистрированн аккаунт.',
    'reapit_username': 'Такой username уже существует.',
    'error_reg': 'Ошибка при регистрации'
}
                     
class Messages:
    def __init__(self, code=LANGUAGE_CODE):
        if code == 'ru':
            self.messages = MESSAGES_RUS
    def __getitem__(self, key):
        return self.messages.get(key)

MSG = Messages()