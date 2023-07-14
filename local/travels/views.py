from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *
from .forms import TravelCommentForm
from users.models import Profile


# Create your views here.
def travel_list(request):
  travels = TravelPost.objects.all()
  query = request.GET.get('query')
  if query:
    travels = TravelPost.objects.filter(nation__icontains=query) | TravelPost.objects.filter(city__icontains=query)
  context = {
    'travels' : travels,
    'query': query,
  }
  return render(request, 'travels/travel_list.html', context)


def travel_detail(request, pk):
  travel = TravelPost.objects.get(pk=pk)
  comments = TravelComment.objects.filter(travel=pk)
  travel.views += 1 
  travel.save()
  
  writer_user = travel.author

  if request.method == 'POST':
    form = TravelCommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.travel = travel
      comment.author = request.user
      comment.save()
      return redirect('travels:travel_detail',travel.pk) 
    
  else:
    form = TravelCommentForm()
    user_list = Profile.objects.exclude(user=request.user).prefetch_related('followers', 'followings')
    context = {
    'travel' : travel,
    'comments' : comments,
    'form' : form,
    'user_list':user_list,
    'current_user': request.user,
    'writer_user' : writer_user
    } 
  return render(request, 'travels/travel_detail.html', context)

@login_required
def travel_create(request):
  if request.method == 'POST':
    travel_post = TravelPost.objects.create(
      title=request.POST.get('title'),
      content=request.POST.get('content'),
      nation=request.POST.get('nation'),
      city=request.POST.get('city'),
      together=int(request.POST.get('together')),
      start_date=request.POST.get('start_date'),
      end_date=request.POST.get('end_date'),
      author=request.user
    )
    
    image_files = request.FILES.getlist('image_files')
    for image_file in image_files:
      TravelPhoto.objects.create(travel=travel_post, image=image_file)
    return redirect('travels:travel_list')
  
  return render(request, 'travels/travel_create.html')

# def travel_delete(request, pk):
#   if request.method == "POST":
#     travel = get_object_or_404(TravelPost, pk=pk)
#     travel.delete()
#   return redirect('travels:travel_list')

@require_POST
def travel_likes(request, pk, *args, **kwargs):
  if request.user.is_authenticated:
    travel = get_object_or_404(TravelPost, pk=pk)
    users = travel.likes.all()
    if users.filter(pk=request.user.pk).exists():
      travel.likes.remove(request.user)
    else:
      travel.likes.add(request.user)
    return redirect('travels:travel_detail',pk)
  return render(request, 'travels/travel_detail.html')