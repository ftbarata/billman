from billman.services_crud.formatters import decimal_to_brz
from django.core.management.base import BaseCommand
from billman.core.send_mail import send_unique_email
from billman.billing_control.models import ScheduledPrice
from django.utils import timezone
from billman.services_crud.models import CustomerDetails


class Command(BaseCommand):
    help = 'Sends bill mail alerts and/or the bill itself'

    def add_arguments(self, parser):

        parser.add_argument(
            '--subject',
            help='Subject of the mail'
        )

        parser.add_argument(
            '--body',
            help='Body content of the mail'
        )

        parser.add_argument(
            '--recipient',
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
        for customer in CustomerDetails.objects.all():
            if timezone.localdate().day == customer.billing_send_date:

                if customer.services.all().exists():
                    mail_body = 'Serviços contratados: \n\n'
                    total = 0
                    for service in customer.services.all():
                        count = service.count
                        unit_price = decimal_to_brz(service.unit_price)
                        total += unit_price * count
                        mail_body += '* ' + service.description + '.  (Quantidade: {}'.format(count) + ' / Valor unitário: {})\n'.format(unit_price)
                    mail_body += '\nTotal: {}'.format(total)
                    duedate = customer.billing_due_date
                    self.stdout.write('Enviado para: {}'.format(customer.email))
                    send_unique_email('Lembrete de cobrança', mail_body, customer.email)

            if ScheduledPrice.objects.filter(customer=customer).exists():
                ScheduleInstance = ScheduledPrice.objects.get(customer=customer)
                if timezone.localdate().day == ScheduleInstance.send_date.day:
                    description = ScheduleInstance.description
                    unit_price = decimal_to_brz(ScheduleInstance.unit_price)
                    count = ScheduleInstance.count
                    attach_bill = ScheduleInstance.attach_bill
                    duedate = ScheduleInstance.duedate
                    email = ScheduleInstance.customer.email
                    mail_body = 'Esta é uma cobrança avulsa agendada do seguinte serviço:\n\n{}, Valor unitário: {}, Quantidade: {}\n\nTotal: {}\n\n Vencimento: {}'.format(description, unit_price, count, count* unit_price, duedate)
                    self.stdout.write('Enviado para: {}'.format(email))
                    send_unique_email('Lembrete de cobrança avulsa', mail_body, email)