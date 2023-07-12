from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

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
  context = {
    'travel' : travel,
    'comments' : comments,
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

# @login_required
# def create(request):
#   if request.method=="GET":
#     return render(request, 'musicapp/create.html')
#   else:
#     Music.objects.create(
#       image = request.FILES.get("image"),
#       title=request.POST.get('title'),
#       content=request.POST.get('content'),
#       music_title=request.POST.get('music_title'),
#       music_singer=request.POST.get('music_singer'),
#       author=request.user
#     )
#     return redirect('index')
    
# def update(request, id):
#   writing=get_object_or_404(Music, pk=id)
#   if request.method=="GET":
#     return render(request, 'musicapp/update.html', {'writing':writing})
#   else:
#     writing.title=request.POST.get('title')
#     writing.content=request.POST.get('content')
#     writing.music_title=request.POST.get('music_title')
#     writing.music_singer=request.POST.get('music_singer')
#     new_image=request.FILES.get('image')
#     if new_image:
#       writing.image.delete()
#       writing.image=new_image
#     writing.save()
#     return redirect('mypage',writing.author) 
    

# @login_required
# def mypage(request, author):
#   try:
#     writings = Music.objects.filter(author=author).order_by('-id')
#   except Music.DoesNotExist:
#     writings = []
#   return render(request, 'musicapp/mypage.html', {'writings': writings})