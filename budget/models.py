from django.db import models
from budget.choices import STATUS, PENDING
from user.models import User
# Create your models here.

MAX_UUID = 30


class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BudgetQuerySet(models.QuerySet):
    def has_uuid(self, uuid):
        return False if self.filter(uuid=uuid) else True


class BudgetManager(models.Manager):
    def get_queryset(self):
        return BudgetQuerySet(self.model, using=self._db)

    def has_uuid(self, uuid):
        return self.get_queryset().has_uuid(uuid)


class Budget(models.Model):

    uuid = models.CharField(max_length=MAX_UUID, blank=False, unique=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=False)
    category = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default=PENDING)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = BudgetManager()

    @classmethod
    def get_new_uuid(self):
        import random, string

        uuid = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(MAX_UUID)])
        if self.objects.has_uuid(uuid):
            return uuid
        else:
            from django.utils.translation import ugettext_lazy as _
            raise ValueError(_("Exist budget with this uuid"))