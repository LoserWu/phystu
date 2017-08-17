# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.db import models

reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.
class Section(models.Model):
	Name=models.CharField(max_length=40)
	introduction=models.TextField()
	image=models.CharField(max_length=100)
	style=models.CharField(max_length=30)
	host=models.CharField(max_length=10)
	sub=models.CharField(max_length=30)
	email=models.EmailField()
	
class News(models.Model):
	title=models.CharField(max_length=40)
	subtitle=models.CharField(max_length=60)
	timestamp=models.CharField(max_length=15)
	text=models.TextField()
	author=models.CharField(max_length=40)
	image1=models.CharField(max_length=40)
	style1=models.CharField(max_length=30)
	image2=models.CharField(max_length=40)
	style2=models.CharField(max_length=30)
	image3=models.CharField(max_length=40)
	style3=models.CharField(max_length=30)
	url=models.URLField()
	email=models.EmailField()
	
class Activity(models.Model):
	title=models.CharField(max_length=40)
	timestamp=models.CharField(max_length=15)
	introduction=models.TextField()
	image=models.CharField(max_length=40)
	style=models.CharField(max_length=30)
	url=models.URLField()
	host=models.CharField(max_length=20)
	undertake=models.CharField(max_length=40)
	email=models.EmailField()
	
class Resource(models.Model):
	name=models.CharField(max_length=20)
	url=models.URLField()
	style=models.CharField(max_length=10)
	type=models.CharField(max_length=10)