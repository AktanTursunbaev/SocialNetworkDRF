from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import UserCreateSerializer, PostSerializer
from .models import Post, PostLike, User
from .permissions import IsPostOwner, IsPostOwnerOrReadOnly


def analyze_likes(post_likes):
    data = {}
    for like in post_likes:
        if str(like.last_update) not in data.keys():
            data[str(like.last_update)] = 0
        data[str(like.last_update)] += 1
    return data


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserActivityView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs["pk"])
        data = {
            "last_login": user.last_login,
            "last_activity": user.last_activity,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise serializers.ValidationError
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    queryset = Post.objects.all()


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_instance = get_object_or_404(Post, pk=kwargs["pk"])
        like_instance, created = PostLike.objects.get_or_create(
            user=request.user, post=post_instance
        ).first()
        if request.data["is_liked"]:
            response = {"message": "Liked"}
            like_instance.is_liked = True
        else:
            response = {"message": "Unliked"}
            like_instance.is_liked = False
        like_instance.save()
        return JsonResponse(response)


class PostAnalyticsView(APIView):
    permission_classes = [IsPostOwner]

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs["pk"])
        self.check_object_permissions(request, post)
        query = Q(last_update__gte=request.query_params.get("date_from")) & Q(
            last_update__lte=request.query_params.get("date_to")
        )
        post_likes = (
            PostLike.objects.filter(post=post, is_liked=True)
            .filter(query)
            .order_by("last_update")
        )
        data = analyze_likes(post_likes)
        return Response(data=data, status=status.HTTP_200_OK)
