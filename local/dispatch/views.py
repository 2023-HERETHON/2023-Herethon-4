from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.utils import timezone
# Create your views here.
def whole_list(request):
    dispatchs = Dispatch.objects.all()
    return render(request, 'dispatch/dispatch_all.html', {'dispatchs':dispatchs})

def near_list(request):
    return render(request, 'dispatch/dispatch_near.html', {})

@login_required
def my_list(request):
    my_dispatchs = Dispatch.objects.filter(username=request.user)
    return render(request, 'dispatch/my.html', {'my_dispatchs': my_dispatchs})

# def dispatch_detail(request, pk):
#     print(pk)
#     dispatchs = get_object_or_404(dispatch, id=pk)
#     return render(request, 'dispatch/dispatch_detail.html', {'dispatchs':dispatchs})

@login_required
def dispatch_post(request):
    if request.method == 'POST':
        dispatch_post = Dispatch.objects.create(
        content=request.POST.get('content'),
        country=request.POST.get('country'),
        city=request.POST.get('city'),
        photo = request.FILES.get('photo'),
        author=request.user
        )
    
        return redirect('dispatch:all_list')
    
    return render(request, 'dispatch/dispatch_post.html')


def dispatch_detail(request, pk):
    dispatch_obj = Dispatch.objects.get(pk=pk)
    comments = Comment.objects.filter(article=dispatch_obj)
    # dispatch_obj = get_object_or_404(dispatch, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = dispatch_obj
            comment.save()
            return redirect('dispatch:dispatch_detail', pk=dispatch_obj.pk)
            # return redirect('dispatch:whole_list')
            # return render(request, 'dispatch/dispatch_detail.html')
            # return redirect('dispatch/dispatch_detail.html',pk=dispatch.pk )
    else:
        form = CommentForm()
    context = {
        'dispatch_obj': dispatch_obj,
        'comments': comments,
        'form': form
    }
    return render(request, 'dispatch/dispatch_detail.html', context)
# @require_POST
# def comments_create(request, pk):
#     if request.user.is_authenticated:
#         dispatch_obj = get_object_or_404(dispatch, pk=pk)
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.article = dispatch_obj
#             comment.user = request.user
#             comment.save()
#         return render(request, 'dispatch/dispatch_detail.html', {dispatch_obj.pk})
#     else:
#         form = CommentForm()
#
#     context = {'form': form}
#     return render(request, 'dispatch/comment_form.html', context)


    # if request.user.is_authenticated:
    #     article = get_object_or_404(dispatch, pk=pk)
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         comment = comment_form.save(commit=False)
    #         comment.article = article
    #         comment.user = request.user
    #         comment.save()
    #     return redirect('dispatch:whole_list', article.pk)
    # return redirect('dispatch:my_list')

def comments_delete(request, dispatch_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('dispatch:whole_list', dispatch_pk)

