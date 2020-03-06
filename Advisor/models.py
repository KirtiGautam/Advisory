from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class department(models.Model):
    name = models.CharField(max_length=255)
    HOD = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class teachers(models.Model):
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=50)
    department = models.ForeignKey(department, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, uid=None, is_admin=False, is_superuser=False):
        if not username:
            raise ValueError('User must have a username')
        if not password:
            raise ValueError('User must have a password')
        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.is_superuser = is_superuser
        user_obj.uid = uid
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, password=None, uid=None):
        user = self.create_user(username,
                                password,
                                uid=uid,
                                is_superuser=True)
        return user

    def create_admin(self, username, password=None, uid=None):
        user = self.create_user(username,
                                password,
                                uid=uid,
                                is_admin=True)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    uid = models.OneToOneField(
        teachers,  on_delete=models.CASCADE, default=None, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.uid)
