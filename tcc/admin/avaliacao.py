import types
from django import forms
from django.db.models import Q
from django.contrib import admin
from tcc.models import Avaliacao, User, Banca


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_max_show_all = 100
    save_as = True
    save_on_top = True

    actions_on_bottom = True

    def get_queryset(self, request):
        qs = super(AvaliacaoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # return qs.filter(trabalho__discente__id=request.user.id)
        return qs.filter(Q(banca__trabalho__semestre__coordenador__id=request.user.id) | Q(avaliador_id=request.user.id) | Q(banca__trabalho__orientador_id=request.user.id))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "avaliador":
            if request.resolver_match.kwargs.get('object_id') is not None:
                kwargs["queryset"] = User.objects.filter(Q(id=request.user.id) | Q(
                    id=request.resolver_match.kwargs['object_id']))
            else:
                kwargs["queryset"] = User.objects.filter(
                    id=request.user.id)

        if db_field.name == "banca":
            if request.resolver_match.kwargs.get('object_id') is not None:
                kwargs["queryset"] = Banca.objects.filter(Q(avaliadores__id=request.user.id) | Q(
                    id=request.resolver_match.kwargs['object_id']), Q(homologacao_orientador=True), Q(homologacao_coordenador=True))
            else:
                kwargs["queryset"] = Banca.objects.filter(Q(avaliadores__id=request.user.id), Q(
                    homologacao_orientador=True), Q(homologacao_coordenador=True))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj=None, **kwargs)

        if obj is not None:
            form.base_fields["avaliador"].disabled = True
            form.base_fields["avaliador"].widget = forms.HiddenInput()

            form.base_fields["banca"].disabled = True

            if (obj.avaliador.id != request.user.id):
                form.base_fields["avaliacao"].disabled = True

        return form
