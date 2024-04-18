from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # tip : the ready function is for when you have signals file in your app
    # if you have signal in your model, and you do not have a separate file for it's not scenery to overwrite this
    def ready(self):
        import accounts.signals
