from django.contrib import admin
from .models import Payment, Invoice, Transaction, Refund, Subscription

admin.site.register(Payment)
admin.site.register(Invoice) 
admin.site.register(Transaction)
admin.site.register(Refund)
admin.site.register(Subscription)

# Register your models here.
