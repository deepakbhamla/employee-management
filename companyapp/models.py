from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 

# Create your models here.
class Company(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=99, null=True, blank=True)
    founder_name = models.CharField(max_length=99, null=True, blank=True)
    refrence_number = models.CharField(max_length=99, null=True, blank=True)
    address = models.CharField(max_length=99, null=True, blank=True)
    is_working = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_fund_raise = models.CharField(max_length=99, null=True, blank=True)
    slug = models.CharField(max_length=130)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super(Company, self).save(*args, **kwargs)    

    def __str__(self):
        return self.company_name


class Employee(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=99, null=True, blank=True)
    last_name = models.CharField(max_length=99, null=True, blank=True)
    address = models.CharField(max_length=99, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee')
    experiance = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return self.first_name
