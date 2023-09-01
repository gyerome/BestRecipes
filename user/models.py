from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from polls.models import Recipe


class User(AbstractUser):
    avatar = models.ImageField(default='images/users/ava1.jpg', upload_to='images/users')
    is_author = models.BooleanField(default=False)
    can_post = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)
    description = models.TextField(default='Этот пользователь не добавил описание.')
    subscribes = models.ManyToManyField('self', through='polls.UserSubscribes')

    subscribers_quantity = models.IntegerField(default=0)
    recipes_quantity = models.IntegerField(default=0)


    def get_views_quantity(self):
        return Recipe.objects\
            .filter(author=self)\
            .values('views')\
            .aggregate(views=models.Sum('views', default=0))\
            .get('views', 'hui')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        print(self.username)
        if self.username == '':
            raise ValueError('username is blank')
        super().save()
        img = Image.open(self.avatar.path)
        square_size = max(img.size)

        if img.size[0] == img.size[1]:
            return

        paste_box = []
        for side in img.size:
            if side == square_size:
                paste_box.append(0)
            else:
                paste_box.append(round((square_size-side)/2))


        background = Image.new('RGBA', (square_size, )*2, 5)
        background.paste(img, paste_box)
        background.save(self.avatar.path, 'png')


