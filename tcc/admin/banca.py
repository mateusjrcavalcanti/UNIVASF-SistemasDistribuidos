import os
from django.contrib import admin
from django.contrib.staticfiles import finders
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from tcc.models import Banca, Horario, Trabalho

from docx import Document


@admin.register(Banca)
class BancaAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_max_show_all = 100
    save_as = True
    save_on_top = True

    actions_on_bottom = True

    # Order the sections within the change form
    jazzmin_section_order = ("Geral", "Datas")

    def get_queryset(self, request):
        qs = super(BancaAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # return qs.filter(trabalho__discente__id=request.user.id)
        return qs.filter(Q(trabalho__semestre__coordenador__id=request.user.id) | Q(trabalho__discente_id=request.user.id) | Q(trabalho__orientador_id=request.user.id))

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        if (request.user.is_superuser):
            return True
        if (Banca.objects.filter(trabalho__discente__id=request.user.id, trabalho__homologacao_orientador=True, trabalho__homologacao_coordenador=True).count() != Trabalho.objects.filter(discente__id=request.user.id).count()) or (Banca.objects.filter(trabalho__orientador__id=request.user.id, trabalho__homologacao_orientador=True, trabalho__homologacao_coordenador=True).count() != Trabalho.objects.filter(orientador__id=request.user.id).count()):
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "horario":
            if request.resolver_match.kwargs.get('object_id') is not None:
                kwargs["queryset"] = Horario.objects.filter(Q(banca=None) | Q(
                    banca__id=request.resolver_match.kwargs['object_id']))
            else:
                kwargs["queryset"] = Horario.objects.filter(banca=None)

        if db_field.name == "trabalho":
            if request.resolver_match.kwargs.get('object_id') is not None:
                kwargs["queryset"] = Trabalho.objects.filter(Q(discente__id=request.user.id) | Q(orientador__id=request.user.id) | Q(
                    banca__id=request.resolver_match.kwargs['object_id']), Q(homologacao_orientador=True), Q(homologacao_coordenador=True))
            else:
                kwargs["queryset"] = Trabalho.objects.filter(Q(discente__id=request.user.id) | Q(orientador__id=request.user.id), Q(
                    homologacao_orientador=True), Q(homologacao_coordenador=True))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj=None, **kwargs)

        if obj is not None and obj.trabalho is not None and obj.trabalho.banca.horario is not None:
            Dictionary = {
                "::ORIENTADOR::": obj.trabalho.orientador.get_full_name(),
                "::T_ORIENTADOR::": obj.trabalho.orientador.titulo if obj.trabalho.orientador.titulo is not None else '',
                "::TITULO::": f'{obj.trabalho.titulo}',
                "::CANDIDATO::": obj.trabalho.discente.get_full_name(),
                "::DATA::": timezone.localtime(obj.trabalho.banca.horario.data).strftime('%d/%m/%Y') if obj.trabalho.banca.horario.data is not None else '',
                "::HORA::": timezone.localtime(obj.trabalho.banca.horario.data).strftime('%H:%M') if obj.trabalho.banca.horario.data is not None else '',
                "::SEMESTRE::": f'{obj.trabalho.semestre.ano}.{obj.trabalho.semestre.numero}',
                "::CURSO::": f'{obj.trabalho.semestre.curso.nome}',
                "::COORDENADOR::": obj.trabalho.semestre.coordenador.get_full_name(),
                "::ESTAGIO::": "ESTAGIO?",
                "CECOMP": f'{obj.trabalho.semestre.curso.sigla}',
                "Prof. Dr. Jairson Barbosa Rodrigues": f'{obj.trabalho.semestre.coordenador.titulo} {obj.trabalho.semestre.coordenador.get_full_name()}',
            }
            if not os.path.exists(f'{settings.MEDIA_ROOT}/tcc/{obj.trabalho.id}/'):
                os.makedirs(f'{settings.MEDIA_ROOT}/tcc/{obj.trabalho.id}/')
            # Declaração do Orientador
            decOriPath = finders.find(
                'formularios/__Declaração Orientador - Modelo Canônico.docx')
            document = Document(decOriPath)

            for i in Dictionary:
                for p in document.paragraphs:
                    if p.text.find(i) >= 0:
                        p.text = p.text.replace(i, Dictionary[i])

            document.save(
                f'{settings.MEDIA_ROOT}/tcc/{obj.trabalho.id}/Orientador_{obj.trabalho.orientador.get_full_name()}.docx')

            # Declaração dos avaliadores
            for avaliador in obj.avaliadores.all():
                Dictionary.update(
                    {"::T_AVAL::": f'{avaliador.titulo}', "::AVAL::": avaliador.get_full_name(), })
                decOriPath = finders.find(
                    'formularios/__Declaração Avaliador - Modelo Canônico.docx')
                document = Document(decOriPath)
                for i in Dictionary:
                    for p in document.paragraphs:
                        if p.text.find(i) >= 0:
                            p.text = p.text.replace(i, Dictionary[i])
                document.save(
                    f'{settings.MEDIA_ROOT}/tcc/{obj.trabalho.id}/Avaliador_{avaliador.get_full_name()}.docx')

            # Declaração dos avaliadores
            for coorientador in obj.coorientadores.all():
                Dictionary.update(
                    {"::T_COORIENTADOR::": f'{coorientador.titulo}', "::COORIENTADOR::": coorientador.get_full_name(), })
                decOriPath = finders.find(
                    'formularios/__Declaração Coorientador - Modelo Canônico.docx')
                document = Document(decOriPath)
                for i in Dictionary:
                    for p in document.paragraphs:
                        if p.text.find(i) >= 0:
                            p.text = p.text.replace(i, Dictionary[i])
                document.save(
                    f'{settings.MEDIA_ROOT}/tcc/{obj.trabalho.id}/Coorientador_{coorientador.get_full_name()}.docx')
        if obj is None:
            form.base_fields["avaliacoesresult"].disabled = True
            form.base_fields["avaliacoesresult"].widget = forms.HiddenInput()

            form.base_fields["resultado"].disabled = True
            form.base_fields["resultado"].widget = forms.HiddenInput()

            form.base_fields["homologacao_coordenador"].disabled = True
            form.base_fields["homologacao_coordenador"].widget = forms.HiddenInput()

            form.base_fields["homologacao_orientador"].disabled = True
            form.base_fields["homologacao_orientador"].widget = forms.HiddenInput()
        else:
            if (obj.trabalho.discente.id == request.user.id):
                form.base_fields["avaliacoesresult"].disabled = True
                form.base_fields["avaliacoesresult"].widget = forms.HiddenInput()
            if (obj.trabalho.orientador_id != request.user.id and obj.trabalho.discente.id != request.user.id and not request.user.is_superuser):
                form.base_fields["avaliadores"].disabled = True
                form.base_fields["coorientadores"].disabled = True
            if obj.trabalho.orientador_id != request.user.id:
                form.base_fields["homologacao_orientador"].disabled = True
                form.base_fields["resultado"].disabled = True
            if obj.trabalho.semestre.coordenador.id != request.user.id:
                form.base_fields["homologacao_coordenador"].disabled = True

        return form
