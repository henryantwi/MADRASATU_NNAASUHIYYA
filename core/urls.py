from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", include("dues.urls")),
    path("payments/", include("payments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
