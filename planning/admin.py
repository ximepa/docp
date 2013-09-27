from django.contrib import admin
from .models import PlanningConnections

class PlanningConnectionsAdmin(admin.ModelAdmin):
    list_filter = ['vyl',]
    save_on_top = True
    search_fields = ['vyl',]
    #class Media:
    ##    css = {
    ##        "all": ("my_styles.css",)
    ##    }
    #    js = ("js/filter.js",)

admin.site.register(PlanningConnections, PlanningConnectionsAdmin)