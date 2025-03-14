# accounts/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm,CustomPasswordChangeForm
from posts.models import Post
from followers.models import Follower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'ثبت نام شما با موفقیت انجام شد')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {username}!')
                return redirect('profile',username=request.user.username)  # تغییر به صفحه اصلی
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید.')
    return redirect('home')  # تغییر به صفحه اصلی 



@login_required
def profile(request, username):
    # دریافت کاربر مورد نظر
    user = get_object_or_404(User, username=username)
    
    # دریافت پست‌های کاربر
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # تعداد دنبال‌کنندگان و دنبال‌شوندگان
    followers_count = Follower.objects.filter(user=user).count()
    following_count = Follower.objects.filter(follower=user).count()

    
    
    # بررسی آیا کاربر جاری، این پروفایل را دنبال کرده است یا نه
    is_following = False
    if request.user.is_authenticated:
        is_following = Follower.objects.filter(user=user, follower=request.user).exists()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    
    return render(request, 'accounts/profile.html', context)



@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت!')
            return redirect('home')  # تغییر به صفحه پروفایل یا صفحه اصلی
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('login')  # اگر کاربر وارد نشده باشد، به صفحه ورود هدایت شود
    
  
    # دریافت تمام کاربران به جز خود کاربر جاری
    users = User.objects.exclude(id=request.user.id).filter(is_staff=False, is_superuser=False)

    # تعداد کاربران در هر صفحه (مثلاً 10 کاربر در هر صفحه)
    paginator = Paginator(users, 10)
    
    # دریافت شماره صفحه از پارامتر GET
    page_number = request.GET.get('page')
    
    try:
        user_page = paginator.page(page_number)
    except PageNotAnInteger:
        # اگر صفحه معتبر نباشد، صفحه اول نمایش داده می‌شود
        user_page = paginator.page(1)
    except EmptyPage:
        # اگر صفحه خارج از محدوده باشد، آخرین صفحه نمایش داده می‌شود
        user_page = paginator.page(paginator.num_pages)
    
    # بررسی وضعیت دنبال کردن هر کاربر
    user_data = []
    for user in user_page:
        is_following = Follower.objects.filter(user=user, follower=request.user).exists()
        user_data.append({
            'user': user,
            'is_following': is_following,
        })
    
    context = {
        'user_data': user_data,
        'user_page': user_page,  # صفحه‌بندی شده کاربران
    }
    
    return render(request, 'accounts/user_list.html', context)