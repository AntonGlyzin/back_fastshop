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
    'minus_product': 'Уменьшить кол-во товара',
    'not_access': 'Доступ ограничен.',
    'not_user': 'Такого пользователя нет.',
    'auth': 'Авторизация',
    'login': 'Логин',
    'users': 'Пользователи',
    'incorrect_email_pass': 'Проблема авторизации: email или пароль не вернны.',
    'success_auth': 'Успешная авторизация',
    'api_401_desk': 'Неудачная авторизация',
    'auth_token_access': 'Авторизация для получеия токена доступа',
    'access_token': 'Токен доступа',
    'type_token': 'Тип токена'
}
                     
class Messages:
    def __init__(self, code=LANGUAGE_CODE):
        if code == 'ru':
            self.messages = MESSAGES_RUS
    def __getitem__(self, key):
        return self.messages.get(key)

MSG = Messages()