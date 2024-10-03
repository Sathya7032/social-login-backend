from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email Address"), unique=True, max_length=255)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
    
    
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='programming_languages/', blank=True, null=True)
    url = models.CharField(max_length=200,unique=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=200,unique=True)
    likes = models.ManyToManyField(CustomUserModel, related_name='liked_blogs', blank=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title[:30]

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'
    

class TutorialPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_content = CKEditor5Field('Text', config_name='extends')
    post_file = models.CharField(max_length=200)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    post_video = models.URLField()
    url = models.CharField(max_length=200,unique=True)
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.post_title

class Comment_tutorials(models.Model):
    post = models.ForeignKey(TutorialPost, on_delete=models.CASCADE, related_name='comments_tutorials')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.post_title}'
    

class Topics(models.Model):
    topic = models.CharField(max_length=100)
    language = models.ForeignKey(ProgrammingLanguage,on_delete=models.CASCADE)
    url = models.CharField(max_length=200,unique=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

class CodeSnippet(models.Model):
    code_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    code = models.TextField()
    content = models.TextField()
    topic = models.ForeignKey(Topics,on_delete= models.CASCADE)
    url = models.CharField(max_length=200,unique=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Short(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    android_link = models.CharField(max_length=200,default=1)
    category = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class McqTopics(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='mcq_topics')
    url = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    topic = models.ForeignKey(McqTopics, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

class Option(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

        
        
class Latest_update(models.Model):
    update = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name