from datetime import datetime
import os
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.dispatch import receiver
from django.core.mail import send_mail




class UserAccountManager(BaseUserManager):
  
  def create_user(self, first_name, last_name,phone_number, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    email = self.normalize_email(email)
    email = email.lower()

    user = self.model(
      first_name=first_name,
      last_name=last_name,
      phone_number=phone_number,
      email=email,
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_superuser(self, first_name,last_name,phone_number,  email, password=None):
    user = self.create_user(
      first_name,
      last_name,
      phone_number,
      email,
      password=password,
    )

    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user


# class PremiumSubscription(models.Model):
#   user                     = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
#   plan                     = models.ForeignKey(Prime,on_delete=models.CASCADE,blank=True,null=True)
#   payment                  = models.FloatField(default=00.0)
#   payment_id               = models.CharField(null=True,blank=True,max_length=500)
#   created_at               = models.DateTimeField(null=True, blank=True)
#   unique_id                = models.CharField(null=True,max_length=100,blank=True)
#   slug                     = models.SlugField(max_length=500,unique=True,blank=True,null=True)

#   def __str__(self):
#     return self.user
#   def save(self, *args, **kwargs):
#     if self.created_at is None:
#       self.created_at      = timezone.localtime(timezone.now())
#     if self.unique_id is None:
#       self.unique_id       = str(uuid.uuid4()).split('-')[4]
#     self.slug = slugify('{} {}'.format(self.plan,self.payment_id))
#     super(PremiumSubscription, self).save(*args, **kwargs)    


class UserAccount(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True, max_length=255)
  phone_number = PhoneNumberField(max_length=17, unique=True)
  wordCount = models.IntegerField(blank=True,null=True)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  image_url = models.URLField(blank=True,null=True,max_length=300)
  is_staff = models.BooleanField(default=False,blank=True,null=True)
  premium = models.BooleanField(default=False,blank=True,null=True)
  subscriptionType = models.CharField(default ='Free Trail',max_length=150,blank=True,null=True)
  monthlyCount = models.IntegerField(default=20000)
  email_otp = models.IntegerField(blank=True,null=True)
  email_verified = models.BooleanField(default=False,null=True)
  approve = models.BooleanField(default=True,null=True)

  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name','phone_number']

  def __str__(self):
    return self.email
  
  @property
  def countChecker(self):
    if self.wordCount > self.monthlyCount:
      self.approve = False
    return self.approve
  


  


class BlogCollection(models.Model):
  title = models.CharField(max_length=255,null=True)
  blog = models.CharField(blank=True,max_length=2000,null=True)
  keywords = models.CharField(blank=True,max_length=300,null=True)
  audience = models.CharField(blank=True,max_length=300,null=True)
  accuracy = models.IntegerField(blank=True,null=True)
  wordCount = models.IntegerField(blank=True,default=0)
  user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)

  unique_id=models.CharField(null=True,max_length=100,blank=True, )
  slug = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  date_created = models.DateTimeField(null=True,blank=True)
  last_updated = models.DateTimeField(null=True,blank=True)


  def __str__(self):
    return '{} {}'.format(self.title,self.unique_id)
  
  def save(self, *args, **kwargs):
    if self.date_created is None:
      self.date_created = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id = str(uuid.uuid4()).split('-')[4]
    
    self.slug = slugify('{} {}'.format(self.title,self.unique_id))
    self.last_updated = timezone.localtime(timezone.now())
    super(BlogCollection, self).save(*args, **kwargs)
  


class BlogIdea(models.Model):
  title = models.CharField(max_length=255,null=True)
  blog_ideas = models.CharField(blank=True,max_length=300,null=True)
  keywords = models.CharField(blank=True,max_length=300,null=True)
  audience = models.CharField(blank=True,max_length=300,null=True)
  wordCount = models.IntegerField(blank=True,null=True,default=0)
  user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)

  unique_id=models.CharField(null=True,max_length=100,blank=True)
  slug = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  date_created = models.DateTimeField(null=True,blank=True)
  last_updated = models.DateTimeField(null=True,blank=True)


  def __str__(self):
    return '{} {}'.format(self.title,self.unique_id)
  
  def save(self, *args, **kwargs):
    if self.date_created is None:
      self.date_created = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id = str(uuid.uuid4()).split('-')[4]
    
    self.slug = slugify('{} {}'.format(self.title,self.unique_id))
    self.last_updated = timezone.localtime(timezone.now())
    super(BlogIdea, self).save(*args, **kwargs)




class BlogSection(models.Model):
  title = models.CharField(max_length=255)
  body = models.TextField(blank=True,null=True)
  blog = models.ForeignKey(BlogIdea,on_delete=models.CASCADE)
  wordCount = models.IntegerField(blank=True,default=0)
  user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
  unique_id=models.CharField(null=True,max_length=100,blank=True)
  slug = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  date_created = models.DateTimeField(null=True,blank=True)
  last_updated = models.DateTimeField(null=True,blank=True)

  def __str__(self):
    return '{} {}'.format(self.title,self.unique_id)
  
  def save(self, *args, **kwargs):
    if self.date_created is None:
      self.date_created = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id = str(uuid.uuid4()).split('-')[4]
    
    self.slug = slugify('{} {}'.format(self.title,self.unique_id))
    self.last_updated = timezone.localtime(timezone.now())
    super(BlogSection, self).save(*args, **kwargs)
  


class BlogIdeaSave(models.Model):
  title                   = models.CharField(max_length=255,null=True)
  blog_ideas              = models.CharField(blank=True,max_length=300,null=True)
  keywords                = models.CharField(blank=True,max_length=300,null=True)
  audience                = models.CharField(blank=True,max_length=300,null=True)
  wordCount               = models.IntegerField(default=0)
  user                    = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
  idea                    = models.ForeignKey(BlogIdea, on_delete=models.CASCADE)
  idea_key                = models.CharField(max_length=200)
  unique_id               = models.CharField(null=True,max_length=100,blank=True)
  slug                    = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  date_created            = models.DateTimeField(null=True,blank=True)
  last_updated            = models.DateTimeField(null=True,blank=True)


  def __str__(self):
    return '{} {}'.format(self.title,self.unique_id)
  
  def save(self, *args, **kwargs):
    if self.date_created is None:
      self.date_created   = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id      = str(uuid.uuid4()).split('-')[4]
    
    self.slug             = slugify('{} {}'.format(self.title,self.unique_id))
    self.last_updated     = timezone.localtime(timezone.now())
    super(BlogIdeaSave, self).save(*args, **kwargs)




class StoryDetails(models.Model):
  title                   = models.CharField(max_length=255,null=True)
  story                   = models.CharField(blank=True,max_length=10000,null=True)
  keywords                = models.CharField(blank=True,max_length=300,null=True)
  audience                = models.CharField(blank=True,max_length=300,null=True)
  wordCount               = models.IntegerField(blank=True,default=0)
  accuracy                = models.IntegerField(blank=True,null=True)
  user                    = models.ForeignKey(UserAccount,on_delete=models.CASCADE)

  unique_id               = models.CharField(null=True,max_length=100,blank=True)
  slug                    = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  date_created            = models.DateTimeField(null=True,blank=True)
  last_updated            = models.DateTimeField(null=True,blank=True)


  def __str__(self):
    return '{} {}'.format(self.title,self.unique_id)
  
  def save(self, *args, **kwargs):
    if self.date_created is None:
      self.date_created   = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id      = str(uuid.uuid4()).split('-')[4]
    
    self.slug = slugify('{} {}'.format(self.title,self.unique_id))
    self.last_updated     = timezone.localtime(timezone.now())
    super(StoryDetails, self).save(*args, **kwargs)






class Prime(models.Model):
  prime                   = models.CharField(null=True,max_length=100,blank=True)
  words                   = models.IntegerField(default=20000)
  month                   = models.IntegerField(default=1)
  prize                   = models.FloatField(default=00.0)
  unique_id               = models.CharField(null=True,max_length=100,blank=True)

  def __str__(self) :
    return self.prime
  
  def save(self, *args, **kwargs):
    if self.unique_id is None :
      self.unique_id       = str(uuid.uuid4()).split('-')[4]
    super(Prime, self).save(*args, **kwargs)


class PremiumSubscription(models.Model):
  user                     = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
  plan                     = models.ForeignKey(Prime,on_delete=models.CASCADE,blank=True,null=True)
  payment                  = models.FloatField(default=00.0)
  payment_id               = models.CharField(null=True,blank=True,max_length=500)
  created_at               = models.DateTimeField(null=True, blank=True)
  unique_id                = models.CharField(null=True,max_length=100,blank=True)
  slug                     = models.SlugField(max_length=500,unique=True,blank=True,null=True)
  planName                 = models.CharField(max_length=200,blank=True,null=True)
  month                    = models.IntegerField(null=True, blank=True)
  status                   = models.BooleanField(null=True, blank=True)
  words                    = models.IntegerField(null=True, blank=True)


  def __str__(self):
    return self.user.first_name
  def save(self, *args, **kwargs):
    if self.created_at is None:
      self.created_at      = timezone.localtime(timezone.now())
    if self.unique_id is None:
      self.unique_id       = str(uuid.uuid4()).split('-')[4]
    if self.planName is None:
      self.planName = self.plan.prime
    if self.month is None:
      self.month = self.plan.month
    if self.words is None:
      self.words = self.plan.words
    self.slug = slugify('{} {}'.format(self.plan,self.payment_id))
    super(PremiumSubscription, self).save(*args, **kwargs)    


class CurrentSub(models.Model):
  user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
  premiumPlan = models.ForeignKey(PremiumSubscription,on_delete=models.CASCADE)


  def __str__(self):
    return str(self.premiumPlan.plan)








class OTP(models.Model):
  otp = models.IntegerField(blank=True, null=True)
  # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
  email = models.EmailField(blank=True, null=True)



