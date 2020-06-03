### based on https://github.com/pretalx/pretalx/blob/master/src/pretalx/common/management/commands/shell_scoped.py

from contextlib import suppress

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_scopes import scope, scopes_disabled


class Command(BaseCommand):  # pragma: no cover
    help = "Run shell or shell_plus with scopes_disabled."

    def create_parser(self, *args, **kwargs):
        parser = super().create_parser(*args, **kwargs)

        def parse_args(args):
            return parser.parse_known_args(args)[0]

        parser.parse_args = parse_args
        return parser

    def handle(self, *args, **options):
        options.pop("skip_checks", None)
        with scopes_disabled():
            self.stdout.write(
                self.style.SUCCESS(
                    "All scopes are disabled for this shell session – please be careful!"
                )
            )
            return self.call_command(*args, **options)

    def call_command(self, *args, **options):
        with suppress(ImportError):
            import django_extensions  # noqa

            return call_command("shell_plus", *args, **options)
        return call_command("shell", *args, **options)
