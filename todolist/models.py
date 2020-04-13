from django.utils import timezone


from django.db import models

# Create your models here.
class Category(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
       return self.name #name to be shown when called


class Task(models.Model): #Todolist able name that inherits models.Model
   title = models.CharField(max_length=250) # a varchar
   content = models.TextField(blank=True) # a text field
   created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
   due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
   category = models.ForeignKey(Category, default="general", on_delete=models.SET_DEFAULT) # a foreignkey

   class Meta:
       ordering = ["-created"] #ordering by the created field

   def __str__(self):
       return self.title #name to be shown when called

