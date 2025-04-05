from django.contrib import admin
from .models import Produto, MovimentacaoEstoque

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade', 'data_cadastro')  # Colunas visíveis
    search_fields = ('nome',)  # Campo de busca
    list_filter = ('data_cadastro',)  # Filtro lateral
    ordering = ('-data_cadastro',)  # Ordenação (mais recentes primeiro)


admin.site.register(MovimentacaoEstoque)
