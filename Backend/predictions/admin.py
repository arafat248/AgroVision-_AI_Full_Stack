from django.contrib import admin

from .models import PredictionHistory


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "predicted_crop", "confidence_score", "risk_level", "created_at")
    search_fields = ("user__email", "predicted_crop", "risk_level")
    list_filter = ("risk_level", "created_at")
    ordering = ("-created_at",)
