from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Occasion(models.Model):
    name=models.CharField(max_length=200,unique=True)


    def __str__(self) -> str:
        return self.name
    
class Cake(models.Model):
    name=models.CharField(max_length=200)
    weight=models.CharField(max_length=200) 
    occasion=models.ForeignKey(Occasion,on_delete=models.CASCADE) 
    options=(
        ("round","round"),
        ("square","square"),
        ("heart","heart")
    ) 
    shape=models.CharField(max_length=200,choices=options,default="round")
    layeroptions=(
        ('1','1'),
        ("2","2"),
        ("3","3")
    )
    layers=models.CharField(max_length=200,choices=layeroptions,default=1)
    price=models.FloatField()
    image=models.ImageField(upload_to="images",blank=True,null=True)

    @property
    def reviews(self):
        return Review.objects.filter(cake=self)
    

    def __str__(self) -> str:
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=200)
    matter=models.CharField(max_length=200)


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    comment=models.TextField(max_length=200)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    

    def __str__(self) -> str:
        return self.comment