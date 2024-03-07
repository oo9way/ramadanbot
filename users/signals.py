from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Day
from datetime import datetime

from .utils import send_message


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
                days = set(x.strip() for x in instance.days.replace("}", "").replace("{", "").replace("'", "").split(","))
            except:
                days = set(instance.days)

            for date in days:
                try:
                    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                    day_data = Day.objects.get(day=parsed_date)
                    day_data.users.remove(instance.user)
                except Exception as e:
                    print(e)
