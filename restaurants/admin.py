from django.contrib import admin
from .models import Category, Restaurant, MenuItem, Review, OpeningHours


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    fk_name = 'restaurant'
    extra = 0
    readonly_fields = ['date']


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 7


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'creator', 'category', 'price_range', 'phone', 'average_rating', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'address', 'description', 'creator__username']
    list_filter = ['status', 'price_range', 'category']
    inlines = [MenuItemInline, OpeningHoursInline, ReviewInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'restaurant']
    search_fields = ['name', 'restaurant__name']
    list_filter = ['restaurant']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'stars', 'parent', 'date', 'comment']
    search_fields = ['restaurant__name', 'comment']
    list_filter = ['stars', 'date']


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'day_of_week', 'open_time', 'close_time', 'is_closed']
    list_filter = ['day_of_week', 'is_closed']
    search_fields = ['restaurant__name']
