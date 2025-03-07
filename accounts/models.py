from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

import uuid
from schools.models import *
from schools.models import School
import uuid
from schools.models import School
import uuid

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
    email = models.EmailField(blank = True, default = '', unique = True)
    name = models.CharField(max_length = 50, blank = True, default = '')  #blank,default=True should be removed before production
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = True)
    school = models.OneToOneField(School, on_delete=models.CASCADE,blank = True, null = True)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(blank = True, null = True)     #blank,null=True should be removed before production
    otp     = models.PositiveIntegerField(blank = True, null = True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    def get_school_name(self, obj):
        if obj.school:
            return obj.school.name
        return None
