import uuid
from django.db import models


class CompanyRelatedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, editable=False, related_name='%(class)s')

    class Meta:
        abstract = True
