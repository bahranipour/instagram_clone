# followers/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follower

User = get_user_model()

def follow_user(request, username):
    # بررسی آیا کاربر وارد سیستم شده است یا نه
    if not request.user.is_authenticated:
        return redirect('login')
    
    # دریافت کاربری که قرار است دنبال شود
    user_to_follow = get_object_or_404(User, username=username)
    
    # بررسی آیا کاربر جاری قبلاً این کاربر را دنبال کرده است یا نه
    follower, created = Follower.objects.get_or_create(
        user=user_to_follow,  # کاربری که دنبال می‌شود
        follower=request.user  # کاربری که دنبال‌کننده است
    )
    
    if not created:
        # اگر قبلاً دنبال کرده بود، آنفالو کند (رابطه را حذف کند)
        follower.delete()
    
    # بازگشت به صفحه پروفایل کاربر
    return redirect('user_list')