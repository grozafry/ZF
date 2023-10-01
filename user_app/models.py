from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from validators import validate_mobile_number

class UserManager(BaseUserManager):

    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('Mobile field is mandatory!')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, **extra_fields)


class User(AbstractUser):
    
    class Role(models.TextChoices):
        ADVISOR = 'Advisor', 'Advisor'
        USER = 'User', 'User'
        ADMIN = 'Admin', 'Admin'

    username = models.CharField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=15, unique=True, validators=[validate_mobile_number])
    role = models.CharField(max_length=20, choices=Role.choices)
    otp = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    class Meta:
        db_table = 'users'

