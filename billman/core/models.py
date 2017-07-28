from django.db import models


class Contacts(models.Model):
    email = models.EmailField('Usuário', null=True, blank=True)
    contacts = models.TextField('Contatos', null=True, blank=True, max_length=500)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'