import uuid as uuid

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from djmoney.models.fields import MoneyField

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    slug = models.SlugField(unique=True, max_length=50, allow_unicode=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class DealManager(models.Manager):
    def get_hot_deal(self, hot_result):
        voting = F('vote_up') - F('vote_down')
        hot_deals = Deal.objects.annotate(rate=voting).filter(
            rate__gte=hot_result,
        )
        return hot_deals


class Deal(models.Model):
    objects = models.Manager()
    deal_mgr = DealManager()
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    active = models.BooleanField(default=True, blank=False, null=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    promo_code = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=140, db_index=True)
    description = models.TextField(max_length=5000)
    link = models.URLField()
    product_img = models.ImageField(upload_to='deals_photo')

    current_price = MoneyField(max_digits=19, decimal_places=2, default_currency='PLN', default=0)
    historical_price = MoneyField(max_digits=19, decimal_places=2, default_currency='PLN',
                                  null=True, blank=True, default=0)
    delivery_cost = MoneyField(max_digits=19, decimal_places=2, default_currency='PLN',
                               null=True, blank=True, default=0)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    valid_till = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    vote_up = models.IntegerField(default=0)
    vote_down = models.IntegerField(default=0)

    @property
    def current_price_format(self):
        if self.current_price.currency.code == 'PLN':
            money_format = f'{self.current_price.amount} zł'
        else:
            money_format = f'{self.current_price.currency}{self.current_price.amount}'
        return money_format

    @property
    def historical_price_format(self):
        if self.historical_price.currency.code == 'PLN':
            money_format = f'{self.historical_price.amount} zł'
        else:
            money_format = f'{self.historical_price.currency}{self.historical_price.amount}'
        return money_format

    def price_percentage(self):
        return (1 - self.current_price.amount / self.historical_price.amount) \
               * 100 if self.historical_price.amount > 0 else 0

    def get_absolute_url(self):
        return reverse("deals:detail", args=[str(self.id)])

    def get_voting_count(self):
        return self.vote_up - self.vote_down

    def can_vote(self, user_id):
        user_voted = Vote.objects.filter(Q(user_id=user_id) & Q(deal_id=self.id))
        if user_voted:
            return True
        else:
            return False

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.vote_up < 0:
            self.vote_up = 0
        if self.vote_down < 0:
            self.vote_down = 0

        super(Deal, self).save(*args, **kwargs)


class Comment(models.Model):
    author: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.first_name if self.author.first_name else self.author.username


class Vote(models.Model):
    class VoteChoice(models.IntegerChoices):
        PLUS = 1
        MINUS = -1
        NEUTRAL = 0

    created_at = models.DateTimeField(auto_now_add=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, db_index=True)
    user: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    vote_value: VoteChoice = models.IntegerField(choices=VoteChoice.choices)

    def save(self, *args, **kwargs):
        vote_deal = Deal.objects.get(id=self.deal.id)
        if self.vote_value == 1:
            vote_deal.vote_up += 1
            vote_deal.save(update_fields=['vote_up'])
        if self.vote_value == -1:
            vote_deal.vote_down += 1
            vote_deal.save(update_fields=['vote_down'])
        super(Vote, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        vote_deal = Deal.objects.get(id=self.deal.id)
        if self.vote_value == 1:
            vote_deal.vote_up -= 1
            vote_deal.save()
        if self.vote_value == -1:
            vote_deal.vote_down -= 1
            vote_deal.save()
        super(Vote, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username
