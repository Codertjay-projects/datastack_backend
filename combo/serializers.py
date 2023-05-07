from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Combo
from users.models import DownloadedCombo


# Category Serializer
class ComboSerializer(ModelSerializer):
    class Meta:
        model = Combo
        fields = "__all__"


# Read Combo Serializer
class ReadComboSerializer(ModelSerializer):
    categoryName = SerializerMethodField('getCategoryName')
    isDownloaded = SerializerMethodField('getIsDownloaded')

    class Meta:
        model = Combo
        fields = ['id', 'name', 'category',
                  'categoryName', 'lines', 'isDownloaded', 'status', 'created']

    def getCategoryName(self, obj):
        return obj.category.name

    def getIsDownloaded(self, obj):
        user = self.context.user
        if DownloadedCombo.objects.filter(user=user, combo_id=obj.id).count() > 0:
            return True
        else:
            return False


# Read Comobo By Admin
class AdminComboSerializer(ModelSerializer):
    categoryName = SerializerMethodField('getCategoryName')

    class Meta:
        model = Combo
        fields = ['id', 'name', 'file', 'lines', 'category',
                  'categoryName', 'releaseDate', 'status', 'created']

    def getCategoryName(self, obj):
        return obj.category.name
