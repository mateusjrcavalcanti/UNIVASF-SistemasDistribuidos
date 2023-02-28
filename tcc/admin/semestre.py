from django.contrib import admin
from tcc.models import Semestre


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Geral", {"fields": ("curso", "ano", "numero", "coordenador"),
         "description": "General Semestre fields"}),
        ("Datas", {"fields": ("reuniaoInicial", "confirmacaoMatricula", "homologacaoAnteprojeto", "resultadosAnteprojeto", "formularioAcompanhamento",
         "definicaoBanca", "homologacaoBanca", "inicioDefesas", "fimDefesas", "envio", "publicacaoUm", "publicacaoDois")}),
    )

    list_display = ("__str__", "curso",)
    readonly_fields = ("__str__",)
    list_per_page = 20
    list_max_show_all = 100
    save_as = True
    save_on_top = True

    actions_on_bottom = True

    # Order the sections within the change form
    jazzmin_section_order = ("Geral", "Datas")
