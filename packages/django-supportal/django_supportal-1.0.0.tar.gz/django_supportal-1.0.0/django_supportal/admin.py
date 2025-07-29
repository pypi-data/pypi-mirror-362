from django.contrib import admin

from .models import Business, ChatMessage, ChatSession, Document, VectorChunk


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_at", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "owner__username"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "business", "processed", "created_at"]
    list_filter = ["processed", "created_at", "business"]
    search_fields = ["title", "business__name"]
    readonly_fields = ["processed", "created_at", "updated_at"]


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = [
        "session_id",
        "business",
        "customer_name",
        "created_at",
        "is_active",
    ]
    list_filter = ["is_active", "created_at", "business"]
    search_fields = ["session_id", "customer_name", "customer_email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["session", "message_type", "content_preview", "created_at"]
    list_filter = ["message_type", "created_at"]
    search_fields = ["content", "session__session_id"]
    readonly_fields = ["created_at"]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "content"


@admin.register(VectorChunk)
class VectorChunkAdmin(admin.ModelAdmin):
    list_display = ["document", "chunk_index", "content_preview", "created_at"]
    list_filter = ["created_at", "document__business"]
    search_fields = ["content", "document__title"]
    readonly_fields = ["created_at"]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "content"
