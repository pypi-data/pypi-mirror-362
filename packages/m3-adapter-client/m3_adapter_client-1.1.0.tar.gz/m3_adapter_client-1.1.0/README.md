# M3 UI клиента для взаимодействия со СМЭВ3 посредством Адаптера

## Подключение
settings:

    INSTALLED_APPS = [
        'adapter_client',
        'm3_adapter_client'
    ]


apps:

    from django.apps.config import AppConfig as AppConfigBase

    class AppConfig(AppConfigBase):

        name = __package__

        def ready(self):
            self._init_adapter_client()

        def _init_adapter_client(self):
            from adapter_client.config import ProductConfig, set_config

            set_config(ProductConfig())

app_meta:

    from django.conf.urls import url
    from m3_adapter_client import actions
    from .controllers import controller

    def register_actions():
        controller.extend_packs((
            actions.Pack(),
            actions.JournalPack(),
        ))

## Запуск тестов
    $ tox
