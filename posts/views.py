from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, LikeSerializer
from .models import Post, Like


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        posts = Post.objects.all()
        return posts

    def get_object(self):
        post = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, post)
        return post

    def create(self, request, *args, **kwargs):
        try:
            post = Post.objects.create(
                title=request.data.get("title"),
                body=request.data.get("body"),
                author=request.user,
            )
            post = PostSerializer(post)
            return Response(post.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(str(ex))
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(
            data=dict(posts=serializer.data, total=len(serializer.data)),
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        posts = self.get_object()
        user = request.user
        serializer = self.get_serializer(posts, data=request.data, partial="partial")
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        if request.user == post.author:
            post.delete()
            return Response(
                data={"message": "The post has been deleted"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"message": "You can not delete other user's post"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def retrieve(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        total_likes = Like.objects.filter(post__id=pk, action="like").count()
        total_unlikes = Like.objects.filter(post__id=pk, action="unlike").count()
        r = PostSerializer(post).data
        r["likes"] = total_likes
        r["unlikes"] = total_unlikes
        return Response(r)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        post_liked = Like.objects.filter(
            post__id=request.data.get("post"), user=request.user
        )
        if len(post_liked) > 0:
            return Response("You already liked/unliked this post before")
        try:
            post = Post.objects.filter(id=request.data.get("post")).first()
            if not post:
                return Response("This post doesn't exist")
            like = Like.objects.create(
                post=post,
                action=request.data.get("action"),
                user=request.user,
            )
            like = LikeSerializer(like)
            return Response(like.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
