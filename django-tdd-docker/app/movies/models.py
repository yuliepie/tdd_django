from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Create custom user class that inherits from AbstractUser.
class CustomUser(AbstractUser):
    pass