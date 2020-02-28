from django.db import models
from django.contrib import messages
import re


# Create your models here.


class UserManager(models.Manager):
    def user_validator(self, post_data):
        user_errors = {}
        if len(post_data["first_name"]) < 3:
            user_errors["first_name"] = "first name should be at least 3 characters"
        if len(post_data["last_name"]) < 3:
            user_errors["last_name"] = "last name should be at least 3 characters"
        Email_Regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_Regex.match(post_data['email']):
            user_errors['email'] = 'invalid email address!'
        if len(post_data["email"]) < 3:
            user_errors["email"] = "email should be at least 3 characters"
        if len(post_data["password"]) < 3:
            user_errors["password"] = "password should be at least 3 characters"
        if post_data["password_confirm"] != post_data['password']:
            user_errors["password_confirm"] = "passwords do not match"
        return user_errors


class JobManager(models.Manager):
    def job_validator(self, post_data):
        job_errors = {}
        if len(post_data["title"]) < 3:
            job_errors["title"] = "title should be at least 3 characters"
        if len(post_data["description"]) < 3:
            job_errors["description"] = " description should be at least 3 characters"

        if len(post_data["location"]) < 3:
            job_errors["location"] = "location should be at least 3 characters"
        return job_errors

    def edit_validator(self, post_data):
        edit_errors = {}
        if len(post_data["title"]) < 3:
            edit_errors["title"] = "title should be at least 3 characters"
        if len(post_data["description"]) < 3:
            edit_errors["description"] = "description should be at least 3 characters"
            edit_errors['location'] = 'invalid location address!'
        if len(post_data["location"]) < 3:
            edit_errors["location"] = "location should be at least 3 characters"
        return edit_errors


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Job(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    location = models.CharField(max_length=45)
    category = models.CharField(max_length=45)

    jobs_to_add = models.BooleanField(default=True)

    user = models.ForeignKey(
        "User", related_name="user_jobs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
