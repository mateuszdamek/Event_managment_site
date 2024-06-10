from django.db import models
from enum import Enum
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("An email is required.")
        if not username:
            raise ValueError("A username is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("An email is required.")
        if not username:
            raise ValueError("A username is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_ID = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        return self.username




# * Event Status Enum
class EventStatus(Enum):
    PLANNED = "Planned"
    DURING = "During"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"


# * Event model
class Event(models.Model):
    event_ID = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    date = models.DateField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()  #! Could add specific time
    end_date = models.DateTimeField()  #! Could add specific time
    location = models.CharField(max_length=255)
    # organizer_ID = models.IntegerField()
    parent_event_ID = models.IntegerField()
    status = models.CharField(
        max_length=10, choices=[(status.value, status.name) for status in EventStatus]
    )
    organizer_ID = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field="user_ID"
    )  # ? to_field may be unnecessary since User has user_id as auto primary key to that field
    parent_event_ID = models.ForeignKey(
        "self", on_delete=models.CASCADE, to_field="event_ID", null=True, blank=True
    )  #! Need to be tested as its self-referential foreign key
    #! Check if this table works right as theres duplication for some fields
    # TODO Refractor if duplication fucks app table


# * Submission Status Enum
class SubmissionEnum(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


# * Event_Submission model
class Event_Submission(models.Model):
    submission_ID = models.BigAutoField(primary_key=True)
    # event_ID = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    submitter_ID = models.IntegerField()
    status = models.CharField(
        max_length=15,
        choices=[(status.value, status.name) for status in SubmissionEnum],
    )
    event_ID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)


# * Event Registration model
from django.utils import timezone

class Event_Registration(models.Model):
    registration_ID = models.BigAutoField(primary_key=True)
    registration_Date = models.DateTimeField(default=timezone.now)
    event_ID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)



# * Category model
class Category(models.Model):
    category_ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


# *Event Category model
class Event_Category(models.Model):
    # event_ID = models.IntegerField() #! Need to add class meta in serializer to use Constraint
    # category_ID = models.IntegerField() #! To make 2 primary keys
    event_ID = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_ID = models.ForeignKey(Category, on_delete=models.CASCADE)


# * Tag model
class Tag(models.Model):
    tag_ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


# * Event Tag Model
class Event_Tag(models.Model):
    # event_ID = models.IntegerField() #! Need to add class meta in serializer to use Constraint
    # tag_ID = models.IntegerField() #! To make 2 primary keys
    event_ID = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag_ID = models.ForeignKey(Tag, on_delete=models.CASCADE)

