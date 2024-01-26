from rest_framework import serializers
from .models import Author, Blog, BlogImage, Comment
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'commenter_name', 'commenter_image', 'description', 'date', 'replies')

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ('image',)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'image', 'description')

class BlogSerializer(serializers.ModelSerializer):
    blog_images = BlogImageSerializer(many=True, source='extra_images', required=False)
    author_name = serializers.CharField(source='author.name', required=False)
    author_image = serializers.ImageField(source='author.image', required=False)
    author_description = serializers.CharField(source='author.description', required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'cover_image', 'created_date', 'description',
                  'blog_images', 'author_name', 'author_image', 'author_description', 'comments')
