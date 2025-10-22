from django.apps import AppConfig

class MembersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "members"
    verbose_name = "Members"

    def ready(self):
        # import signal handlers
        try:
            import members.signals  # noqa: F401
        except Exception:
            # avoid breaking manage.py commands if dependencies aren't available yet
            pass