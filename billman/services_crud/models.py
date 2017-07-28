from django.db import models


class Service(models.Model):
    description = models.CharField('Descrição', max_length=500)
    unit_price = models.FloatField('Valor unitário', null=True, blank=True)
    count = models.IntegerField('Quantidade', null=True, blank=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.description


class CustomerDetails(models.Model):
    class Meta:
        verbose_name = 'Detalhe do cliente'
        verbose_name_plural = 'Detalhes do cliente'
    customer_type = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    email = models.EmailField(primary_key=True, max_length=60)
    type = models.CharField('tipo', max_length=2, choices=customer_type)
    name = models.CharField('nome',max_length=100)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    country_abbreviation = models.CharField('País(Sigla)', max_length=2, null=True, blank=True)
    state_abbreviation = models.CharField('Estado(Sigla)', max_length=20, null=True, blank=True)
    city = models.CharField('Cidade', max_length=60, null=True, blank=True)
    full_address = models.CharField('Endereço completo com CEP', max_length=500, null=True, blank=True)
    responsibles = models.CharField('Responsáveis', max_length=300, null=True, blank=True)
    phones = models.CharField('Telefones', max_length=100, blank=True)
    services = models.ManyToManyField('Service', blank=True)

    def __str__(self):
        return self.email


