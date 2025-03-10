from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1


class ProductInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = Product
    extra = 1


class ProductComboInline(admin.TabularInline):
    model = ProductCombo
    extra = 1


@admin.register(Category,)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
                'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Store)
class StoreAdmin(TranslationAdmin):
    inlines = [ContactInfoInline, ProductInline, ProductComboInline]

    class Media:
        js = (
                'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(StoreReview)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(CourierReview)
admin.site.register(Cart)
admin.site.register(CarItem)


