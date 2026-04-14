from django.contrib import admin
from .models import (
    Stat, Feature, FeatureTag, Skill, SkillItem,
    Tag, Project, ContactMessage, DownloadRequest, Feedback,
)


class FeatureTagInline(admin.TabularInline):
    model = FeatureTag
    extra = 2


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_css_class", "order")
    list_editable = ("order",)
    inlines = [FeatureTagInline]


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "data_count", "order")
    list_editable = ("value", "data_count", "order")


class SkillItemInline(admin.TabularInline):
    model = SkillItem
    extra = 2


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage", "bar_css_class", "order")
    list_editable = ("percentage", "order")
    inlines = [SkillItemInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "is_featured", "order")
    list_editable = ("status", "is_featured", "order")
    list_filter = ("status", "is_featured")
    filter_horizontal = ("tags",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def has_add_permission(self, request):
        return False


class FeedbackInline(admin.StackedInline):
    model = Feedback
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(DownloadRequest)
class DownloadRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "email", "profession", "country",
        "has_contributed", "contribution_amount",
        "created_at", "downloaded_at",
    )
    list_filter = (
        "has_contributed", "profession", "heard_from",
        "country", "accepts_newsletter", "created_at",
    )
    search_fields = ("full_name", "email", "phone", "organization", "country", "city")
    readonly_fields = ("ip_address", "user_agent", "created_at", "downloaded_at")
    inlines = [FeedbackInline]
    fieldsets = (
        ("Identification", {
            "fields": ("full_name", "email", "phone", "profession", "organization"),
        }),
        ("Localisation", {
            "fields": ("country", "city"),
        }),
        ("Contexte", {
            "fields": ("heard_from", "intended_use", "accepts_newsletter"),
        }),
        ("Contribution", {
            "fields": ("has_contributed", "contribution_amount"),
        }),
        ("Telemetrie", {
            "fields": ("ip_address", "user_agent", "created_at", "downloaded_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "email", "rating", "would_recommend",
        "download_request", "created_at",
    )
    list_filter = ("rating", "would_recommend", "created_at")
    search_fields = (
        "full_name", "email",
        "what_liked", "what_to_improve", "features_wanted",
    )
    readonly_fields = ("created_at",)
