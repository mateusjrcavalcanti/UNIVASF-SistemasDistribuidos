from django.shortcuts import render
from django.core.paginator import Paginator

from tcc.models.trabalho import Trabalho


def index(request):
    tcc_list = Trabalho.objects.all()
    paginator = Paginator(tcc_list, 1)  # Show 1 tccs per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'projetos': page_obj})


# def index(request):
#     return render(
#         request,
#         "index.html",
#         {
#             "title": "Django example",
#             "projetos": Trabalho.objects.all(),
#         },
#     )
