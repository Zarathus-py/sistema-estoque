from django.urls import path
from . import views

urlpatterns = [
    path('relatorios/', views.relatorio_estoque, name='relatorios'),  # Corrigido
    path('produtos/', views.produto_list_view, name='produto_list'),
    path('produtos/novo/', views.produto_create_view, name='produto_create'),
    path('produtos/editar/<int:pk>/', views.produto_update_view, name='produto_update'),
    path('produtos/excluir/<int:pk>/', views.produto_delete_view, name='produto_delete'),

    path('movimentacoes/', views.movimentacao_list_view, name='movimentacao_list'),
    path('movimentacoes/novo/', views.movimentacao_create_view, name='movimentacao_create'),
    path('movimentacoes/editar/<int:pk>/', views.movimentacao_update_view, name='movimentacao_update'),
    path('movimentacoes/excluir/<int:pk>/', views.movimentacao_delete_view, name='movimentacao_delete'),
]
