from django.core.management.base import BaseCommand
from billman.core.send_mail import send_unique_email


class Command(BaseCommand):
    help = 'Sends bill mail alerts and/or the bill itself'

    def add_arguments(self, parser):

        parser.add_argument(
            'subject',
            help='Subject of the mail'
        )

        parser.add_argument(
            'body',
            help='Body content of the mail'
        )

        parser.add_argument(
            'recipient',
            help='recipient of the mail'
        )

        parser.add_argument(
            '--mail_only',
            action='store_true',
            default=False,
            help='Sends the billing mail WITHOUT the bill itself'
        )

        parser.add_argument(
            '--html_template',
            help='Optional html template for text/html alternative version mail',
            metavar='app_name/path/template_name'
        )

    def handle(self, *args, **options):
        # self.stdout.write('options used: {}'.format(options))
        send_unique_email(options['subject'], options['body'], options['recipient'])
