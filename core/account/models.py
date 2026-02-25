from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class UserManager(BaseUserManager):
    """
    Custom User Model Manager where email is unique beside username 
    """
    def create_user(self,email,password,**extra_fields):
        """
        create and save user with the given email and password and extras
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email= email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        """
        craete and save a super user 
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_verified',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super User must have is_staff = true'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Super User must have is_superuser = true'))
        
        self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    '''
    Docstring for User
    https://testdriven.io/blog/django-custom-user-model/
    '''
    email = models.EmailField(max_length=255,unique=True,verbose_name="email address")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    #verified email just checked in APIs not in forms and logins
    # TODO: can be done with permission classes
    is_verified = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return self.email
    
