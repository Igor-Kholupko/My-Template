from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from custom_auth.models import Group


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

    def add_arguments(self, parser):
        parser.add_argument(
            '%s' % self.UserModel.USERNAME_FIELD,
            default=None,
            help='Specifies the login for the superuser.',
        )

    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]
        try:
            user = self.UserModel.objects.get(**{self.UserModel.USERNAME_FIELD: username})
        except self.UserModel.DoesNotExist:
            raise CommandError("User '%s' doesn't exist." % username)
        try:
            group = Group.objects.get(name="Administrators")
        except Group.DoesNotExist:
            raise CommandError("Administrators group doesn't exist.")
        user.is_staff = True
        user.save()
        user.groups.add(group)
        self.stdout.write("User successfully added to administrators.")
