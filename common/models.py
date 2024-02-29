from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from synopex.models import Question, Answer, Comment
import secrets

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intro = models.CharField(max_length=300, blank=True, null=True, verbose_name="한줄소개")
    image = models.ImageField(upload_to="profile_images/")
    instagram_url = models.URLField(max_length=255, blank=True, null=True)
    twitter_url = models.URLField(max_length=255, blank=True, null=True)
    youtube_url = models.URLField(max_length=255, blank=True, null=True)
    personal_url = models.URLField(max_length=255, blank=True, null=True)

    def get_user_questions(self):
        return Question.objects.filter(author=self.user)

    def get_user_answers(self):
        return Answer.objects.filter(author=self.user)

    def get_user_comments(self):
        return Comment.objects.filter(author=self.user)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
    else:
        profile = instance.profile

    # profile.score = profile.calculate_score()
    profile.save()
