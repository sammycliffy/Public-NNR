from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    companyAddress = models.CharField(max_length=255, null=True)
    companyName = models.CharField(max_length=255, null=True)
    contactPerson = models.CharField(max_length=255, null=True)
    contactPhone = models.CharField(max_length=255, null=True)

    #   objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        #self.user.username = email
        #self.matric_number = slugify_matric_number(self)
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    '''
	@property
	def is_estateuser(self):
		#"Is the user an estate occupant?"
		return self.is_estateuser

	@property
	def is_estateguard(self):
		#"Is the user an estate guard?"
		return self.is_estateguard

	@property
	def is_estateadmin(self):
		#"Is the user an estate admin member?"
		return self.is_estateadmin
	'''

    def __str__(self):
        return str(self.email)


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


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now=True)
