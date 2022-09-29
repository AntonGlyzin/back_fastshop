from settings import LANGUAGE_CODE

SHOP_DESK = """
Список API для быстрого взаимодействия с магазином. 🚀

"""

MESSAGES_RUS = {
    'products': 'Товары',
    'desk_all_prod': 'Выводит список товаров по страницам.',
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
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
}
                     
class Messages:
    def __init__(self, code=LANGUAGE_CODE):
        if code == 'ru':
            self.messages = MESSAGES_RUS
    def __getitem__(self, key):
        return self.messages.get(key)

MSG = Messages()