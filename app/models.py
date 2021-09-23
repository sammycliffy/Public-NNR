from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)  # change password to hash
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password):
        # if not email:
        #     raise ValueError("User must have an email")
        # if not password:
        #     raise ValueError("User must have a password")

        user = self.create_user(
            email,
            password=password,
        )

        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    companyAddress = models.CharField(max_length=255, null=True)
    companyName = models.CharField(max_length=255, null=True)
    contactPerson = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        ''' Does the user have a specific permission'''
        return True   # This may need to be changed depending on the object we want to find permission for

    def has_module_perms(self, app_label):
        ''' Does the user have permission to view the app 'app_label'? The default answer is yes.
        This may be modified later on. '''

        return True

    # @property
    # def is_staff(self):
    #     ''' IS the user a member of staff? '''
    #     return self.is_admin


class RadioActiveSourcesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    acknowleged = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    siteVisit = models.BooleanField(default=False)
    installation = models.BooleanField(default=False)
    sourceCategory = models.CharField(max_length=255, null=True)
    sourceName = models.CharField(max_length=255, null=True)
    sourceState = models.CharField(max_length=255, null=True)
    sourceAddress = models.CharField(max_length=255, null=True)


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now=True)
