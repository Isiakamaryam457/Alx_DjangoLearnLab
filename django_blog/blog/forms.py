from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Includes title and content fields.
    Author is set automatically in the view.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }
        help_texts = {
            'title': 'Enter a descriptive title for your blog post (max 200 characters)',
            'content': 'Write the main content of your blog post',
        }

class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments on blog posts.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'maxlength': '1000'
            }),
        }
        labels = {
            'content': 'Comment',
        }
        help_texts = {
            'content': 'Share your thoughts (max 1000 characters)',
        }
    
    def clean_content(self):
        """
        Custom validation for comment content.
        Ensures comment is not empty or just whitespace.
        """
        content = self.cleaned_data.get('content')
        
        # Strip whitespace and check if empty
        if not content or not content.strip():
            raise forms.ValidationError('Comment cannot be empty.')
        
        # Check minimum length
        if len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        
        # Check maximum length
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        
        return content.strip()