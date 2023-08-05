from django.db import models

# Create your models here.


class Category(models.Model):
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category", blank=True, null=True)

    def __str__(self) -> str:
        return self.name