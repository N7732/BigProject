from django.db import models

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment of {self.amount} on {self.payment_date}"
class Invoice(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        def __str__(self):
            status = getattr(self.payment, "status", "unknown")
            method = getattr(self.payment, "method", "") or "unknown"
            mtn_tag = " (MTN code 920600)" if "920600" in method else ""
            return f"Invoice {self.invoice_number} for Payment {self.payment.id} - {status}{mtn_tag}"
        
        return f"Invoice {self.invoice_number} for Payment {self.payment.id}"
class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.transaction_id} for Payment {self.payment.id}"
    
class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    refund_id = models.CharField(max_length=100, unique=True)
    refund_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Refund {self.refund_id} for Payment {self.payment.id}"
    
class Subscription(models.Model):
    user = models.CharField(max_length=100)
    plan = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Subscription of {self.user} to {self.plan}"
