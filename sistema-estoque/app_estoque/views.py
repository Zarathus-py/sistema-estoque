from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Produto, MovimentacaoEstoque  # MovimentacaoEstoque está correto agora!
from .forms import ProdutoForm, MovimentacaoForm
import json

def relatorio_estoque(request):
    # Buscar os produtos mais movimentados (top 10)
    movimentacoes = (
        MovimentacaoEstoque.objects
        .values('produto__nome')  # Acessando corretamente o nome do produto
        .annotate(total_movimentado=Sum('quantidade'))
        .order_by('-total_movimentado')[:10]
    )
    
    # Buscar estoque atual
    produtos = Produto.objects.all()
    
    # Preparar dados para o gráfico
    grafico_labels = [item['produto__nome'] for item in movimentacoes]
    grafico_valores = [item['total_movimentado'] for item in movimentacoes]
    
    context = {
        'movimentacoes': movimentacoes,
        'produtos': produtos,
        'grafico_labels': json.dumps(grafico_labels),  # JSON serializado corretamente
        'grafico_valores': json.dumps(grafico_valores),
    }
    
    return render(request, 'estoque/relatorio.html', context)

# CRUD de produtos
def produto_list_view(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/produto_list.html', {'produtos': produtos})

def produto_create_view(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('produto_list')
    return render(request, 'estoque/produto_form.html', {'form': form, 'titulo': 'Adicionar Produto'})

def produto_update_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('produto_list')
    return render(request, 'estoque/produto_form.html', {'form': form, 'titulo': 'Editar Produto'})

def produto_delete_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'estoque/produto_confirm_delete.html', {'produto': produto})


def movimentacao_list_view(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto').order_by('-data')
    return render(request, 'estoque/movimentacao_list.html', {'movimentacoes': movimentacoes})

def movimentacao_create_view(request):
    form = MovimentacaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('movimentacao_list')
    return render(request, 'estoque/movimentacao_form.html', {'form': form, 'titulo': 'Registrar Movimentação'})

def movimentacao_update_view(request, pk):
    movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
    form = MovimentacaoForm(request.POST or None, instance=movimentacao)
    if form.is_valid():
        form.save()
        return redirect('movimentacao_list')
    return render(request, 'estoque/movimentacao_form.html', {'form': form, 'titulo': 'Editar Movimentação'})

def movimentacao_delete_view(request, pk):
    movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
    if request.method == 'POST':
        movimentacao.delete()
        return redirect('movimentacao_list')
    return render(request, 'estoque/movimentacao_confirm_delete.html', {'movimentacao': movimentacao})