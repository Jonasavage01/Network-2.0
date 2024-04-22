from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PostForm
from .models import User, Post
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EditPostForm
from .models import User, Post, Follow
from django.utils import timezone
from datetime import datetime, timedelta



def index(request):
    # Fetch all posts from the database
    all_posts = Post.objects.all().order_by('-created_at')

    # Paginate the posts, displaying 10 per page
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'page_obj': page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Save the new post to the database
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            # Redirect the user back to the index page
            return redirect('index')

    else:
        form = PostForm()

    return render(request, 'network/new_post.html', {'form': form})

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch all posts, ordered by creation time
    return render(request, 'network/all_posts.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        # Redirect or display an error message indicating unauthorized access
        return redirect('error_page')

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect back to the index page after editing
    else:
        form = EditPostForm(instance=post)

    # Instead of rendering 'edit_post.html', render the 'index.html' with updated data
    all_posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'page_obj': page_obj, 'form': form})



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        return JsonResponse({'liked': True, 'message': 'You have already liked this post.'})
    else:
        post.likes.add(request.user)
        return JsonResponse({'liked': True, 'message': 'Post liked successfully.', 'action': 'like'})

@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse({'liked': False, 'message': 'Post unliked successfully.', 'action': 'unlike'})
    else:
        return JsonResponse({'liked': False, 'message': 'You have not liked this post yet.'})



@login_required
def user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    followers = set(follow.follower for follow in user.followers_relationships.all())
    following = set(follow.followed_user for follow in user.following_relationships.all())
    followers_count = len(followers)
    following_count = len(following)

    # Verificar si el usuario actual está siguiendo al usuario de la página
    is_following = False
    if request.user.is_authenticated:  # Asegurarse de que el usuario esté autenticado
        try:
            check_follow = request.user.following_relationships.filter(followed_user=user)
            if check_follow.exists():
                is_following = True
        except:
            pass

    return render(request, 'network/user_page.html', {
        'user': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'user_profile': user
    })


@login_required
def following_posts(request):
    user = request.user
    following_posts = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')

    # Get the list of followers and followed users
    followers = user.followers_relationships.all()
    following = user.following_relationships.all()

    # Calculate the number of followers and followed users
    followers_count = followers.count()
    following_count = following.count()

    return render(request, "network/following_posts.html", {
        'following_posts': following_posts,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count,
    })


@login_required
def profile(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')

    # Get the list of followers and followed users
    followers = user.followers_relationships.all()
    following = user.following_relationships.all()

    # Calculate the number of followers and followed users
    followers_count = followers.count()
    following_count = following.count()

    return render(request, "network/profile.html", {
        'user': user,
        'user_posts': user_posts,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

def follow(request):
    userfollow = request.POST.get('userfollow')
    try:
        userfollowData = get_object_or_404(User, pk=userfollow)
        currentUser = request.user
        f = Follow(follower=currentUser, followed_user=userfollowData)
        f.save()
        return HttpResponseRedirect(reverse('user_page', kwargs={'user_id': userfollow}))
    except User.DoesNotExist:
        # Manejar el caso en el que el usuario no existe
        return HttpResponse("El usuario no existe.")

def unfollow(request):
    userfollow_id = request.POST.get('userfollow')
    currentUser = request.user
    
    try:
        userfollowData = User.objects.get(pk=userfollow_id)
    except User.DoesNotExist:
        # Manejar el caso en el que el usuario no existe
        # Puedes mostrar un mensaje de error o realizar alguna acción específica
        return HttpResponse("El usuario que intentas dejar de seguir no existe.")
    
    # Filtrar todos los objetos Follow que coincidan con el usuario actual y el usuario seguido
    follow_objects = Follow.objects.filter(follower=currentUser, followed_user=userfollowData)
    
    # Eliminar cada objeto Follow encontrado
    for follow_object in follow_objects:
        follow_object.delete()
    
    return HttpResponseRedirect(reverse('user_page', kwargs={'user_id': userfollowData.pk}))

