from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from .models import Category, Thread, Post
from django.contrib.auth.models import User
from notifications.signals import notify

app_name = 'forum'


def thread_list(request, category_id, page_number):
    category = get_object_or_404(Category, id=category_id)
    threads = Thread.objects.filter(category=category).order_by('-sticky', '-last_post_date')
    paginator = Paginator(threads, 10)
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'forum/thread_list.html', context)


def thread_detail(request, thread_id, page_number):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.views += 1
    thread.save()
    posts = thread.post_set.all().order_by('created_at')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {'thread': thread, 'page_obj': page_obj}
    return render(request, 'forum/thread_detail.html', context)


@login_required
def new_thread(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        thread = Thread.objects.create(
            category=category,
            title=request.POST['title'],
            created_by=request.user
        )
        post = Post.objects.create(
            thread=thread,
            created_by=request.user,
            body=request.POST['body']
        )
        recipient_user = User.objects.filter(is_superuser=True)
        notify.send(request.user, recipient=recipient_user, verb='created a new thread', target=thread,
                    action_object=post)
        return redirect('thread_detail', thread_id=thread.id, page_number=1)
    else:
        context = {'category': category}
    return render(request, 'forum/new_thread.html', context)


@login_required
@permission_required('forum.add_post', raise_exception=True)
def reply_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        post = Post.objects.create(
            thread=thread,
            created_by=request.user,
            body=request.POST['body']
        )
        thread.last_post_date = post.created_at
        thread.last_post_by = request.user
        thread.save()
        notify.send(request.user, recipient=thread.created_by, verb='replied to your thread', target=thread,
                    action_object=post)
        return redirect('thread_detail', thread_id=thread.id, page_number=1)
    else:
        context = {'thread': thread}
    return render(request, 'forum/reply_thread.html', context)


@login_required
@permission_required('forum.add_post', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.body = request.POST['body']
        post.edited = True
        post.edited_at = timezone.now()
        post.edited_by = request.user
        post.save()
        return redirect('thread_detail', thread_id=post.thread.id, page_number=1)
    else:
        context = {'post': post}
    return render(request, 'forum/edit_post.html', context)
