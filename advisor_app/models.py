from django.db import models
from user_app.models import User
from admin_app.models import Product

class AdvisorClientMapping(models.Model):
    advisor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_advisor')
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_client')

    class Meta:
        db_table = 'advisor_client_mapping'

class ProductLink(models.Model):
    product_link = models.CharField(max_length=50)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_link_client")
    advisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="product_link_advisor")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    

    class Meta:
        db_table = "product_link"
        unique_together = ["client", "product"]