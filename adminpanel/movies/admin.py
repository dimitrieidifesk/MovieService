from django.contrib import admin

from .models import Movies


@admin.register(Movies)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "rating", "updated_at"]
    list_filter = ["type", "rating", "updated_at"]
