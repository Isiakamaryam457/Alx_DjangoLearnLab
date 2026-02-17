from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

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

    # Custom tags field (comma-separated)
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add tags separated by commas e.g. Django, Python, Tutorial',
        }),
        help_text='Enter tags separated by commas. New tags will be created automatically.'
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            # Pre-fill tags when editing a post
            existing_tags = self.instance.tags.all()
            self.fields['tags'].initial = ', '.join(
                tag.name for tag in existing_tags
            )

    def save(self, commit=True):
        """
        Override save to handle tag creation and association.
        """
        post = super().save(commit=False)

        if commit:
            post.save()

            # Handle tags
            tags_input = self.cleaned_data.get('tags', '')

            # Clear existing tags first
            post.tags.clear()

            if tags_input.strip():
                tag_names = [
                    tag.strip().lower()
                    for tag in tags_input.split(',')
                    if tag.strip()
                ]

                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

        return post
        

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