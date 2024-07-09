import logging
import requests
import pathlib
import os.path

from googletrans import Translator
import argostranslate.package
import argostranslate.translate

from constants import TR_FOLDER


class Transliterator:
    def __init__(self):
        self.cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')

    # №1
    def get_tranlit(self, text):
        trantab = {k: v for k, v in zip(self.cyrillic, self.latin)}
        new_text = ''
        for ch in text:
            casefunc = str.capitalize if ch.isupper() else str.lower
            new_text += casefunc(trantab.get(ch.lower(), ch))
        return new_text


class Translate:
    def __init__(self):
        self.active = False
        self.online = False
        self.state_text = ''

        self.name_file_translate = "translate-ru_en-1_9.argosmodel"
        self.path_file_translate = os.path.join(TR_FOLDER, self.name_file_translate)
        self.package_path = pathlib.Path(self.path_file_translate)

        self.from_code = 'ru'
        self.to_code = 'en'

        self.google_translator = None
        self.offline_package = argostranslate.package
        self.offline_translate = argostranslate.translate
        # self.offline_package = None
        # self.offline_translate = None

        self._setup()

    def _setup(self):
        self._test_connect()
        if self.online:
            self._test_online()
        else:
            self._test_offline()

    def is_active(self):
        return self.active

    def is_online(self):
        return self.online

    def get_state(self):
        return self.state_text

    def _test_connect(self):
        try:
            requests.head("https://www.google.com/", timeout=1)
            self.online = True
        except requests.ConnectionError:
            logging.info(f"Translate online error: requests.ConnectionError [Нет соединения с интернетом]")
            self.state_text = 'Нет соединения с интернетом'
            self.online = False

    def _test_online(self):
        try:
            self.google_translator = Translator()
            self.google_translator.translate("тест")
            self.online = True
            self.active = True
            self.state_text = 'Перевод онлайн'
        except requests.ConnectionError:
            logging.info(f"Translate online error: ConnectionError [Нет соединения с онлайн переводчиком]")
            self.state_text = 'Нет соединения с онлайн переводчиком'
            self.online = False
        except Exception as e:
            logging.exception(f"Translate online error: {e}")
            self.state_text = 'Нет соединения с онлайн переводчиком'
            self.online = False

    def _test_offline(self):
        if os.path.exists(self.path_file_translate):
            try:
                self.offline_package.install_from_path(self.package_path)
                self.state_text = 'Перевод офлайн'
                self.active = True
            except Exception as e:
                logging.exception(f"Translate offline error: {e}")
                self.state_text = 'Ошибка распаковки файла перевода'
                self.active = False
        else:
            logging.info(f"Translate offline error: Файл для перевода не найден: {self.path_file_translate}")
            self.state_text = 'Файл для перевода не найден'
            self.active = False

    # def _test_offline(self):
    #     logging.info(f"Translate offline error: Файл для перевода не найден: {self.path_file_translate}")
    #     self.state_text = 'Офлайн перевод не доступен'
    #     self.active = False

    def translate(self, text):
        if self.online:
            translation = self.google_translator.translate(text)
            return translation.text
        else:
            translation = self.offline_translate.translate(text, self.from_code, self.to_code)
            return translation


if __name__ == '__main__':
    transliterator = Transliterator()
    print(transliterator.get_tranlit('Тестовый текст на русском'))
