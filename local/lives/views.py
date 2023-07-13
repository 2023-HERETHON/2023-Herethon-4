from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import cv2
import threading
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

from users.models import Profile



# class VideoStreamingView(View):
#   def get(self, request, *args, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)("video_stream", {"type": "stream.video"})
#     return HttpResponse("Video streaming started.")

@gzip.gzip_page
def video(request):
  try:
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace; boundary=frame")
  except:
    pass
  return render(request, 'lives/video.html')

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
    

def home(request):
    if request.user.is_authenticated:  # 로그인된 상태인지 확인
        try:
            profile = request.user.profile  # 프로필 객체 가져오기
        except Profile.DoesNotExist:
            # 프로필 객체가 없는 경우 신규 프로필 생성
            profile = Profile.objects.create(user=request.user)

        if not profile.phone:  # phone 필드가 비어있는지 확인
            return redirect('users:more_info')
    else:
        return render(request, 'index.html')

    return render(request, 'index.html')