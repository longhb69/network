from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0) 

    def __str__(self):
        return self.content
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like,
        }

class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE,default=None, related_name="user_follow")
    following = models.ManyToManyField(User,null=True,blank=True, related_name="following")
    follower = models.ManyToManyField(User,null=True,blank=True, related_name="follower")

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=None, related_name="user_like")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, default=None, related_name="like_post")

    def __str__(self):
        return f"{self.user} liked {self.post}"

    
