from django.db import models

class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog_images/')

class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='author_images/')
    description = models.TextField()

class Comment(models.Model):
    commenter_name = models.CharField(max_length=255)
    commenter_image = models.ImageField(upload_to='commenter_images/', null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='blog_covers/')
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    extra_images = models.ManyToManyField(BlogImage)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    comments = models.ManyToManyField(Comment)

