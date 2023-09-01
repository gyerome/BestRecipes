from django import forms
from polls.models import Forum_theme, Forum, Recipe, Comment, Category
from user.models import User


class AbstractNewPostForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'auth-field', 'placeholder':'Название'}
    ))
    text_content = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'text_content', 'placeholder':'Текст', 'class':'auth-field'}
    ))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = User.objects.filter(can_post=True, id=user.id)[0]

    def save(self, *args, **kwargs):
        self.instance.author = self.author
        return super().save(*args, **kwargs)

class NewForumForm(AbstractNewPostForm):
    theme = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'auth-field', 'required':'true'}),
                                   queryset=Forum_theme.objects.all(),
                                   empty_label='Выберите тему')

    class Meta:
        model = Forum
        fields = ('name', 'text_content', 'theme')


class NewRecipeForm(AbstractNewPostForm):
    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'auth-field', 'required':'true'}),
                                      queryset=Category.objects.all(),
                                      empty_label='Выберите категорию')

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'text_content', 'category', 'photo')


class NewCommentForm(AbstractNewPostForm):
    name = None
    class Meta:
        model = Comment
        fields = ('text_content', )

    def save(self, *args, **kwargs):
        self.instance.name = 'CommentName'
        #todo убрать заглушку
        self.instance.forum = Forum.objects.get(id=1)
        return super().save(*args, **kwargs)


