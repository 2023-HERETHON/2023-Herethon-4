from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import TravelCommentForm


# Create your views here.
def travel_list(request):
  travels = TravelPost.objects.all()
  context = {
    'travels' : travels,
  }
  return render(request, 'travels/travel_list.html', context)


def travel_detail(request, pk):
  travel = TravelPost.objects.get(pk=pk)
  comments = TravelComment.objects.filter(travel=pk)
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
  context = {
    'travel' : travel,
    'comments' : comments,
    'form' : form
  } 
  return render(request, 'travels/travel_detail.html', context)

@login_required
def travel_create(request):
  if request.method == 'POST':
    travel_post = TravelPost.objects.create(
      title=request.POST.get('title'),
      content=request.POST.get('content'),
      location=request.POST.get('location'),
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

  
def travel_delete(request, pk):
  if request.method == "POST":
    travel = get_object_or_404(TravelPost, pk=pk)
    travel.delete()
  return redirect('travels:travel_list')