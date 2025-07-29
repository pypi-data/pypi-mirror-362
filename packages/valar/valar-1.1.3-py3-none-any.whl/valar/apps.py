import os
from django.apps import AppConfig

from .classes.auto_migration_mixin import AutoMigrationMixin
from .classes.auto_urlpatterns_mixin import AutoUrlPatternsMixin


class ValarConfig(AutoMigrationMixin,AutoUrlPatternsMixin,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'valar'
    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            getattr(super(), 'set_url', None)()
            getattr(super(), 'auto_migrate', None)()
            print('valar')





