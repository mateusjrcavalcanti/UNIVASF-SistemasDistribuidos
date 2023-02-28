from django.contrib import admin
from django.db.models import Q
from tcc.models import Trabalho


@admin.register(Trabalho)
class TrabalhoAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Geral", {"fields": ("titulo", "tipo", "discente", "orientador", "semestre"),
         "description": "General TCC fields"}),
        ("Anteprojeto", {
         "fields": ("anteprojeto", "homologacao_orientador", "homologacao_coordenador")}),
    )

    list_per_page = 20
    list_max_show_all = 100
    save_as = True
    save_on_top = True

    actions_on_bottom = True

    # Order the sections within the change form
    jazzmin_section_order = ("Geral", "Datas")

    def get_queryset(self, request):
        qs = super(TrabalhoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(semestre__coordenador__id=request.user.id) | Q(discente_id=request.user.id) | Q(orientador_id=request.user.id))

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.discente_id != request.user.id and obj.orientador_id != request.user.id and obj.semestre.coordenador_id != request.user.id:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser and obj.semestre.coordenador_id != request.user.id:
            return False
        return True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)

        if obj is None:
            form.base_fields["homologacao_coordenador"].disabled = True
            form.base_fields["homologacao_orientador"].disabled = True
            form.base_fields["anteprojeto"].disabled = True
        else:
            if (not request.user.is_superuser and obj.semestre.coordenador.id != request.user.id) or obj.homologacao_coordenador:
                form.base_fields["semestre"].disabled = True
                form.base_fields["tipo"].disabled = True
            if obj.homologacao_coordenador:
                form.base_fields["titulo"].disabled = True
            if obj.homologacao_orientador or obj.homologacao_coordenador:
                form.base_fields["orientador"].disabled = True
            if obj.orientador_id != request.user.id or obj.titulo is None:
                form.base_fields["homologacao_orientador"].disabled = True
            if obj.semestre.coordenador.id != request.user.id or obj.titulo is None:
                form.base_fields["homologacao_coordenador"].disabled = True
            if (obj.semestre.coordenador.id != request.user.id and not request.user.is_superuser) or obj.homologacao_coordenador:
                form.base_fields["discente"].disabled = True
            if obj.discente.id != request.user.id or obj.homologacao_coordenador or obj.homologacao_orientador:
                form.base_fields["anteprojeto"].disabled = True

        return form
