from django.db import models


class BaseModel(models.Model):
    """
    The model to use for all models because it includes date creation and
    a last modified date. Something we want for /all/ models.
    """
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    visits = models.PositiveIntegerField(default=0)


class Organization(BaseModel):
    name = models.CharField(max_length=300)
    email = models.EmailField(blank=True)


class Event(BaseModel):
    name = models.CharField(max_length=300)
    date = models.DateField()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )


class Transaction(BaseModel):
    amount = models.DecimalField(decimal_places=3, max_digits=10)
    method = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )


class Visit(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )




