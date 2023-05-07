from django.urls import path
from .api import (
    Dashboard,
    ReadUsers,
    SubscriptionHistory,
    GetUserToken,
    NetRevenue,
    ExtendExpiry,
    MinusExpiry,
    ExtendTodayDownload,
    ActivateUser,
    DeactivateUser,
    UpdateUserInfo,
    AddPlanToUser,

    LeakChecker
)


# URLS
urlpatterns = [
    path("dashboard", Dashboard.as_view()),
    path("read-users", ReadUsers.as_view()),
    path("subscription-history/<str:id>", SubscriptionHistory.as_view()),
    path('revenue/<str:filter>', NetRevenue.as_view()),
]

urlpatterns += [
    path('extend-expiry/<str:id>', ExtendExpiry.as_view()),
    path('minus-expiry/<str:id>', MinusExpiry.as_view()),
    path('extend-downloads/<str:id>', ExtendTodayDownload.as_view()),
    path('get-user-token/<str:username>', GetUserToken.as_view()),
    path('activate-user/<str:id>', ActivateUser.as_view()),
    path('deactivate-user/<str:id>', DeactivateUser.as_view()),
    path('update-user-info/<str:id>', UpdateUserInfo.as_view()),
    path('add-plan', AddPlanToUser.as_view()),
]

urlpatterns += [
    path("leak-checker", LeakChecker.as_view()),
]
