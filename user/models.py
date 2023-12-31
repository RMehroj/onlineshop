import uuid as uuid_lib
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel
from . import managers


class Company(BaseModel):
    owner = models.OneToOneField(
        "Owner", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Company")
        verbose_name_plural = ("Companies")

    def __str__(self):
        return self.name or f"{self.pk}"

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ", "")
        super().save(*args, **kwargs)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    class AUTH_PROVIDERS(models.TextChoices):
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"
        TWITTER = "twitter", "Twitter"
        EMAIL = "email", "Email"
    
    class ROLES(models.TextChoices):
        OWNER = "owner", "Owner"

    jwt_uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    social_media_id = models.CharField(max_length=50, blank=True)
    username = models.CharField(("name"), max_length=150)
    full_name = models.CharField(
        ("full name"), max_length=150, blank=True)
    email = models.EmailField(("email address"), unique=True)
    phone = PhoneNumberField(("phone number"), blank=True)
    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              blank=True,
                              null=True,
                              default='M')

    is_staff = models.BooleanField(
        default=False,
        help_text=(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=(
            "Designates whether this user's email address has been verified."),
    )
    is_available = models.BooleanField(
        default=True, help_text=("Designates whether the labeler is available.")
    )
    auth_provider = models.CharField(
        max_length=50,
        choices=AUTH_PROVIDERS.choices,
    )
    role = models.CharField(max_length=50, choices=ROLES.choices)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = managers.UserManager()
        
    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")
        app_label = 'user' 

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
    
    def register(self): 
        self.save() 
  
    @staticmethod
    def get_user_by_email(email): 
        try: 
            return User.objects.get(email=email) 
        except: 
            return False
    
    def isExists(self): 
        if User.objects.filter(email=self.email): 
            return True
        return False

class Owner(User):
    objects = managers.AdminManager()

    class Meta:
        proxy = True
