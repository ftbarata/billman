from django.db import models
from billman.services_crud.models import CustomerDetails, Service


class BillingControl(models.Model):
    customer = models.ForeignKey(CustomerDetails, verbose_name='Cliente')
    service = models.ForeignKey(Service, verbose_name='Serviço', on_delete=models.CASCADE)
    attach_bill = models.BooleanField(default=False, verbose_name='Gerar boleto')
    active = models.BooleanField(verbose_name='Ativo', default=False)
    send_montly_day = models.DateField('Data de envio')
    duedate = models.DateField('Vencimento')
    paid = models.BooleanField(verbose_name='Pago', default=False)

    class Meta:
        verbose_name = 'Controle de Cobrança'
        verbose_name_plural = 'Controles de Cobrança'

    def __str__(self):
        return self.customer.email + ' - ' + self.service.description


class ScheduledPrice(models.Model):
    customer = models.ForeignKey(CustomerDetails, verbose_name='Cliente')
    send_date = models.DateField('Data de envio')
    duedate = models.DateField('Vencimento')
    description = models.CharField('Descrição', max_length=500)
    unit_price = models.FloatField('Valor unitário', null=True, blank=True)
    count = models.IntegerField('Quantidade', null=True, blank=True)
    attach_bill = models.BooleanField(default=False, verbose_name='Gerar boleto')

    class Meta:
        verbose_name = 'Agendamento de Cobrança'
        verbose_name_plural = 'Agendamentos de Cobranças'

    def __str__(self):
        return self.customer.email + ' - ' + self.description


class BillingHistory(models.Model):
    customer = models.ForeignKey(CustomerDetails, verbose_name='Cliente')
    description = models.CharField('Descrição', max_length=500)
    value = models.FloatField('Valor', null=True, blank=True)
    date = models.DateField('Data', null=True, blank=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-updated_at']