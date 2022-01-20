# Register your models here.
from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from deals.models import Category
from deals.models import Comment
from deals.models import Deal
from deals.models import Vote


class DealAdminForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = '__all__'

    def clean(self):
        hist_price = self.cleaned_data['historical_price']
        if not hist_price:
            self.cleaned_data['historical_price'] = 0

        if hist_price and hist_price < self.cleaned_data['current_price']:
            raise forms.ValidationError('Current price must be lower than historical price')
        return self.cleaned_data


class DealAdmin(SummernoteModelAdmin):
    form = DealAdminForm
    list_display = ('name', 'created_at', 'vote_up', 'vote_down', 'overall_rating', 'active',)
    summernote_fields = '__all__'

    def overall_rating(self, obj):
        return obj.vote_up - obj.vote_down


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'created_at']


class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'vote_value', 'deal_id', 'created_at', 'id']

    def delete_queryset(self, request, queryset):
        for vote in queryset:
            vote_deal = Deal.objects.get(id=vote.deal_id)
            if vote.vote_value == 1:
                vote_deal.vote_up -= 1
                vote_deal.save(update_fields=['vote_up'])
            if vote.vote_value == -1:
                vote_deal.vote_down -= 1
                vote_deal.save(update_fields=['vote_down'])
        super().delete_queryset(request, queryset)


admin.site.register(Deal, DealAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Category)
