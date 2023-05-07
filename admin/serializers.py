from rest_framework.serializers import ModelSerializer, SerializerMethodField
from account.models import User
from users.models import UserSubscriptions
from helper import helper


# Read All Users
class ReadUserSerializer(ModelSerializer):
    isSubscription = SerializerMethodField('getSubscriptionStatus')
    plan_expiry = SerializerMethodField('getSubcriptionExpiry')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'isPaid',
            'todayDownloads',
            'is_verified',
            'is_active',
            'plan_expiry',
            'date_joined',
            'isSubscription'
        ]

    def getSubscriptionStatus(self, obj):
        susbcriptions = UserSubscriptions.objects.filter(
            user_id=obj.id, expiry__gte=helper.datetime.now())
        if susbcriptions.count() > 0:
            return True
        else:
            return False

    def getSubcriptionExpiry(self, obj):
        susbcriptions = UserSubscriptions.objects.filter(
            user_id=obj.id, expiry__gte=helper.datetime.now())
        if susbcriptions.count() > 0:
            return susbcriptions[0].expiry
        else:
            return None


# Read All Users
class ReadSubscriptionHistorySerializer(ModelSerializer):
    class Meta:
        model = UserSubscriptions
        exclude = ['user']
        depth = 1


# Leak User Serializer
class ReadLeakUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
