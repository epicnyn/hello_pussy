from rest_framework import serializers
from project_api.models import Article, Comment, Category, ArticleImages


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')
        # exclude =

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(
                instance=instance.children.all(), many=True
            ).data
        return representation


class ArticleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleImages
        exclude = ('id', )


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    images = ArticleImageSerializer(many=True, read_only=False)

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'owner', 'comments', 'category', 'preview', 'images')

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')
        # print("Файлы: ", request.FILES)
        images_data = request.FILES
        created_post = Article.objects.create(**validated_data)
        print(created_post)
        print("Work: ", images_data.getlist('images'))
        print("Is not work: ", images_data)
        # for image_data in images_data.getlist('images'):
        #     PostImages.objects.create(
        #         post=created_post, image=image_data
        #     )
        images_obj = [
            ArticleImages(post=created_post, image=image)
            for image in images_data.getlist('images')
        ]
        ArticleImages.objects.bulk_create(images_obj)
        return created_post


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')