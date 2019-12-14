from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import UserManager


#---USER MODEL---
class UserManager(BaseUserManager):
    def create_user(self, email, firstname, secondname,  password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not name:
            raise ValueError("Users must have a name")
        if not surname:
            raise ValueError("Users must have a surname")
        if not father_name:
            raise ValueError("Users must have a father_name")
        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            secondname = secondname,
        )
        user.set_password(password) # change user password
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, firstname, secondname, password=None):
        user = self.create_user(
                email,
                firstname = firstname,
                secondname = secondname,
                password = password,
                is_staff = True
        )
        return user

    def create_superuser(self, email=None, password=None):
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    THEME_CHOICES = (
        ('Client', 'Client'),
        ('Company', 'Company'),
    )

    email = models.EmailField(max_length=40, blank=True, null=True, unique=True)

    firstname = models.CharField(max_length=40, blank=True, null=True)
    secondname = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=40, choices=THEME_CHOICES, blank=True, null=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that's built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_user_context(self):
        context = {
            'firstname': self.firstname,
            'secondname': self.secondname,
            'email': self.email,
            'city': self.city,
            'type': self.type,
            'page_name': "",
            'user_id': self.id,
        }
        return context

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
#---USER MODEL---


#---ACCOUNTS_TYPES_MODELS---
class Client(models.Model):
    THEME_CHOICES = (
        ('Passenger', 'Passenger'),
        ('Small jeep', 'Small jeep'),
        ('Big jeep', 'Big jeep'),
        ('Gazel(before 1.5t)', 'Gazel(before 1.5t)'),
    )
    statenumber = models.CharField(max_length=255, unique=False)
    mark = models.CharField(max_length=255, unique=False)
    model = models.CharField(max_length=255, unique=False)
    region = models.CharField(max_length=255, unique=False)
    car_type = models.CharField(max_length=255, choices=THEME_CHOICES, unique=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, unique=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.company_name
#---ACCOUNTS_TYPES_MODELS---


#---SERVICE_MODELS---
class ServiceManager(models.Manager):
    def create_example_service(self, user, company):
        service = self.create(
            name = "Example Service",
            car_type = "Passenger",
            price = 0,
            user = user,
            company = company,
            example = True,
        )
        return service


class Service(models.Model):
    THEME_CHOICES = (
        ('Passenger', 'Passenger'),
        ('Small jeep', 'Small jeep'),
        ('Big jeep', 'Big jeep'),
        ('Gazel(before 1.5t)', 'Gazel(before 1.5t)'),
    )
    name = models.CharField(max_length=255)
    car_type = models.CharField(max_length=255, choices=THEME_CHOICES, unique=False)
    price = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    example = models.BooleanField(default=False)

    objects = ServiceManager()

    def __str__(self):
        name = "" + self.name + "(" + self.car_type + ")" + " - " + str(self.price) + ".р"
        return name

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})
#---SERVICE_MODELS---
