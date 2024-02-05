"""Custom User model. Use email and first_name as mandatory."""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
)
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GroupProxy(Group):
    """Proxy class for Group so that it can reside in the same app as users"""

    class Meta:
        """Meta class."""

        # pylint: disable=protected-access, no-member
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


class UserManager(BaseUserManager):
    """Manager for our custom User."""

    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, first_name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name and password.
        """
        user = self.create_user(email, password=password, first_name=first_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email/password for authentication."""

    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False
    )
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=False, unique=True, null=False)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = UserManager()

    class Meta:
        """Meta for this model."""

        verbose_name = _("user")
        verbose_name_plural = _("users")
        # app_label = "Authentication and Authorization"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
