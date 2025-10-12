from django.contrib import admin
from .models import House, HouseImage

class HouseImageInline(admin.TabularInline):  # or StackedInline
    model = HouseImage
    extra = 1

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    inlines = [HouseImageInline]

admin.site.register(HouseImage)

