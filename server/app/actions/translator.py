import os
import requests
from app.db import db
from app.models.setting import Setting
from config import Config
from app.log import log


class Translator:
    """Handler for the Yandex translation service."""

    """Translate terms"""
    @staticmethod
    def translate(terms, lang):
        url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
        data = {
            'folderId': Config.YA_FOLDERID,
            'texts': terms,
            'targetLanguageCode': lang
        }

        token = Translator.getToken()

        if token is None:
            log.error('Translator token is empty')
            return None

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Check requests count (prevent overuse)
        setting = db.session.query(Setting).filter(
            Setting.field == 'ya_tr').first()

        if int(setting.value) > 5000:
            log.error('Translator requests are exausted')
            return None

        setting.value = int(setting.value) + 1
        db.session.commit()
        db.session.close()

        r = requests.post(url, json=data, headers=headers)
        log.info(f'Translator: {terms}')

        items = r.json().get('translations')
        if not items:
            return None

        return [i['text'] for i in items]

    """Get access token (limited lifetime)"""
    @staticmethod
    def getToken():
        url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
        data = {
            'yandexPassportOauthToken': Config.YA_OAUTH
        }

        r = requests.post(url, json=data)

        return r.json().get('iamToken')
