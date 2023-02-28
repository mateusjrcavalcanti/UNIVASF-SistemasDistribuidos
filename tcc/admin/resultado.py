import types
from django import forms
from django.db.models import Q
from django.contrib import admin
from tcc.models import Resultado, User, Banca


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_max_show_all = 100
    save_as = True
    save_on_top = True

    actions_on_bottom = True

    def get_queryset(self, request):
        qs = super(ResultadoAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.groups.filter(name='Discentes').exists():
            return qs.filter(banca__trabalho__discente__id=request.user.id)

        if qs.filter(Q(banca__trabalho__semestre__coordenador__id=request.user.id) | Q(banca__trabalho__orientador_id=request.user.id)).count() > 0:
            return qs.filter(Q(banca__trabalho__semestre__coordenador__id=request.user.id) | Q(banca__trabalho__orientador_id=request.user.id))
        else:
            return qs.filter(Q(banca__avaliadores__id=request.user.id))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "banca":
            if request.resolver_match.kwargs.get('object_id') is not None:
                kwargs["queryset"] = Banca.objects.filter(Q(trabalho__orientador__id=request.user.id) | Q(
                    id=request.resolver_match.kwargs['object_id']), Q(homologacao_orientador=True), Q(homologacao_coordenador=True))
            else:
                kwargs["queryset"] = Banca.objects.filter(Q(trabalho__orientador__id=request.user.id), Q(
                    homologacao_orientador=True), Q(homologacao_coordenador=True))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj=None, **kwargs)

        if obj is not None:
            form.base_fields["banca"].disabled = True

        return form
