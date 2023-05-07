from re import L
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Q, Count
from .serializers import ReadUserSerializer, ReadSubscriptionHistorySerializer, ReadLeakUserSerializer
from helper import helper
from account.models import User
from subscription.models import Subscription
from users.models import UserSubscriptions
from combo.models import Combo
from invoice.models import Invoice


# Dashboard
# get
# /v1/admin/dashboard
class Dashboard(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('Profile'),
            {
                "totalCombos": Combo.objects.filter().count(),
                "totalComboLines": Combo.objects.aggregate(Sum('lines'))['lines__sum'],
                "totalUsers": User.objects.filter().count(),
                "activeUsers": User.objects.filter(isPaid=True).count(),
                "inactiveUsers": User.objects.filter(isPaid=False).count(),
                "totalRevenue": Invoice.objects.filter(status=True).aggregate(Sum('price'))['price__sum'],
                "totalSubscriptions": Invoice.objects.filter(status=True).count()
            }
        )


# Read Users
# get
# /v1/admin/read-users
class ReadUsers(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = helper.settings.PAGE_SIZE
        queryset = User.objects.filter(is_superuser=False)

        if "search" in request.GET:
            search = request.GET['search']
            queryset = User.objects.filter(Q(username__icontains=search) | Q(
                email__icontains=search), is_superuser=False)

        page_context = paginator.paginate_queryset(queryset, request)

        return paginator.get_paginated_response(
            ReadUserSerializer(page_context, many=True).data
        )


# Read Users Subscription Purchase History
# get
# /v1/admin/subscription-history/<str:id>
class SubscriptionHistory(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def list(self, request, id):
        user = helper.checkRecord(id, User, "User")
        return helper.createResponse(
            helper.message.MODULE_LIST('Subscriptions'),
            ReadSubscriptionHistorySerializer(
                UserSubscriptions.objects.filter(user=user), many=True).data
        )


# Extend Subscription Duration
# post
# /v1/admin/extend-expiry
class ExtendExpiry(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        helper.checkParams(request, ['days'])
        user = helper.checkRecord(id, User, "User")

        subscription = UserSubscriptions.objects.filter(
            user=user).order_by('-created')

        if subscription.count() == 0:
            raise helper.exception.NotAcceptable(
                helper.message.USER_ACC_NOT_HAVING_SUBCRIPTION
            )

        if subscription.count() > 0:
            subscription = subscription[0]
            subscription = UserSubscriptions.objects.get(id=subscription.id)

            subscription.expiry = subscription.expiry + \
                helper.timedelta(int(request.data['days']))
            subscription.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE(
                'User subscription', 'extended')
        )


# Minus Expiry
# post
# /v1/admin/minus-expiry
class MinusExpiry(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        helper.checkParams(request, ['days'])
        user = helper.checkRecord(id, User, "User")

        subscription = UserSubscriptions.objects.filter(
            user=user).order_by('-created')

        if subscription.count() == 0:
            raise helper.exception.NotAcceptable(
                helper.message.USER_ACC_NOT_HAVING_SUBCRIPTION
            )

        if subscription.count() > 0:
            subscription = subscription[0]
            subscription = UserSubscriptions.objects.get(id=subscription.id)

            subscription.expiry = subscription.expiry - \
                helper.timedelta(int(request.data['days']))
            subscription.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE(
                'User subscription', 'subtracted')
        )


# Extend Today Download
# post
# /v1/admin/extend-downloads
class ExtendTodayDownload(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        helper.checkParams(request, ['downloads'])

        user = helper.checkRecord(id, User, "User")
        user.todayDownloads -= int(request.data['downloads'])
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE(
                'User today downloads', 'extended')
        )


# Deactivate User
# post
# /v1/admin/deactivate/<str:id>
class DeactivateUser(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        user = helper.checkRecord(id, User, "User")
        user.is_active = False
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('User', 'deactivated')
        )


# Update Email & Password User
# post
# /v1/admin/deactivate/<str:id>
class UpdateUserInfo(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        helper.checkParams(request, ['email', 'password'])

        user = helper.checkRecord(id, User, "User")

        user.email = request.data['email']
        if request.data['password']:
            user.set_password(request.data['password'])
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('User', 'updated')
        )


# Activate User
# post
# /v1/admin/activate/<str:id>
class ActivateUser(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request, id):
        user = helper.checkRecord(id, User, "User")
        user.is_active = True
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('User', 'Activated')
        )


# Get user token
# get
# /v1/admin/get-user-token/<str:username>
class GetUserToken(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]
    http_method_names = ['get']

    def list(self, request, username):
        try:
            user = User.objects.get(username=username)
        except Exception:
            raise helper.exception.ParseError(
                helper.message.MODULE_NOT_FOUND('User'))

        return helper.createResponse(
            helper.message.MODULE_LIST('User'),
            {"token": helper.get_token(user)}
        )


# Add Plan to User
# post
# /v1/admin/add-plan
class AddPlanToUser(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request):
        helper.checkParams(request, ['userId', 'subscriptionId'])
        body = request.data

        # check if record exists
        user = helper.checkRecord(body['userId'], User, 'User')
        subscription = helper.checkRecord(
            body['subscriptionId'], Subscription, 'Subscription')

        # create invoice for user
        invoice = Invoice.objects.create(
            user=user,
            subscription=subscription,
            name=subscription.name,
            price=subscription.price,
            duration=subscription.duration,
            downloads=subscription.downloads,
            status=True,
        )
        invoice.save()

        # activating plan for user
        userSubscription = UserSubscriptions.objects.create(
            user=user,
            subscription=subscription,
            expiry=helper.timezone.now() + helper.timedelta(subscription.duration)
        )
        userSubscription.save()

        # mark user as paid
        user.isPaid = True
        user.todayDownloads = 0
        user.save()

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Subscription'),
        )


# Net Revenue
# get
# /v1/admin/revenue/<str:filter>
def getStats(date, differ=1):
    queryset = Invoice.objects.filter(
        created__lte=date, created__gte=date.date() - helper.timedelta(days=differ), status=True
    ).values('created__date').annotate(created=Count('created'), price=Sum('price'))

    if len(queryset) > 0:
        return queryset[0]['price']
    else:
        return 0


# get dates for year months
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m:
        m = 12
    d = min(date.day, [31,
                       29 if y % 4 == 0 and (
                           not y % 100 == 0 or y % 400 == 0) else 28,
                       31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
    return date.replace(day=d, month=m, year=y)


# for year
def getMonthStats(date, date2):
    queryset = Invoice.objects.filter(
        created__lte=date, created__gte=date2, status=True
    ).values('created__date').annotate(created=Count('created'), price=Sum('price'))

    if len(queryset) > 0:
        return queryset[0]['price']
    else:
        return 0


class NetRevenue(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def list(self, request, filter):
        label = []
        price = []
        if filter not in ["t", "w", "m", "y", "a"]:
            raise helper.exception.ParseError(
                helper.message.MODULE_NOT_FOUND("Filter"))

        if filter == "t":
            label = [helper.datetime.now().date(
            ) - helper.timedelta(days=1), helper.datetime.now().date()]
            price = [getStats(
                helper.datetime.now() - helper.timedelta(days=1)), getStats(
                helper.datetime.now())]

        elif filter == "w":
            for i in range(0, 7):
                label.append(helper.datetime.now().date() -
                             helper.timedelta(days=i))
                price.append(getStats(
                    helper.datetime.now() - helper.timedelta(days=i)
                ))

        elif filter == "m":
            for i in range(0, 30):
                label.append(helper.datetime.now().date() -
                             helper.timedelta(days=i))
                price.append(getStats(
                    helper.datetime.now() - helper.timedelta(days=i)
                ))
        elif filter == "y":
            for m in range(-12, 1):
                label.append(monthdelta(helper.datetime.now().date(), m))
                price.append(getMonthStats(monthdelta(helper.datetime.now(), m),
                                           monthdelta(helper.datetime.now(), m-1)))
        else:
            label.append('All Time'),
            queryset = Invoice.objects.filter(status=True).values('created__date').annotate(
                created=Count('created'), price=Sum('price'))
            if len(queryset) > 0:
                price.append(queryset[0]['price'])

        return helper.createResponse(
            helper.message.MODULE_LIST('Plans Revenue'),
            {
                "label": label,
                "price": price
            }
        )


# Leak checker
class LeakChecker(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def post(self, request):
        helper.checkParams(request, ['combo'])
        combo = (request.FILES['combo'].read()).decode('utf-8')

        users = User.objects.filter(is_superuser=False)

        usersData = ReadLeakUserSerializer(users, many=True).data

        suspect = {}

        for user in usersData:
            if user['fingerPrint'] in combo:
                suspect = user
                break

        return helper.createResponse(
            helper.message.MODULE_LIST('Suspect'),
            suspect
        )
