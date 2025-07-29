from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str, help="App label for the CustomUser model")

    @transaction.atomic
    def handle(self, *args: Any, **options: Any):
        app_label = options["app_label"]
        from django.contrib.auth.models import User
        from bigtrill import settings

        CustomUser = apps.get_model(app_label, settings.COPY_MODEL)

        users = User.objects.all()
        user_fields = [f for f in User._meta.get_fields() if not isinstance(f, ManyToManyField)]
        m2m_fieldnames = [
            f.name for f in User._meta.get_fields() if isinstance(f, ManyToManyField)
        ]
        custom_users = []
        for user in users:
            field_values = {}
            for field in user_fields:
                if isinstance(field, ForeignObjectRel):
                    continue

                field_name = field.name
                field_values[field_name] = getattr(user, field_name)
            custom_user = CustomUser(**field_values)
            custom_users.append(custom_user)
        CustomUser.objects.bulk_create(custom_users)
        # Copy groups and permissions after bulk_create
        for user in users:
            try:
                custom_user = CustomUser.objects.get(username=user.username)
                for m2m_field in m2m_fieldnames:
                    getattr(custom_user, m2m_field).set(getattr(user, m2m_field).all())
                custom_user.groups.set(user.groups.all())
            except CustomUser.DoesNotExist:
                pass
