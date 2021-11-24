# Register your models here.
from django import forms
from django.contrib import admin

from deals.models import Comment
from deals.models import Deal


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


class DealAdmin(admin.ModelAdmin):
    form = DealAdminForm


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'created_at']


admin.site.register(Deal, DealAdmin)
admin.site.register(Comment, CommentAdmin)
