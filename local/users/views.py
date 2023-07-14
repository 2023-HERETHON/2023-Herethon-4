from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from users.models import Profile
from travels.models import TravelPost
from lives.models import Video


def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['repeat']:
            new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            print('회원가입 성공')
            return redirect('users:more_info')
    return render(request, 'idsignup.html')

def input_info(request):
    if request.method == "POST":
        new_user = request.user
        name = request.POST['name'] 
        nickname = request.POST['nickname'] 
        phone = request.POST['phone'] 
        cntry_residence = request.POST['cntry_residence'] 
        city_residence = request.POST['city_residence'] 
        visited_cntry = request.POST['visited_cntry'] 
        visited_city = request.POST['visited_city'] 
        preferred_cntry = request.POST['preferred_cntry'] 
        preferred_city = request.POST['preferred_city'] 
        shop_option = request.POST['shop']

        try:
            profile = new_user.profile  # 기존에 연결된 프로필 객체 가져오기
            # 이미 연결된 프로필이 있는 경우 필드 업데이트
            profile.name = name
            profile.nickname = nickname
            profile.phone = phone
            profile.cntry_residence = cntry_residence
            profile.city_residence = city_residence
            profile.visited_cntry = visited_cntry
            profile.visited_city = visited_city
            profile.preferred_cntry = preferred_cntry
            profile.preferred_city = preferred_city
            if shop_option == 'No':
                profile.is_provider = False
            else:
                profile.is_provider = True
            profile.save()
        except Profile.DoesNotExist:
            # 연결된 프로필이 없는 경우 새로운 프로필 생성
            profile = Profile.objects.create(user=new_user, name=name, nickname=nickname, phone=phone,
                                             cntry_residence=cntry_residence, city_residence=city_residence,
                                             visited_cntry=visited_cntry, visited_city=visited_city,
                                             preferred_cntry=preferred_cntry, preferred_city=preferred_city,
                                             is_provider = (shop_option == 'Yes'))
        return redirect('lives:live_list')
    else:
        return render(request, 'general-signup.html')
    

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('로그인 성공')
            return redirect('lives:live_list')
        else: 
            return render(request, 'bad_login.html')
    else:
        return render(request, 'onboarding.html')
    
def id_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('로그인 성공')
            return redirect('lives:live_list')
        else: 
            return render(request, 'bad_login.html')
    else:
        return render(request, 'phone_login.html')


def logout(request):
    auth.logout(request)
    return redirect('lives:live_list')


# 전체 사용자 리스트를 가져와서 user_list로 출력
@login_required
def user_view(request):
    if request.method == 'GET':
        user_list = Profile.objects.exclude(user=request.user).prefetch_related('followers', 'followings')
        return render(request, 'user_list.html', {'user_list':user_list, 'current_user': request.user})
    

def user_follow(request, id, pk):
    me = request.user
    click_user = User.objects.get(id=id)

    try:
        click_profile = Profile.objects.get(user=click_user)
    except Profile.DoesNotExist:
        # Profile 객체가 존재하지 않을 경우, 생성해야 함
        click_profile = Profile.objects.create(user=click_user)

    try:
        my_profile = Profile.objects.get(user=me)
    except Profile.DoesNotExist:
        # Profile 객체가 존재하지 않을 경우, 생성해야 함
        my_profile = Profile.objects.create(user=me)

    if my_profile.user in click_profile.followers.all():
        click_profile.followers.remove(my_profile.user)
        my_profile.followings.remove(click_user)
    else:
        click_profile.followers.add(my_profile.user)
        my_profile.followings.add(click_user)
    return redirect('travels:travel_detail', pk=pk)


@login_required
def mypage(request):
    if request.method == 'POST':
        mypage_list = request.POST.get('mypage-list')
        if mypage_list == "travel":
            objs = TravelPost.objects.filter(likes=request.user)
            travel = '여행리스트'
            context = {
                'travel': travel,
                'objs': objs,
            }
            return render(request, 'mypage.html', context)   
    objs = Video.objects.filter(saves=request.user)
    return render(request, 'mypage.html', {'objs': objs})