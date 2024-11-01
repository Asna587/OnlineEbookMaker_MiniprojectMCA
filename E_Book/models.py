from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=20)

class User(models.Model):
    LOGIN = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dob = models.DateField()
    phone = models.BigIntegerField()
    email = models.CharField(max_length=50)
    photo = models.FileField()
    place = models.CharField(max_length=50)
    pin = models.BigIntegerField()
    post = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)

class Book(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50)
    description = models.TextField()
    thumbnail = models.ImageField()
    date_of_upload = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='book')

class BookEditRequest(models.Model):
    BOOK = models.ForeignKey(Book,on_delete=models.CASCADE)
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=30,default='pending')
    date = models.DateField(auto_now_add=True)

class Feedbacks(models.Model):
    BOOK = models.ForeignKey(Book,on_delete=models.CASCADE)
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField()
    date = models.DateField()

class Complaint(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint = models.TextField()
    date = models.DateField(auto_now_add=True)
    reply = models.TextField(default='pending')


