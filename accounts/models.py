from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import OneToOneField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError("user must have an username")
        if not phone_number:
            raise ValueError('user must have a phone number')
        user = self.model(
            # tip: the code below will convert an email with capital to a small and make it normal
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        # tip: next line will store the password in encoded
        user.set_password(password)
        # tip: next line will store the data in default database that we mention in setting
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, phone_number, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICES = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    # required field
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # tip : adding this field to a custom user model is very important because authentication in login logic will
    # check that is this flag is green or not and then authenticate the user base on username and password
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # todo: check that we can use two username field or not (phone)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']
    objects = UserManager()

    def __str__(self):
        return self.email

    # tip : has_perm(self, perm, obj=None): This method is used to check if a user has a
    # specific permission for a particular object (optional).
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # tip : has_module_perms(self, app_label): This method is used to check if a user has any permissions
    # for a specific Django app (identified by its app label).
    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Restaurant'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role


class UserProfile(models.Model):
    ZONE_CHOICES = (
         ('Z1', 'Zone 1'),
         ('Z2', 'Zone 2'),
         ('Z3', 'Zone 3'),
         ('Z4', 'Zone 4'),
         ('Z5', 'Zone 5'),
         ('Z6', 'Zone 6'),
         ('Z7', 'Zone 7'),
         ('Z8', 'Zone 8'),
         ('Z9', 'Zone 9'),
         ('Z10', 'Zone 10'))

    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    zone = models.CharField(max_length=10, choices=ZONE_CHOICES, blank=True, null=True, default='Z1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


