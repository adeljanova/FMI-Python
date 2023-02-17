from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from notifications.models import Notification


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        verbose_name_plural = 'Categories'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_thread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    last_post_date = models.DateTimeField(auto_now=True)
    last_post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_post_thread')

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_post')

    def __str__(self):
        return self.body[:50] + '...'


class ForumNotification(Notification):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_notify')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_notify')

    class Meta:
        index_together = [
            ["thread", "post"],
        ]