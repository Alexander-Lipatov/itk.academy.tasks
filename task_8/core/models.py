from django.db import models
from django.db import models, transaction
from django.db.models import F

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
        
    def get_queryset(self):
        return self.__class__.objects.filter(id=self.id)

    @transaction.atomic()
    def buy_book(self, count):
        obj = self.get_queryset().select_for_update().get()
        if self.count > 0  and self.count > count:
            obj.count = F('count') - count
            obj.save(update_fields=['count'])
            return True
        return False
        

     
