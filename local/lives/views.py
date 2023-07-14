
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from .forms import VideoCommentForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST

from users.models import Profile



# class VideoStreamingView(View):
#   def get(self, request, *args, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)("video_stream", {"type": "stream.video"})
#     return HttpResponse("Video streaming started.")



@gzip.gzip_page
def live_stream(request):
  try:
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
  except:
    pass
  return render(request, 'lives/live_stream.html')

#to capture video class
class VideoCamera(object):
  def __init__(self):
    self.video = cv2.VideoCapture(0)
    (self.grabbed, self.frame) = self.video.read()
    threading.Thread(target=self.update, args=()).start()

  def __del__(self):
    self.video.release()

  def get_frame(self):
    image = self.frame
    _, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()

  def update(self):
    while True:
      (self.grabbed, self.frame) = self.video.read()

def gen(camera):
  while True:
    frame = camera.get_frame()

    yield (b'--fram\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    

# def home(request):
#     yield (b'--frame\r\n'
#       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#     if request.user.is_authenticated:  # 로그인된 상태인지 확인
#         try:
#             profile = request.user.profile  # 프로필 객체 가져오기
#         except Profile.DoesNotExist:
#             # 프로필 객체가 없는 경우 신규 프로필 생성
#             profile = Profile.objects.create(user=request.user)

#         if not profile.phone:  # phone 필드가 비어있는지 확인
#             return redirect('users:more_info')
#     else:
#         return render(request, 'lives:live_list')

#     return render(request, 'lives:live_list')


    

def live_list(request):
  video = Video.objects.all()[:6]
  osaka1 = None
  osakas = None

  try:
    osaka1 = Video.objects.filter(city__icontains='오사카').latest('id')
  except Video.DoesNotExist:
    pass

  try:
    osakas = Video.objects.filter(city__icontains='오사카').order_by('-id')[1:4]
  except Video.DoesNotExist:
    pass

  query = request.GET.get('query')
  if query:
    travels = Video.objects.filter(nation__icontains=query) | Video.objects.filter(city__icontains=query)

  context = {
    'video': video,
    'query': query,
    'osaka1': osaka1,
    'osakas': osakas,
  }

  if request.user.is_authenticated:  # 로그인된 상태인지 확인
    try:
        profile = request.user.profile  # 프로필 객체 가져오기
    except Profile.DoesNotExist:
        # 프로필 객체가 없는 경우 신규 프로필 생성
        profile = Profile.objects.create(user=request.user)

    if not profile.phone:  # phone 필드가 비어있는지 확인
      return redirect('users:more_info')
  else:
      return render(request, 'lives/live_home.html', context)

  return render(request, 'lives/live_home.html', context)

def live_recent(request):
  video = Video.objects.all().order_by('-id')
  query = request.GET.get('query')
  if query:
    video = Video.objects.filter(nation__icontains=query) | Video.objects.filter(city__icontains=query)
  context = {
    'video': video,
    'query': query,
  }
  return render(request, 'lives/live_recent.html', context)

def live_soon(request):
  video = Video.objects.filter(state='reservation')
  context = {
    'video': video,
  }
  return render(request, 'lives/live_soon.html', context)


def live_detail(request, pk):
  video = Video.objects.get(pk=pk)
  comments = VideoComment.objects.filter(video=pk)
  if request.method == 'POST':
    form = VideoCommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.video = video
      comment.author = request.user
      comment.save()
      return redirect('lives:live_detail',video.pk) 
    
  else:
    form = VideoCommentForm()
  context = {
    'video' : video,
    'comments' : comments,
    'form' : form
  } 
  return render(request, 'lives/live_detail.html', context)

@login_required
def live_create(request):
  if request.method == 'POST':
    # POST 요청을 처리하여 새로운 Video 객체 생성
    state = request.POST.get('state')
    title = request.POST.get('title')
    sub1 = request.POST.get('sub1')
    sub2 = request.POST.get('sub2')
    sub3 = request.POST.get('sub3')
    video_file = request.FILES.get('video_file')
    thumbnail = request.FILES.get('thumbnail')
    author = request.user 
    nation = request.POST.get('nation')
    city = request.POST.get('city')
    views = 0 
    date = request.POST.get('date')
    
    video = Video.objects.create(
      state=state,
      title=title,
      sub1=sub1,
      sub2=sub2,
      sub3=sub3,
      video_file=video_file,
      thumbnail=thumbnail,
      author=author,
      nation=nation,
      city=city,
      views=views,
      date=date
    )
    # 새로운 Video 객체 생성 후, 어떤 작업을 수행하거나 리디렉션할 수 있음
    
    return redirect('lives:live_detail', video_id=video.id)
  # GET 요청 처리
  return render(request, 'lives/live_create.html')


@require_POST
def live_likes(request, pk, *args, **kwargs):
  if request.user.is_authenticated:
    video = get_object_or_404(Video, pk=pk)
    users = video.saves.all()
    if users.filter(pk=request.user.pk).exists():
      video.saves.remove(request.user)
    else:
      video.saves.add(request.user)
    return redirect('lives:live_detail',pk)
  return render(request, 'lives/live_detail.html')
