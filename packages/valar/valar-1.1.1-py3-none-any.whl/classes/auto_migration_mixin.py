class AutoMigrationMixin:
    name = None  # 子类必须提供
    def auto_migrate(self):
        from django.core.management import call_command
        call_command('makemigrations', self.name, interactive=False, verbosity=0)
        call_command('migrate', self.name, interactive=False, verbosity=0)

