from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )

        if not created:
            return Response(
                {'detail': 'Post already liked.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )

        return Response({'detail': 'Post liked.'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response(
                {'detail': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        like.delete()
        return Response({'detail': 'Post unliked.'})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

# ✅ FEED VIEW
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followed_users = request.user.following.all()

        posts = Post.objects.filter(
            author__in=followed_users
        ).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    #"Post.objects.filter(author__in=following_users).order_by