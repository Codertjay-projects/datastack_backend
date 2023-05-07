from django.contrib import admin as django_admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # path("admin_dashboard", django_admin.site.urls),
    path("v1/admin/", include("admin.urls")),
    path("v1/auth/", include("account.urls")),
    path("v1/category/", include("category.urls")),
    path("v1/combo/", include("combo.urls")),
    path("v1/subscription/", include("subscription.urls")),
    path("v1/user/", include("users.urls")),
    path("v1/announcement/", include("announcement.urls")),
    path("v1/faq/", include("faq.urls")),
    path("v1/maintenance/", include("maintenance.urls")),
    path("v1/invoice/", include("invoice.urls")),
    path("v1/privacy_policy/", include("privacy_policy.urls")),
    path("v1/tos/", include("tos.urls")),
    path("v1/webhook/", include("webhook.urls")),
    path("v1/social_media/", include("social_media.urls")),

    # # File serve
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
