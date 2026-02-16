from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm
from .models import Post


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




   


