from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View

from .models import Relation, Story, Music
from .forms import UserLoginForm, UserRegisterForm, UserEditProfileForm, UserCreateStoryForm, UserCreateMusicForm


class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged-in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Username or Password is wrong', 'danger')
                return redirect('account:user_login')
        else:
            context = {
                    'form' : form
                }
            return render(request, self.template_name, context=context)


class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegisterForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'You registered successfully', 'success')
            return redirect('account:user_login')
        else:
            context = {
                'form' : form
            }
            return render(request, self.template_name, context=context)


class UserLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged-out successfully', 'success')
        return redirect('home:home')


class UserProfileView(View):
    template_name = 'account/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            is_following = True
        else:
            is_following = False
        context = {
            'user' : user,
            'is_following' : is_following
        }
        return render(request, self.template_name, context=context)


class UserPostsView(View):
    template_name = 'account/posts.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        posts = user.posts.all()
        if request.GET.get('search_text'):
            posts = posts.filter(title__contains=request.GET['search_text'])
        context = {
            'user' : user,
            'posts' : posts
        }
        return render(request, self.template_name, context=context)


class UserFollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user == self.user_instance:
            return redirect('account:user_profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            messages.error(request, f'You followed {user.username}', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f'You now followed {user.username}', 'success')
        return redirect('account:user_profile', user.username)


class UserUnfollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user == self.user_instance:
            return redirect('account:user_profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(request, f'You now unfollowed {user.username}', 'success')
        else:
            messages.success(request, f'You not followed {user.username}', 'danger')
        return redirect('account:user_profile', user.username)


class UserFollowersView(View):
    template_name = 'account/followers.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        followers = user.followers.all()
        context = {
            'user' : user,
            'followers' : followers
        }
        return render(request, self.template_name, context=context)


class UserFollowingsView(View):
    template_name = 'account/followings.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        followings = user.followings.all()
        context = {
            'user' : user,
            'followings' : followings
        }
        return render(request, self.template_name, context=context)


class UserDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.user_instance:
            return redirect('account:user_profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        user.delete()
        messages.success(request, 'You deleted yourself account', 'success')
        return redirect('home:home')


class UserEditProfileeView(View):
    template_name = 'account/edit-profile.html'
    form_class = UserEditProfileForm
    
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.user_instance:
            return redirect('account:user_profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        INITIAL = {'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name}
        form = self.form_class(instance=user.profile, initial=INITIAL)
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST, instance=user.profile)

        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user.email = cd['email']
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'You edited your profile', 'success')
            return redirect('account:user_profile', user.username)
        else:
            context = {
                'form' : form
            }
            return render(request, self.template_name, context=context)


class FindFriendsView(View):
    template_name = 'account/find-friends.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = User.objects.all()
        if request.GET.get('search_text'):
            users = users.filter(username__contains=request.GET['search_text'])
        context = {
            'users' : users
        }
        return render(request, self.template_name, context=context)


class UserCreateStoryView(View):
    template_name = 'account/create-story.html'
    form_class = UserCreateStoryForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, 'You created a story', 'success')
            return redirect('account:user_profile', request.user.username)


class UserStoriesView(View):
    template_name = 'account/stories.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        stories = user.stories.all()
        context = {
            'user' : user,
            'stories' : stories
        }
        return render(request, self.template_name, context=context)


class UserDeleteStoryView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        self.story_instance = get_object_or_404(Story, id=kwargs['story_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.story_instance.user:
            return redirect('account:user_profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        story = self.story_instance
        story.delete()
        messages.success(request, 'You deleted a story', 'success')
        return redirect('account:user_profile', request.user.username)


class UserCreateMusicView(View):
    template_name = 'account/create-music.html'
    form_class = UserCreateMusicForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            music = form.save(commit=False)
            music.user = request.user
            music.save()
            messages.success(request, 'You created a music', 'success')
            return redirect('account:user_profile', request.user.username)
        else:
            context = {
                'form' : form
            }
            return render(request, self.template_name, context=context)


class UserMusicsView(View):
    template_name = 'account/musics.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        musics = user.musics.all()
        context = {
            'user' : user,
            'musics' : musics
        }
        return render(request, self.template_name, context=context)

class UserDeleteMusicView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        self.music_instance = get_object_or_404(Music, id=kwargs['music_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.music_instance.user:
            return redirect('account:user_profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        music = self.music_instance
        music.delete()
        messages.success(request, 'You deleted a music', 'success')
        return redirect('account:user_profile', request.user.username)