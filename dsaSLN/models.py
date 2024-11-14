from django.db import models

# Create your models here.



class DSA(models.Model):

    dsa_registerid=models.CharField(max_length=100)
    dsa_name=models.CharField(max_length=100,null=True)
    dsa_password=models.CharField(max_length=200,null=True,blank=True)


class DSA_Applications(models.Model):
    dsa=models.ForeignKey(DSA, on_delete=models.CASCADE, related_name='dsa',blank=True,null=True)
    cust_applicationId=models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.cust_applicationId}"
    # loan_type=models.CharField(max_length=100,null=True)


class Comission(models.Model):
    con=models.ForeignKey(DSA,on_delete=models.CASCADE,related_name='comission',blank=True)
    application_id=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100,null=True)
    loan_amount=models.CharField(max_length=100,null=True)
    loan_type=models.CharField(max_length=100)
    comissionPercentage=models.CharField(max_length=100,null=True,blank=True)
    comissionAmount=models.CharField(max_length=100)
    disbursedAmount=models.CharField(max_length=100)
    date=models.DateField(null=True)

class DSAPayOut(models.Model):
    payouts=models.ForeignKey(DSA,on_delete=models.CASCADE,related_name='payout',blank=True)
    application_id=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100,null=True)
    loan_amount=models.CharField(max_length=100,null=True)
    loan_type=models.CharField(max_length=100)
    comissionPercentage=models.CharField(max_length=100,null=True,blank=True)
    comissionAmount=models.CharField(max_length=100)
    disbursedAmount=models.CharField(max_length=100)
    date=models.DateField(null=True)


    