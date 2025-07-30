from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str, help="App label for the CustomUser model")

    def reset_sequence(self, model_class):
        """Reset the sequence counter for the model's primary key"""
        if connection.vendor == "postgresql":
            # For PostgreSQL
            table_name = model_class._meta.db_table
            pk_field = model_class._meta.pk.column
            with connection.cursor() as cursor:
                sql = (
                    f"SELECT setval(pg_get_serial_sequence('{table_name}', '{pk_field}'), "
                    f"COALESCE(MAX({pk_field}), 1)) FROM {table_name};"
                )
                cursor.execute(sql)
        elif connection.vendor == "sqlite":
            # For SQLite
            table_name = model_class._meta.db_table
            with connection.cursor() as cursor:
                sql = (
                    f"UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM {table_name}) "
                    f"WHERE name = '{table_name}';"
                )
                cursor.execute(sql)
        elif connection.vendor == "mysql":
            # For MySQL
            table_name = model_class._meta.db_table
            with connection.cursor() as cursor:
                sql = (
                    f"ALTER TABLE {table_name} AUTO_INCREMENT = "
                    f"(SELECT MAX(id) + 1 FROM (SELECT * FROM {table_name}) AS temp);"
                )
                cursor.execute(sql)
        else:
            self.stdout.write(
                self.style.WARNING(f"Sequence reset not implemented for {connection.vendor}")
            )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any):
        app_label = options["app_label"]
        from django.contrib.auth.models import User

        import bigtrill_settings as settings

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

        # Reset the sequence counter after bulk_create with manual primary keys
        self.reset_sequence(CustomUser)

        # Copy groups and permissions after bulk_create
        for user in users:
            try:
                custom_user = CustomUser.objects.get(username=user.username)
                for m2m_field in m2m_fieldnames:
                    getattr(custom_user, m2m_field).set(getattr(user, m2m_field).all())
                custom_user.groups.set(user.groups.all())
            except CustomUser.DoesNotExist:
                pass

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully copied users from User to {CustomUser._meta.label} and reset database sequence."
            )  # noqa
        )
