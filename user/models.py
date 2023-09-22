import uuid as uuid_lib
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import BaseModel
from . import managers


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    class AUTH_PROVIDERS(models.TextChoices):
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"
        TWITTER = "twitter", "Twitter"
        EMAIL = "email", "Email"

    jwt_uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True)
    social_media_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(_("name"), max_length=150)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user's email address has been verified."),
    )
    is_available = models.BooleanField(
        default=True, help_text=_("Designates whether the labeler is available.")
    )
    auth_provider = models.CharField(
        max_length=50,
        choices=AUTH_PROVIDERS.choices,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    one_time_password = models.CharField(max_length=255, blank=True)
    objects = managers.UserManager()

    __original_profile_image_name = None

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_profile_image_name = self.profile_image.name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @property
    def tasks_count(self):
        return self.missions.count()

    @property
    def tasks_finished_count(self):
        return self.missions_through.filter(is_finished=True).count()

    @property
    def success_rate(self):
        from api.v1.unitlabel.utils import calculate_percentage

        tasks_finished_count = (
            self.task_finished
            if hasattr(self, "task_finished")
            else self.tasks_finished_count
        )
        tasks_count = (
            self.task_count if hasattr(
                self, "task_count") else self.tasks_count
        )
        return calculate_percentage(tasks_finished_count, tasks_count)

    @property
    def tasks_progress_count(self):
        if hasattr(self, "task_progress"):
            return self.task_progress
        return self.missions_through.filter(is_finished=False).count()
