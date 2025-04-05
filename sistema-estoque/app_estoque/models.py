from django.db import models
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    preco = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2)
    quantidade = models.IntegerField("Quantidade em Estoque", default=0)
    valor_total = models.DecimalField("Valor Total", max_digits=12, decimal_places=2, default=0.00)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.preco * self.quantidade
        super().save(*args, **kwargs)

    @property
    def valor_total_formatado(self):
        return f"R${self.valor_total:,.2f}".replace('.', ',').replace(',', '.', 1)

    def __str__(self):
        return self.nome

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'entrada':
            self.produto.quantidade += self.quantidade
        elif self.tipo == 'saida':
            if self.quantidade > self.produto.quantidade:
                raise ValueError("Quantidade de saída maior do que o disponível em estoque.")
            self.produto.quantidade -= self.quantidade

        self.produto.valor_total = self.produto.preco * self.produto.quantidade
        self.produto.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.tipo.title()} de {self.quantidade}x {self.produto.nome}'


    