from django.shortcuts import render, redirect
from polls.models import UserSubscribes
from user.models import User
from django.http import HttpRequest, HttpResponse
from django.views.defaults import bad_request
from django.views.generic.edit import FormView
from .forms import NewForumForm, NewRecipeForm, NewCommentForm

def subscribe(request: HttpRequest):
    subscriber_id = request.POST.get('subscriber_id')
    author_id = request.POST.get('author_id')

    try:
        subscriber_id = int(subscriber_id)
        author_id = int(author_id)
        if subscriber_id == author_id:
            raise ValueError()

    except (TypeError, ValueError) as e:
        bad_request(request, e)

    author = User.objects.filter(id=author_id)[0]
    subscriber = User.objects.filter(id=subscriber_id)[0]

    try:
        subscribe = author.subscribes.through.objects.filter(author=author, subscriber=subscriber).get()

    except UserSubscribes.DoesNotExist as e:
        subscribe = author.subscribes.through.objects.create(author=author, subscriber=subscriber, _rating=0)

    else:
        subscribe.delete()

    return HttpResponse(status=200)


class NewPostView(FormView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] =self.request.user
        return kwargs

    def form_valid(self, form):
        forum = form.save()
        return super().form_valid(form)


class NewForumView(NewPostView):
    form_class = NewForumForm
    template_name = 'makeForum.html'
    success_url = '/forum'

class NewRecipeView(NewPostView):
    form_class = NewRecipeForm
    template_name = 'newRecipe.html'
    success_url = '/admin'

class NewCommentView(NewPostView):
    form_class = NewCommentForm
    template_name = 'newComment.html'
    success_url = '/admin'
