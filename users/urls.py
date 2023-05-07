from django.urls import path
from .api import (
    Dashboard,
    UserProfile,
    DeactivateAccount,
    DownloadCombo,
    RecentCombos,
    DownloadedCombos
)


# URLS
urlpatterns = [
    path("dashboard", Dashboard.as_view()),
    path("profile", UserProfile.as_view()),
    path("deactivate", DeactivateAccount.as_view()),
    path("downloadCombo", DownloadCombo.as_view()),
    path("recentCombos", RecentCombos.as_view()),
    path("downloadedCombos", DownloadedCombos.as_view()),
]
