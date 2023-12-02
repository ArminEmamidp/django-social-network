from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.text import slugify

from .models import Post, Like, Comment
from .forms import CommentForm, CommentReplyForm, PostCreateForm, PostUpdateForm


class PostsView(View):
    template_name = 'posts/posts.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search_text'):
            posts = posts.filter(title__contains=request.GET['search_text'])
        context = {
            'posts' : posts
        }
        return render(request, self.template_name, context=context)


class PostDetailView(View):
    template_name = 'posts/detail.html'
    form_class_1 = CommentForm
    form_class_2 = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = self.form_class_1()
        form2 = self.form_class_2()
        post = self.post_instance
        like = Like.objects.filter(post=post, user=request.user)
        comments = post.comments.filter(is_reply=False)

        if like.exists():
            can_like = False
        else:
            can_like = True
        context = {
            'post' : post,
            'can_like' : can_like,
            'comments' : comments,
            'form' : form,
            'form2' : form2
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class_1(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'You send a comment', 'success')
        return redirect(post.get_absolute_url())
    

class PostLikeView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = self.post_instance
        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            return redirect(post.get_absolute_url())
        else:
            Like.objects.create(user=request.user, post=post)
            messages.success(request, 'You liked the post', 'success')
            return redirect(post.get_absolute_url())


class PostDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.post_instance.user:
            return redirect('account:user_profile', self.post_instance.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = self.post_instance
        post.delete()
        messages.success(request, 'You deleted the post', 'success')
        return redirect('account:user_profile', request.user.username)


class AddReplyCommentView(View):
    form_class = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        self.comment_instance = get_object_or_404(Comment, id=kwargs['comment_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, **kwargs):
        post = self.post_instance
        comment = self.comment_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user 
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'You have replied to a comment', 'success')
        return redirect(post.get_absolute_url())


class PostCreateView(View):
    template_name = 'posts/create.html'
    form_class = PostCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context=context  )
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(cd['description'][:20])
            post.save()
            messages.success(request, 'You created a post', 'success')
            return redirect('account:user_profile', request.user.username)
        else:
            context = {
                'form' : form
            }
            return render(request, self.template_name, context=context)


class PostUpdateView(View):
    template_name = 'posts/update.html'
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.post_instance.user:
            return redirect('account:user_profile', self.post_instance.user.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        context = {
            'post' : post,
            'form' : form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)

        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(cd['description'][:20])
            post.save()
            messages.success(request, f'You updated the {post.title}', 'success')
            return redirect('account:user_profile', post.user.username)
        else:
            context = {
                'post' : post,
                'form' : form
            }
            return render(request, self.template_name, context=context)