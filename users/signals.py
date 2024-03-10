from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Day
from datetime import datetime
from .tasks import send_message_to_admin

from .utils import send_message, send_photo

BASE_URL = "http://127.0.0.1:8000/"
ADMIN = 1921103181


@receiver(post_save, sender=Application)
def check_field_on_save(sender, instance, created, **kwargs):
    if not created:
        if instance.is_approved:
            send_message(instance.user.user_id, "Your application is approved")
            days = set(x.strip() for x in instance.days.replace("}", "").replace("{", "").replace("'", "").split(","))
            for date in days:
                try:
                    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                    day_data, _ = Day.objects.get_or_create(day=parsed_date)
                    day_data.users.add(instance.user)
                except Exception as e:
                    print(e)

        elif not instance.is_approved:
            try:
                days = set(
                    x.strip() for x in instance.days.replace("}", "").replace("{", "").replace("'", "").split(","))
            except:
                days = set(instance.days)

            for date in days:
                try:
                    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                    day_data = Day.objects.get(day=parsed_date)
                    day_data.users.remove(instance.user)
                except Exception as e:
                    print(e)

    if instance.payment_check_url and instance._sent_to_admin == False:
        url = BASE_URL + f"users/application/{instance.id}/change/"
        caption = f"New application from {instance.user.first_name} {instance.user.last_name}\n\n"
        caption += f"Phone: {instance.phone}"
        if instance.phone2:
            caption += f", {instance.phone2}\n"
        else:
            caption += "\n"

        caption += f"Payment type: {instance.get_payment_type_display()}"

        try:
            days = set(
                x.strip() for x in instance.days.replace("}", "").replace("{", "").replace("'", "").split(","))
        except:
            days = set(instance.days)

        if days:
            caption += "\nDays:\n"
            caption += '\n'.join(days)

        caption += "\n\n====================="
        caption += "\n Confirm application"
        caption += f"\n{url}"

        with_photo = True

        send_message_to_admin.delay(ADMIN, instance.payment_check_url, caption, instance.id, with_photo)

    if not instance.payment_check_url and instance._sent_to_admin == False and created and instance.payment_type == "cash":
        url = BASE_URL + f"users/application/{instance.id}/change/"
        caption = f"New application from {instance.user.first_name} {instance.user.last_name}\n\n"
        caption += f"Phone: {instance.phone}"
        if instance.phone2:
            caption += f", {instance.phone2}\n"
        else:
            caption += "\n"

        caption += f"Payment type: {instance.get_payment_type_display()}"

        try:
            days = set(
                x.strip() for x in instance.days.replace("}", "").replace("{", "").replace("'", "").split(","))
        except:
            days = set(instance.days)

        print(days)

        if days:
            caption += "\nDays:\n"
            caption += '\n'.join(days)

        caption += "\n\n====================="
        caption += "\n Confirm application"
        caption += f"\n{url}"

        with_photo = False

        send_message_to_admin.delay(ADMIN, instance.payment_check_url, caption, instance.id, with_photo)
