from options.models import *
from django.contrib import admin


class DomAdmin(admin.ModelAdmin):
    list_filter = ['sorting',]
    save_on_top = True
    search_fields = ['sorting', 'vyl__name', 'house__num']
    class Media:
    #    css = {
    #        "all": ("my_styles.css",)
    #    }
        js = ("js/filter.js",)

class WorkerAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'is_active', 'work_type', 'notebook_ip', 'show_in_graphs',)
    fields = ('name', 'is_active', 'work_type', 'notebook_ip', 'show_in_graphs',)
    class Media:
    #    css = {
    #        "all": ("my_styles.css",)
    #    }
        js = ("js/filter.js",)


class Work_typeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name',)
    fields = ('name',)
    class Media:
    #    css = {
    #        "all": ("my_styles.css",)
    #    }
        js = ("js/filter.js",)


class Claim_typeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name',)
    fields = ('name',)
    class Media:
    #    css = {
    #        "all": ("my_styles.css",)
    #    }
        js = ("js/filter.js",)


class Claims_groupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class PerformedWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Work_type, Work_typeAdmin)
admin.site.register(Claim_type, Claim_typeAdmin)
admin.site.register(Dom, DomAdmin)
admin.site.register(Claims_group, Claims_groupAdmin)
admin.site.register(PerformedWork, PerformedWorkAdmin)
