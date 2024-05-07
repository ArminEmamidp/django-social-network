from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from .models import Comment, Like, Post
from .forms import PostCreateForm, CommentSendForm, PostSearchForm


page_urls = {
    'home' : 'base:home'
}

def home_view(request):
    return render(request, 'base/index.html')


class PostsView(View):
    template_name = 'posts/posts.html'
    form_class = PostSearchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        posts = Post.objects.all()
        form = self.form_class()

        if request.GET.get('search_text'):
            search_text = request.GET.get('search_text')
            posts = posts.filter(title__contains = search_text)

        return render(request, self.template_name, {
            'posts' : posts,
            'form' : form
        })


class PostDetailView(View):
    template_name = 'posts/detail.html'
    form_class = CommentSendForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['id'])
        like = Like.objects.filter(post=post, auther=request.user)
        if like.exists():
            can_like = False
        else:
            can_like = True
        comments = post.comments.all()
        form = self.form_class()

        return render(request, self.template_name, {
            'post' : post,
            'can_like' : can_like,
            'comments' : comments,
            'form' : form
        })

    def post(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['id'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Comment.objects.create(auther=request.user, post=post, body=cd['body']).save()
            messages.success(request, 'You posted a comment successfully!', 'success')
            return redirect(post.post_detail())
        else:
            return render(request, self.template_name, {
                'post' : post,
                'form' : form
            })


class PostCreateView(View):
    template_name = 'posts/create.html'
    form_class = PostCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
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
            Post.objects.create(auther=request.user, title=cd['title'], description=cd['description'], body=cd['body']).save()
            messages.success(request, 'You have created a post successfully!', 'success')
            return redirect('account:user_profile', request.user)
        else:
            return render(request, self.template_name, {
                'form' : form
            })


def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if not request.user.is_authenticated:
        return redirect(page_urls['home'])
    elif request.user != post.auther:
        messages.error(request, 'You can`t delete the post!', 'danger')
        return redirect(post.post_detail())
    else:
        post.delete()
        messages.success(request, 'You have deleted a post successfully!', 'success')
    return redirect('account:user_posts', request.user)


class PostLikeView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        like = Like.objects.filter(post=post, auther=request.user)

        if like.exists():
            messages.error(request, "You already liked this post", 'warning')
        else:
            Like.objects.create(auther=request.user, post=post).save()
            messages.success(request, f"You have liked this post successfully", 'success')
        return redirect(post.post_detail())


class PostUpdateView(View):
    template_name = 'posts/update.html'
    form_class = PostCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(page_urls['home'])
        if request.user != self.post_instance.auther:
            messages.error(request, 'You can`t update this post', 'danger')
            return redirect(self.post_instance.post_detail())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        INITIAL = {'title':post.title, 'description':post.description, 'body':post.body}
        form = self.form_class(initial=INITIAL)
        return render(request, self.template_name, {
            'form' : form
        })

    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post.title = cd['title']
            post.description = cd['description']
            post.body = cd['body']
            post.save()
            messages.success(request, "You have updated the post successfully", 'success')
            return redirect('account:user_posts', request.user)
        else:
            return render(request, self.template_name, {
                'form' : form
            })


def post_comment_delete(request, id, comment_id):
    post = get_object_or_404(Post, id=id)
    comment = post.comments.get(id=comment_id)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != post.auther: messages.error(request, 'You can`t delete the comment.', 'danger'); return redirect(post.post_detail())
    comment.delete(); messages.success(request, 'You have deleted a comment successfully', 'success'); return redirect(post.post_detail())
