from django.db import models
import uuid
# Create your models here.
class UserModel(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=150)
    email=models.EmailField()
    password=models.CharField(max_length=40)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class PostModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    image=models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_liked = models.BooleanField(default=False)

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self)

class SessionToken(models.Model):
	user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
	session_token = models.CharField(max_length=255)
	#last_request_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	is_valid = models.BooleanField(default=True)

	def create_token(self):
		self.session_token = uuid.uuid4()

class LikeModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


