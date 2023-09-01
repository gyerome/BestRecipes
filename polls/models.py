from django.db import models
from django.utils.timezone import now
from .utils import calculate_time
from datetime import datetime


class UserSubscribes(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='+')
    subscriber = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.author.subscribers_quantity += 1
            self.author.rating += 5
            self.author.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.author.subscribers_quantity -= 1
        self.author.rating -= 5
        self.author.save()
        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class AbstractPost(models.Model):
    name = models.CharField(max_length=50)
    text_content = models.TextField()
    date = models.DateTimeField(default=now)
    date_timestamp = models.IntegerField(null=True, default=0)
    author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)#todo null false
    rating = models.IntegerField(default=0)
    isBlocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.author is None:
            raise ValueError()

        if self.date_timestamp == 0 or self.date_timestamp is None:
            self.date_timestamp = datetime.timestamp(self.date)*1000

        if self.id is not None:
            super().save(*args, **kwargs)
            return

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Recipe(AbstractPost):
    description = models.TextField()
    photo = models.ImageField(upload_to='images/recipes', blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.author.recipes_quantity += 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.author.recipes_quantity-=1
        self.author.save()
        super().delete(*args, **kwargs)

    def add_view(self):
        self.views += 1
        self.author.rating += 1
        self.save()
        self.author.save()



class Forum_theme(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Forum(AbstractPost):
    theme = models.ForeignKey(Forum_theme, on_delete=models.SET_NULL, null=True)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

class Comment(AbstractPost):
    forum = models.ForeignKey(Forum, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            Forum.objects.filter(id=self.forum.id).update(comments=models.F('comments')+1)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Forum.objects.filter(id=self.author.id).update(comments=models.F('comments')-1)
        print('deleted')
        super().delete(*args, **kwargs)


class Saved(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)