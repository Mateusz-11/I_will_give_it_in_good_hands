from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Kategorie"


TYPE_INSTITUTION = (
   (1, "Fundacja"),
   (2, "Organizacja pozarządowa"),
   (3, "Zbiórka lokalna"),
)

class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE_INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Instytucje"


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=24, blank=True, null=True)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=12)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Darowizny"
