from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Relation, Music, Image, Story, Link
from .forms import (UserRegisterForm, UserLoginForm, UserUpdateProfileForm, UserMusicCreateForm, UserImageCreateForm, 
                    UserSearchForm, UserStoryCreateForm, UserLinkCreateForm)


page_urls = {
    'home' : 'base:home',
    'register' : 'account:user_register',
    'login' : 'account:user_login'
}

class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            'form' : form
        })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'You have registered successfully!', 'success')
            return redirect(page_urls['login'])
        else:
            return render(request, self.template_name, {
                'form' : form
            })


class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            'form' : form
        })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'You have loged-in successfully!', 'success')
                return redirect(page_urls['home'])
            else:
                messages.error(request, 'Username or Password is wrong!', 'danger')
                return redirect(page_urls['login'])
        else:
            return render(request, self.template_name, {
                'form' : form
            })


def user_logout_view(request):
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    else:
        logout(request)
        messages.success(request, 'You have loged-out sccessfully!', 'success')
        return redirect(page_urls['home'])


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView, View):
    template_name = 'account/change_password.html'
    success_message = "You have changed the password successfully"
    success_url = reverse_lazy('account:user_password_change')


def user_settings_view(request, username):
    user = get_object_or_404(User, username=username)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != user:
        messages.error(request, 'You don`t have access to this section', 'danger')
        return redirect('account:user_profile', user)
    return render(request, 'account/settings.html', {'user' : user})


class UsersView(View):
    template_name = 'account/users.html'
    form_class = UserSearchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = User.objects.order_by('?')
        form = self.form_class()

        if request.GET.get('search_text'):
            search_text = request.GET.get('search_text')
            users = users.filter(username__contains=search_text)

        return render(request, self.template_name, {
            'users' : users,
            'form' : form
        })


class UserProfileView(View):
    template_name = 'account/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        links = user.links.all()
        stories = user.stories.all()
        posts = user.posts.all()
        musics = user.musics.all()
        images = user.images.all()

        if relation.exists():
            is_follow = True
        else:
            is_follow = False

        return render(request, self.template_name, {
            'user' : user,
            'links' : links,
            'stories' : stories,
            'posts' : posts,
            'musics' : musics,
            'images' : images,
            'is_follow' : is_follow
        })


class UserDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.user_instance:
            messages.error(request, 'You can`t delete this account!', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        user.delete()
        messages.success(request, 'Your account deleted successfully!', 'success')
        return redirect(page_urls['home'])


class UserUpdateProfileView(View):
    template_name = 'account/update.html'
    form_class = UserUpdateProfileForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user.pk != self.user_instance.pk:
            messages.error(request, 'You can`t update this profile', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        INITIAL = {'first_name':user.first_name, 'last_name':user.last_name,
                   'email':user.email}
        form = self.form_class(instance=user.profile, initial=INITIAL)

        return render(request, self.template_name, {
            'form' : form,
            'user' : user
        })

    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST, instance=user.profile)

        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            # user.username = cd['username']
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.save()
            messages.success(request, 'You have updated the profile successfully!', 'success')
            return redirect('account:user_profile', user.username)
        else:
            return render(request, self.template_name, {
                'form' : form
            })


class UserPostsView(View):
    template_name = 'account/posts.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        posts = user.posts.all()

        return render(request, self.template_name, {
            'user' : user,
            'posts' : posts
        })


class UserFollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user.pk == self.user_instance.pk:
            return redirect('account:user_profile', request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            messages.error(request, f"You already followed '{user}'", 'warning')
        else:
            Relation.objects.create(from_user=request.user, to_user=user).save()
            messages.success(request, f"You have followed '{user}'", 'success')
        return redirect('account:user_profile', user)


class UserUnfollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user.pk == self.user_instance.pk:
            return redirect('account:user_profile', request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(request, f"You have unfollowed '{user}'", 'success')
        else:
            messages.error(request, f"You have not followed '{user}'", 'warning')
        return redirect('account:user_profile', user)


def user_followers_view(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    user = get_object_or_404(User, username=kwargs['username'])
    followers = user.followers.all()

    return render(request, 'account/followers.html', {
        'user' : user,
        'followers' : followers
    })


def user_followings_view(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    user = get_object_or_404(User, username=kwargs['username'])
    followings = user.followings.all()

    return render(request, 'account/followings.html', {
        'user' : user,
        'followings' : followings
    })



class UserMusicCreateView(View):
    template_name = 'account/create-music.html'
    form_class = UserMusicCreateForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.user_instance:
            messages.error(request, 'You can not create music for this user', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class()

        return render(request, self.template_name, {
            'form' : form,
        })

    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            music = form.save(commit=False)
            music.auther = user
            music.save()
            messages.success(request, 'You have created a music successfully', 'success')
            return redirect('account:user_profile', request.user)
        else:
            return render(request, self.template_name, {
                'form' : form,
            })


def user_musics_view(request, username):
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    user = get_object_or_404(User, username=username)
    musics = user.musics.all()

    return render(request, 'account/musics.html', {
        'user' : user,
        'musics' : musics
    })


def user_music_delete_view(request, username, id):
    user = get_object_or_404(User, username=username)
    music = get_object_or_404(Music, id=id)
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    if request.user != user:
        messages.error(request, 'You can`t delete the music', 'danger')
    else:
        music.delete()
        messages.success(request, 'You have deleted a music successfully', 'success')
    return redirect('account:user_musics', user)


class UserImageCreateView(View):
    template_name = 'account/create-image.html'
    form_class = UserImageCreateForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.user_instance:
            messages.error(request, 'You can`t create image for this user', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class()

        return render(request, self.template_name, {
            'form' : form,
        })

    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            Image.objects.create(auther=user, image_file=cd['image_file'])
            messages.success(request, 'You have created a image successfully', 'success')
            return redirect('account:user_profile', request.user)
        return render(request, self.template_name, {
            'form' : form,
        })


def user_images_view(request, username):
    user = get_object_or_404(User, username=username)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    images = user.images.all()
    return render(request, 'account/images.html', {
        'images' : images
    })


def user_image_delete_view(request, username, id):
    user = get_object_or_404(User, username=username)
    image = get_object_or_404(Image, id=id)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != user: messages.error(request, 'You can`t delete the image', 'danger')
    else: image.delete(); messages.success(request, 'You have deleted a image successfully', 'success')
    return redirect('account:user_images', user)


class UserStoryCreateView(View):
    template_name = 'account/create-story.html'
    form_class = UserStoryCreateForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.user_instance:
            messages.error(request, 'You can`t create story for this user', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class()

        return render(request, self.template_name, {
            'user' : user,
            'form' : form 
        })

    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Story.objects.create(auther=user, content=cd['content'])
            messages.success(request, 'You have created a story successfully', 'success')
            return redirect('account:user_profile', user)
        else:
            return render(request, self.template_name, {
                'user' : user,
                'form' : form
            })


def user_stories_view(request, username):
    user = get_object_or_404(User, username=username)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    stories = user.stories.all()
    return render(request, 'account/stories.html', {
        'user' : user,
        'stories' : stories
    })


def user_story_delete_view(request, username, id):
    user = get_object_or_404(User, username=username)
    story = get_object_or_404(Story, id=id)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != user: messages.error(request, 'You can`t delete the story', 'danger')
    else: story.delete(); messages.success(request, 'You have deleted a story successfully', 'success')
    return redirect('account:user_stories', user)


class UserLinkCreateView(View):
    template_name = 'account/create-link.html'
    form_class = UserLinkCreateForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.user_instance:
            messages.error(request, 'You can`t create link for this user', 'danger')
            return redirect('account:user_profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Link.objects.create(user=user, title=cd['title'], url=cd['url']).save()
            messages.success(request, 'You have created a link successfully', 'success')
            return redirect('account:user_profile', user.username)
        else:
            return render(request, self.template_name, {'form':form})


def user_links_view(request, username):
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    user = get_object_or_404(User, username=username)
    links = user.links.all()
    return render(request, 'account/links.html', {'user':user, 'links':links})


def user_link_delete_view(request, username, id):
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    user = get_object_or_404(User, username=username)
    link = get_object_or_404(Link, user=user, id=id)
    link.delete()
    messages.success(request, 'You have deleted a link successfully', 'success')
    return redirect('account:user_profile', user.username)

