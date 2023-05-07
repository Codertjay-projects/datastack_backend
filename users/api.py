from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from helper import helper
from .models import DownloadedCombo, UserSubscriptions
from combo.models import Combo
from account.models import User
from urllib.parse import urlparse
from django.db.models import Sum
from .serializers import (
    ReadDownloadedComboSerializer,
    ReadComboSerializer,
    UserSubscriptionSerializer
)


# Dashboard
# get
# /v1/user/dashboard
class Dashboard(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('Profile'),
            {
                "totalComboDownloaded": DownloadedCombo.objects.filter(user=request.user).count(),
                "totalCombos": Combo.objects.filter().count(),
                "totalComboLines": Combo.objects.aggregate(Sum('lines'))['lines__sum']
            }
        )


# Profile
# get
# /v1/user/profile
class UserProfile(ListAPIView):
    permission = [helper.permission.IsAuthenticated]

    def list(self, request):
        user = request.user

        subscription = UserSubscriptions.objects.filter(
            user=user, expiry__gte=helper.datetime.now()).order_by('-created')

        expiry = None
        isSubscription = False
        if len(subscription) > 0:
            subscription = UserSubscriptionSerializer(subscription[0]).data
            expiry = subscription['expiry']
            isSubscription = True
        else:
            subscription = {}

        return helper.createResponse(
            helper.message.MODULE_LIST('Profile'),
            {
                "username": user.username,
                "email": user.email,
                "expiry": expiry,
                "isSubscription": isSubscription,
                "todayDownloads": user.todayDownloads,
                "subscription": subscription,
                "is_verified": user.is_verified,
                "date_joined": user.date_joined,
                "totalComboDownloads": DownloadedCombo.objects.filter(user=user).count()
            }
        )


# Recent Combos
# get
# /v1/user/recentCombos
class RecentCombos(ListAPIView):
    permission = [helper.permission.IsAuthenticated]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('Recent combos'),
            ReadComboSerializer(Combo.objects.filter().order_by(
                '-created')[:10], context=request, many=True).data
        )


# Downloaded Combos
# get
# /v1/user/downloadedCombos
class DownloadedCombos(ListAPIView):
    permission = [helper.permission.IsAuthenticated]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('Downloaded combos'),
            ReadDownloadedComboSerializer(
                DownloadedCombo.objects.filter(user=request.user).order_by('-downlaoded')[:10], context=request, many=True).data
        )


# Deactivate Account
# post
# /v1/user/deactivate
class DeactivateAccount(CreateAPIView):
    permission = [helper.permission.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Account', 'deactivated')
        )


# Download Combo
# post
# /v1/user/downloadCombo
class DownloadCombo(CreateAPIView):
    permission = [helper.permission.IsAuthenticated]

    def post(self, request):
        helper.checkParams(request, ['combo'])
        body = request.data
        user = request.user

        # check today download limit
        if user.todayDownloads >= helper.comboDownloadLimit(user, UserSubscriptions):
            raise helper.exception.ParseError(
                helper.message.DOWNLOAD_LIMIT_EXCEED)

        # check if user account having a valid subscription
        isSubscription = False
        if UserSubscriptions.objects.filter(user=user, expiry__gte=helper.datetime.now()).count() > 0:
            isSubscription = True

        if not isSubscription:
            raise helper.exception.NotAcceptable(
                helper.message.USER_NOT_HAVING_SUBCRIPTION)

        # checking if combo exists
        combo = helper.checkRecord(body['combo'], Combo, "Combo")

        # reading combo file data
        path = combo.file.url

        file = open(str(helper.settings.BASE_DIR) +
                    path, 'r', encoding="ISO-8859-1")
        file_lines = file.readlines()
        file_length = len(file_lines)

        # preparing file for download
        prepareCombo = []
        prepareCombo = prepareCombo + file_lines[0:int(file_length/3)]
        prepareCombo = prepareCombo + [user.fingerPrint]
        prepareCombo = prepareCombo + \
            file_lines[int(file_length/3):file_length-1]

        prepareCombo = ''.join(prepareCombo)

        # updating download list
        if DownloadedCombo.objects.filter(combo=combo, user=user).count() == 0:
            downloads = DownloadedCombo.objects.create(
                combo=combo,
                category=combo.category,
                user=user
            )
            downloads.save()
            # updating today downloads
            user.todayDownloads += 1
            user.save()

        return helper.createResponse(
            helper.message.MODULE_LIST('Combo'),
            {"combo": prepareCombo}
        )
