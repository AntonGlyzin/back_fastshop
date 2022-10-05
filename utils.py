from firebase_admin import storage
from settings import CONFIG_EMAIL, BASE_DIR
import smtplib
import os
from messages import MSG
import uuid

class FireBaseStorage:
    @staticmethod
    def get_link_file(source: bytes, dist: str, type: str = None) -> str:
        bucket = storage.bucket()
        blob = bucket.blob(dist)
        blob.upload_from_string(source, content_type=type)
        blob.make_public()
        return blob.public_url


class EmailWorked:
    MAIL_SERVER = CONFIG_EMAIL['MAIL_SERVER']
    MAIL_PORT = CONFIG_EMAIL['MAIL_PORT']
    MAIL_FROM = CONFIG_EMAIL['MAIL_FROM']
    MAIL_PASSWORD = CONFIG_EMAIL['MAIL_PASSWORD']
    CONFIRM_REGISTRATION = 'users/confirm-registration'
    RESET_PASSWORD = 'users/reset-password'

    @classmethod
    def send_email(cls, to_mail, title_mail, body_mail):
        mail_lib = smtplib.SMTP_SSL(cls.MAIL_SERVER, cls.MAIL_PORT)
        mail_lib.login(cls.MAIL_FROM, cls.MAIL_PASSWORD)
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            cls.MAIL_FROM, to_mail, title_mail)
        msg += body_mail
        mail_lib.sendmail(cls.MAIL_FROM, to_mail, msg.encode('utf8'))
        mail_lib.quit()

    @classmethod
    def send_confirm_registration(cls, to_mail, key):
        txt = ''
        path = os.path.join(BASE_DIR, 'templates/email/confirm-registration.txt')
        with open(path, 'r', encoding='utf-8') as file:
            txt = file.read()
        txt = txt % (CONFIG_EMAIL['CALLBACK_SITE']+'/'+cls.CONFIRM_REGISTRATION+'?key='+key)
        cls.send_email(to_mail, MSG['confirm_registration'], txt)

    @classmethod
    def send_reset_password(cls, to_mail, key):
        txt = ''
        path = os.path.join(BASE_DIR, 'templates/email/reset-password.txt')
        with open(path, 'r', encoding='utf-8') as file:
            txt = file.read()
        txt = txt % (CONFIG_EMAIL['CALLBACK_SITE']+'/'+cls.RESET_PASSWORD+'?key='+key)
        cls.send_email(to_mail, MSG['confirm_reset_pass'], txt)

    @classmethod
    def send_password(cls, to_mail, password):
        txt = ''
        path = os.path.join(BASE_DIR, 'templates/email/send-password.txt')
        with open(path, 'r', encoding='utf-8') as file:
            txt = file.read()
        txt = txt % (password)
        cls.send_email(to_mail, MSG['confirm_reset_pass'], txt)

    @classmethod
    def confirm_change_password(cls, to_mail):
        txt = ''
        path = os.path.join(BASE_DIR, 'templates/email/confirm-change-password.txt')
        with open(path, 'r', encoding='utf-8') as file:
            txt = file.read()
        txt = txt % (CONFIG_EMAIL['CALLBACK_SITE'],)
        cls.send_email(to_mail, MSG['notify_change_pass'], txt)