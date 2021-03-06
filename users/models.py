import email
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.contrib.auth import get_user_model
from sorl.thumbnail import get_thumbnail


class BasicCustomerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(
                "Почта должна быть указана в обязательном порядке.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Администраторы должны быть определенны с is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class BasicCustomer(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_lessor = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        help_text=_("Required. Enter a valid email address."),
    )
    mobile_number = PhoneNumberField(
        _("mobile number"),
        blank=True,
        error_messages={
            "incorrect": _("Incorrect mobile number."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    middle_name = models.CharField("Отчество", max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    avatar = models.ImageField(
        verbose_name="Аватарка пользователя",
        upload_to="uploads/",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = BasicCustomerManager()

    def get_image_100x100(self):
        return get_thumbnail(self.avatar, "100x100", upscale=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            image = Image.open(self.avatar.path)
            if image.height > 100 or image.width > 100:
                image.thumbnail((100, 100), Image.ANTIALIAS)
                image.save(self.avatar.path)

        if self.is_lessor and not LessorProfile.objects.check_if_lessor_exist(self.id):
            LessorProfile.objects.create(user=self).save()
        if self.is_tenant and not TenantProfile.objects.check_if_tenant_exist(self.id):
            TenantProfile.objects.create(user=self).save()
        if not self.is_lessor and LessorProfile.objects.check_if_lessor_exist(self.id):
            LessorProfile.objects.filter(user=self).delete()
        if not self.is_tenant and TenantProfile.objects.check_if_tenant_exist(self.id):
            TenantProfile.objects.filter(user=self).delete()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


User = get_user_model()


class TenantManager(models.Manager):
    def check_if_tenant_exist(self, id):
        return self.get_queryset().filter(user=id).exists()


class TenantProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="tenant_profile"
    )
    contacts_and_over_information = models.TextField("Контакты и другая важная информация", blank=True)
    balance = models.BigIntegerField('Баланс', default=0)
    objects = TenantManager()

    class Meta:
        verbose_name = "Профиль арендатора"
        verbose_name_plural = "Профили арендаторов"

    def __str__(self):
        return f"Арендатор {self.user.email}"


class LessorManager(models.Manager):
    def check_if_lessor_exist(self, id):
        return self.get_queryset().filter(user=id).exists()


class LessorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="lessor_profile"
    )
    contacts_and_over_information = models.TextField("Контакты и другая важная информация", blank=True)

    def __str__(self):
        return f"Арендодатель {self.user.email}"

    objects = LessorManager()

    class Meta:
        verbose_name = "Профиль арендодателя"
        verbose_name_plural = "Профили арендодателей"
