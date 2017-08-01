import datetime
from django.core.management.base import BaseCommand
from billman.services_crud.formatters import decimal_to_brz
from billman.core.send_mail import send_unique_email
from billman.billing_control.models import BillingControl, ScheduledPrice
from billman.services_crud.models import CustomerDetails, Service


class Command(BaseCommand):
    help = 'Sends bill mail alerts and/or the bill itself'

    def add_arguments(self, parser):

        # parser.add_argument(
        #     'subject',
        #     help='Subject of the mail'
        # )
        #
        # parser.add_argument(
        #     'body',
        #     help='Body content of the mail'
        # )
        #
        # parser.add_argument(
        #     'recipient',
        #     help='recipient of the mail'
        # )

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
        services_unit_price_count_list = []
        # send_unique_email(options['subject'], options['body'], options['recipient'])

        for customer in CustomerDetails.objects.all():
            self.stdout.write('Processando cliente: {} \n'.format(customer.email))

            for bcq_line in BillingControl.objects.all().filter(customer_id=customer.email):
                if bcq_line.send_montly_day.day == datetime.date.today().day:
                    duedate = bcq_line.duedate
                    service_description = bcq_line.service.description
                    unit_price = bcq_line.service.unit_price
                    count = bcq_line.service.count

                    self.stdout.write('{}, Valor unitário: {}, Quantidade: {}, Vencimento: {}'.format(service_description, decimal_to_brz(unit_price), count, duedate))
                    services_unit_price_count_list.append((service_description, decimal_to_brz(unit_price), count, duedate))

            # Test if there are scheduled billings

            for sp_line in ScheduledPrice.objects.all().filter(customer_id=customer.email):
                if sp_line.send_date == datetime.date.today():
                    scheduled_duedate = sp_line.duedate
                    scheduled_description = sp_line.description
                    scheduled_unit_price = sp_line.unit_price
                    scheduled_count = sp_line.count
                    self.stdout.write('{}, Valor unitário: {}, Quantidade: {}, Vencimento: {}'.format(scheduled_description, decimal_to_brz(scheduled_unit_price), scheduled_count, scheduled_duedate))
                    services_unit_price_count_list.append((scheduled_description, decimal_to_brz(scheduled_unit_price), scheduled_count, scheduled_duedate))

