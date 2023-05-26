from django.http import HttpResponse
from django.shortcuts import render
from .models import Exemplar
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json

# Create your views here.
def convertQueryResultToJsonList(queryResult):
    return [exemplar.as_json() for exemplar in queryResult]

'''
RF01 Um usuário da biblioteca deve conseguir solicitar a reserva
de um livro
'''
# PUT /catalogo/reserva_exemplar/:id
def reservarExemplar(request, exemplar_id):
    try:
        if request.method == "PUT":
            exemplar = Exemplar.objects.get(id=exemplar_id)
            if(exemplar.reservado == 0):
                exemplar.reservado = 1
                exemplar.save()
                return HttpResponse("Exemplar reservado com sucesso")
            else:
                return HttpResponse('O Exemplar {} já está reservado'.format(exemplar.titulo))
        return HttpResponse("Nenhum exemplar alterado. Verifique se o método HTTP da requisição está como PUT")
    except exemplar.DoesNotExist:
        return HttpResponse("O Exemplar solicitado para reserva não se encontra no catálogo")    

'''
RF02 Um usuário ou bibliotecário da biblioteca deve conseguir
buscar por um Exemplar pelo seu título.
'''
# GET /catalogo/exemplar/titulo?titulo=""
def buscaExemplarByNome(request):
    try:
        titulo_exemplar = request.GET.get('titulo', )
        print(titulo_exemplar)
        exemplares = Exemplar.objects.filter(titulo__contains=titulo_exemplar)[:10]
        lista_exemplares =list(exemplares.values())
        return JsonResponse(lista_exemplares, safe=False)
    except exemplares.DoesNotExist:
        return HttpResponse("Não há nenhuma exemplar no catálogo com o termo de busca solicitado!")  

'''
RF05 Um bibliotecário deve conseguir inserir novos livros no
catálogo da biblioteca. 
'''
# POST /catalogo/criar_exemplar
def criarExemplar(request):
    try:
        if request.method == 'POST':
            dadosExemplar = json.loads(request.body)
            # print(request.body)
            # print(dadosExemplar)
            novoExemplar = Exemplar(
                titulo = dadosExemplar['titulo'].upper(),
                autor = dadosExemplar['autor'].upper(),
                exemplar = "EX." + str(dadosExemplar['exemplar']),
                area = dadosExemplar['area'].upper(),
                reservado = False
            )
            novoExemplar.save()
            return HttpResponse("Novo exemplar de {} criado com sucesso!".format(novoExemplar.titulo))
        return HttpResponse("Nenhum dado de novo cadastro foi recebido!")
    except Exception as error:
        return HttpResponse("Houve um erro ao salvar um novo Exemplar: Caused by {}".format(error.args))

'''
RF06 Um bibliotecário deve conseguir remover um livro do
catálogo da biblioteca.
'''
# DELETE /remover_exemplar/:exemplar_id
def removerExemplar(request, exemplar_id):
    try:
        if request.method == 'DELETE':
            removido = Exemplar.objects.get(id=exemplar_id).delete()
            return HttpResponse("Exemplar removido com sucesso!")
        return HttpResponse("Nenhuma exemplar removido. Verifique se o método HTTP da requisição está como DELETE")
    except removido.DoesNotExist:
        return HttpResponse("Não foi encontrado nenhum exemplar")  

'''
RF07 Um bibliotecário deve acessar uma lista com todos os livros
emprestados.
'''   
# GET /catalogo/examplares_emprestados
def todosExemplaresReservados(request):
    try:
        exemplares = Exemplar.objects.filter(reservado = True).values()
        # lista_exemplares = convertQueryResultToJsonList(exemplares)
        lista_exemplares = list(exemplares)
        return JsonResponse(lista_exemplares, safe=False)
    except Exemplar.DoesNotExist:
        return HttpResponse("Não há nenhum exemplar emprestado no catálogo!")  

# GET /catalogo/exemplar
def allExemplares(request):
    try:
        page = request.GET.get('page', )
        itemsPerPage = request.GET.get('itemsPerPage', 0)
        sortBy = request.GET.get('sortBy', 'titulo')
        lingua = request.GET.get('lingua', '')
        
        # exemplares = list(Exemplar.objects.order_by('titulo').values())
        exemplar_list = Exemplar.objects.order_by(sortBy)
        if lingua != '':
            exemplar_list = exemplar_list.filter(area=lingua.upper())
            
        if page != 0 and itemsPerPage != 0:
            paginator = Paginator(exemplar_list, itemsPerPage)
            page = paginator.get_page(page)
            return JsonResponse({"exemplares":list(page.object_list.values()), 
                                 "totalItems": exemplar_list.count()} , safe=False)
        return JsonResponse(list(exemplar_list.values()), safe=False)
    except Exemplar.DoesNotExist:
        return HttpResponse("Não foi encontrado nenhum exemplar")
    
# GET /catalogo/exemplar/:exemplar_id
def exemplarById(request, exemplar_id):
    try:
        exemplar = Exemplar.objects.get(id=exemplar_id)
        return HttpResponse(json.dumps(exemplar.as_json()), content_type="application/json" )
        # serializedObj = serialize('json', [ exemplar, ])
        # # return JsonResponse(serialized_obj, safe=False)
        # return HttpResponse(serializedObj, content_type="application/json" )
    except exemplar.DoesNotExist:
        return HttpResponse("Não foi encontrado nenhum exemplar")
    
# GET /catalogo/exemplares_por_lingua/:lingua
def exemplarByLingua(lingua):
    try:
        exemplares = Exemplar.objects.filter(area=lingua.upper())
        lista_exemplares = convertQueryResultToJsonList(exemplares)
        return HttpResponse(lista_exemplares)
    except exemplares.DoesNotExist:
        return HttpResponse("Não foi encontrado nenhum exemplar")
    