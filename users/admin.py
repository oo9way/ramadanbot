from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html

from dtb.settings import DEBUG

from users.models import User, Application, Day
from users.forms import BroadcastForm

from users.tasks import broadcast_message
from tgbot.handlers.broadcast_message.utils import send_one_message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def broadcast(self, request, queryset):
        """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
        user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
        if 'apply' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]

            if DEBUG:  # for test / debug purposes - run in same thread
                for user_id in user_ids:
                    send_one_message(
                        user_id=user_id,
                        text=broadcast_message_text,
                    )
                self.message_user(request, f"Just broadcasted to {len(queryset)} users")
            else:
                broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
                self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")

            return HttpResponseRedirect(request.get_full_path())
        else:
            form = BroadcastForm(initial={'_selected_action': user_ids})
            return render(
                request, "admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
            )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
    "user", "phone", "get_days_count", "payment_type", "is_approved", "show_payment_check_url", "created_at",)
    list_display_links = ("user",)
    list_filter = ("payment_type",)
    search_fields = ("user",)
    ordering = ("is_approved",)
    readonly_fields = ("user", "phone", "payment_type", "payment_check_url", "days", "phone2", "order_type",)

    def show_payment_check_url(self, obj):
        if obj.payment_check_url:
            return format_html(f'<a href="{obj.payment_check_url}" target="_blank">Check Photo</a>')
        else:
            return "No photo"


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("day", "get_onsite_users_count", "get_takeaway_users_count")
    ordering = ("day",)

    fieldsets = (
        ('Details', {
            'fields': ('day', 'get_onsite_users', 'get_takeaway_users',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
