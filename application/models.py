""" Database models (tables) """

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        username = self.model.normalize_username(username)
        email = self.normalize_email(email)

        user = self.model(username=username,
                          email=email,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Category(models.Model):
    category = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'
        ordering = ['category']
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{str(self.category)}"


class Task(models.Model):
    task = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    PRIORITIZE_CHOICES = [(1, 1), (2, 2), (3, 3)]
    prioritize = models.IntegerField(choices=PRIORITIZE_CHOICES, default=1)
    status = models.BooleanField()
    deadline = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creation_datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tasks'
        ordering = ['status', '-prioritize']
        managed = True
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{str(self.category)}"
