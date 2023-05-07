from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from helper import helper
from .models import Category
from .serializers import CategorySerializer


# Create Category
# post
# /v1/category/create
class CreateCategory(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = CategorySerializer

    def create(self, request):
        helper.checkParams(request, ['name'])

        if Category.objects.filter(name=request.data['name']).count() > 0:
            raise helper.exception.NotAcceptable(
                helper.message.MODULE_EXISTS('Category'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Category'),
            CategorySerializer(Category.objects.all(), many=True).data
        )


# Read Category
# get
# /v1/catgory/read
class ReadCategory(ListAPIView):
    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('Categories'),
            CategorySerializer(Category.objects.all(), many=True).data
        )


# Update Category
# put
# /v1/category/update/<str:id>
class UpdateCategory(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.checkParams(request, ['name'])

        category = helper.checkRecord(id, Category, 'Category')
        category.name = request.data['name']
        category.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Category', 'updated'),
            CategorySerializer(Category.objects.all(), many=True).data
        )


# Delete Category
# delete
# /v1/category/delete
class DeleteCategory(DestroyAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def delete(self, request, id):
        category = helper.checkRecord(id, Category, 'Category')
        category.delete()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Category', 'deleted'),
            CategorySerializer(Category.objects.all(), many=True).data
        )
