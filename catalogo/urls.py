from django.urls import path

from . import views

urlpatterns = [
    path("reserva_exemplar/<int:exemplar_id>", views.reservarExemplar, name="reserva-exemplar"),
    path("exemplar", views.allExemplares, name="all-exemplares"),
    path("exemplar/<int:exemplar_id>", views.exemplarById, name="exemplar-byid"),
    path("exemplar/titulo", views.buscaExemplarByNome, name="exemplar-byname"),
    path("criar_exemplar", views.criarExemplar, name="cria-exemplar"),
    path("remover_exemplar/<int:exemplar_id>", views.removerExemplar, name="remover-exemplar"),
    path("exemplares_emprestados", views.todosExemplaresReservados, name="exemplares-emprestados"),
    path("exemplares_por_lingua", views.exemplarByLingua, name="exemplares-por-lingua"),
]