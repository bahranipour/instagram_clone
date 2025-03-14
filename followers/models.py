
# followers/models.py
from django.db import models
from django.conf import settings

class Follower(models.Model):
    # کاربری که دنبال می‌شود
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'  # برای دسترسی به دنبال‌کنندگان یک کاربر
    )
    
    # کاربری که دنبال‌کننده است
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'  # برای دسترسی به کاربرانی که یک کاربر دنبال می‌کند
    )
    
    # تاریخ ایجاد رابطه دنبال کردن
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # اطمینان از اینکه هر کاربر فقط یک بار می‌تواند کاربر دیگری را دنبال کند
        unique_together = ('user', 'follower')
        ordering = ['-created_at']  # مرتب‌سازی بر اساس تاریخ ایجاد

    def __str__(self):
        return f'{self.follower.username} follows {self.user.username}'