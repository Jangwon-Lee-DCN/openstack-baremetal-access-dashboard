import django
from django.conf import settings


def pytest_configure():
    if not settings.configured:
        settings.configure(
            SECRET_KEY="test",
            USE_I18N=False,
            INSTALLED_APPS=[],
            TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}],
            DCN_BAREMETAL_ADMIN_PROJECT_ID="dcn-project",
            BAREMETAL_ACCESS_API_URL="http://access-api.test/",
        )
    django.setup()
