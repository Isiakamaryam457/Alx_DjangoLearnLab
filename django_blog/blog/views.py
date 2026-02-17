from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag


def register(request):
    """
    Handle user registration.
    Uses CustomUserCreationForm to create new users with email field.
    """
    if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    """
    Display and handle user profile management.
    Requires user to be logged in (enforced by @login_required decorator).
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'blog/profile.html', context)

class PostListView(ListView):
        """
        Display all blog posts.
        """
        model = Post
        template_name = 'blog/post_list.html'
        context_object_name = 'posts'
        paginate_by = 5  # Show 5 posts per page

class PostDetailView(DetailView):
    """
    Display individual blog post.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new posts.
    LoginRequiredMixin ensures only logged-in users can access this view.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user before saving.
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their posts.
    LoginRequiredMixin: User must be logged in
    UserPassesTestMixin: User must be the author of the post
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user before saving.
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow authors to delete their posts.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # Redirect to post list after deletion
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """
        Add success message when post is deleted.
        """
        messages.success(self.request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)

# ==================== Comment CRUD Views ====================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to add comments to a blog post.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    
    def form_valid(self, form):
        """
        Set the post and author before saving.
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the post detail page after adding comment.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """
        Add the post to the context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow comment authors to edit their comments.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Ensure only the comment author can edit.
        """
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """
        Redirect to the post detail page after updating.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow comment authors to delete their comments.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """
        Ensure only the comment author can delete.
        """
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """
        Redirect to the post detail page after deleting.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been deleted!')
        return super().delete(request, *args, **kwargs)

class PostSearchView(ListView):
    """
    Search for posts based on title, content, or tags.
    """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)  # taggit uses same lookup
            ).distinct()
        
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PostByTagListView(ListView):
    """
    Display all posts associated with a specific tag.
    """
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs.get('tag_slug', '')
        return context