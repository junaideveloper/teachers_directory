from django.db import models

#Subject Model
class Subject(models.Model):
	name = models.CharField(max_length=120, null=False, blank=False, unique=True, verbose_name="Subject Name")

# Teacher Model
class Teacher(models.Model):
	first_name = models.CharField(max_length=100,verbose_name="First Name", null=False, blank=False)
	last_name = models.CharField(max_length=100,  verbose_name="Last Name",null=False, blank=False)
	profile_picture = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	email = models.EmailField(max_length=200,  verbose_name="Email",null=False, blank=False, unique=True)
	phone = models.CharField(max_length=100,verbose_name="Phone", null=False, blank=False)
	room_no = models.CharField(max_length=100, verbose_name="Room No", null=False, blank=False)
	subjects = models.ManyToManyField(Subject)

