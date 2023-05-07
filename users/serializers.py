from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import DownloadedCombo, UserSubscriptions
from combo.models import Combo


# Downloaded Combo Serializer
class DownloadedComboSerializer(ModelSerializer):
    class Meta:
        model = DownloadedCombo
        exclude = ['user']
        depth = 1


# Downloaded Combo Serializer
class UserSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = UserSubscriptions
        exclude = ['user']
        depth = 1


class ReadDownloadedComboSerializer(ModelSerializer):
    comboName = SerializerMethodField('getComboName')
    comboLines = SerializerMethodField('getComboLines')
    categoryName = SerializerMethodField('getCategoryName')

    class Meta:
        model = DownloadedCombo
        fields = ['id', 'comboName', 'comboLines',
                  'categoryName', 'downlaoded']

    def getComboName(self, obj):
        return obj.combo.name

    def getComboLines(self, obj):
        return obj.combo.lines

    def getCategoryName(self, obj):
        return obj.combo.category.name


# Combo Serializers
class ReadComboSerializer(ModelSerializer):
    categoryName = SerializerMethodField('getCategoryName')
    isDownloaded = SerializerMethodField('getIsDownloaded')

    class Meta:
        model = Combo
        fields = ['id', 'name', 'categoryName',
                  'isDownloaded', 'lines', 'created', 'status']

    def getCategoryName(self, obj):
        return obj.category.name

    def getIsDownloaded(self, obj):
        user = self.context.user
        if DownloadedCombo.objects.filter(user=user, combo_id=obj.id).count() > 1:
            return True
        else:
            return False
