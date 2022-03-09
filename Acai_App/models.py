from django.db import models
import re
import bcrypt


class UserManager(models.Manager):

    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 1:
            errors['first_name'] = 'First name is too short.'
        if len(post_data['last_name']) < 1:
            errors['last_name'] = 'Last Name must be at least one character long.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):        
            errors['email'] = "Invalid email address."
        if len(post_data['email']) > 30:
            errors['email'] = 'Email address is too long.'
        if len(post_data['address']) > 30:
            errors['address'] = 'Address is too long.'
        if len(post_data['city']) > 30:
            errors['city'] = 'City is too long.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'
        try:
            user = User.objects.get(email = post_data['email'])
            errors['email_in_use'] = 'This email is already associated with an account.'
        except:
            pass
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if not check:
            errors['email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors
    
    def edit_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 1:
            errors['first_name'] = 'First name is too short.'
        if len(post_data['last_name']) < 1:
            errors['last_name'] = 'Last Name must be at least one character long.'
        if len(post_data['email']) > 30:
            errors['email'] = 'Email address is too long.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

class Acai(models.Model):
    method = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    base = models.CharField(max_length=255)
    quantity = models.IntegerField(max_length=255)
    toppings = models.CharField(max_length=255)
    beverage = models.CharField(max_length=255)

class Order(models.Model):
    acai = models.ForeignKey(Acai, related_name='acai_orders', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)



