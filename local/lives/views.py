from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

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
    yield (b'--frame\r\n'
          b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    

# def live_list(request):
#   video = Video.objects.all()
#   osaka1 = Video.objects.filter(city__icontains='오사카').latest('id')
#   osakas = Video.objects.filter(city__icontains='오사카').order_by('-id')[1:4]
#   query = request.GET.get('query')
#   if query:
#     travels = Video.objects.filter(nation__icontains=query) | Video.objects.filter(city__icontains=query)
#   context = {
#     'video' : video,
#     'query': query,
#     'osaka1': osaka1,
#     'osakas': osakas,
#   }
#   return render(request, 'lives/live_home.html',context)

def live_list(request):
  video = Video.objects.all()
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
  return render(request, 'lives/live_home.html', context)

# def live_recent(request):
  

