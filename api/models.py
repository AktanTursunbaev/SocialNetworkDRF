from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_activity = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=1000, null=False, blank=False)
    publication_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post",
        verbose_name="User",
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="like",
        verbose_name="User",
        null=False,
        blank=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="like",
        verbose_name="Post",
        null=False,
        blank=False,
    )
    is_liked = models.BooleanField(default=False)
    last_update = models.DateField(auto_now=True)

    def __str__(self):
        return f"{str(self.post)} {str(self.user)}"
