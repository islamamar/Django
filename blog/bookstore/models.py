from django.db import models 
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    name = models.CharField( max_length=90 , null = True)
    email= models.CharField( max_length=90, null=True)
    phone = models.CharField( max_length=90, null=True) 
    age = models.FloatField(null= True) 
    avatar = models.ImageField(blank=True,null=True,default="person.png")
    date_created = models.DateField( auto_now_add=True , null= True)


    def __str__(self):
        return self.name 

class Book (models.Model): 
    CATEGORY = (
        ("Fiction" , "Fiction "),  
        ("Mystery" , "Mystery "),  
        ("horror" ,"horror")
    )
    name = models.CharField( max_length=90 , null=True) 
    Author= models.CharField( max_length=90, null = True)
    price = models.FloatField(null= True) 
    category = models.CharField(max_length=90 , null=True, choices=CATEGORY)
    date_created =models.DateField( auto_now_add=True) 

    def __str__(self):
        return self.name   
    
class Tag(models.Model):
    name= models.CharField(max_length=90 , null= True) 
    def __str__(self):
        return self.name  
    
class Order(models.Model): 
    STATUS = (
        ("pending" , "pending "),  
        ("delivered" , "delivered "),  
        ("in Progress" ,"in Progress"),
        ("out of order" , "out of order")
      )
    
    book = models.ForeignKey(Book, on_delete=models.SET_NULL , null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null= True)
    status = models.CharField( max_length=90 ,null= True , choices=STATUS ) 
    tag = models.ManyToManyField(Tag) 
    date_created = models.DateField( auto_now_add=True , null= True)


