import uuid as uuid

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.urls import reverse

from users.models import CustomUser


class Dealmanager(models.Manager):
    def get_hot_deal(self, hot_result):
        voting = F('vote_up') - F('vote_down')
        hot_deals = Deal.objects.annotate(rate=voting).filter(
            rate__gte=hot_result,
        )
        return hot_deals


class Deal(models.Model):
    objects = models.Manager()
    deal_mgr = Dealmanager()
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=5000)
    link = models.URLField()
    product_img = models.URLField()
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    historical_price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=True, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valid_till = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.CharField(max_length=200, blank=True)

    active = models.BooleanField(default=True, blank=False, null=False)

    vote_up = models.IntegerField(default=0)
    vote_down = models.IntegerField(default=0)

    def price_percentage(self):
        return (1 - self.current_price / self.historical_price) * 100 if self.historical_price > 0 else 0

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
    author: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
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
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
