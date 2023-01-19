from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import * 
from .forms import ImaginiAutoForm
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('foto')
class ImaginiAutoInLine(admin.StackedInline):
    model = ImaginiAuto

class DotariAdmin(admin.ModelAdmin):
    model = Dotare
    list_filter = ['categorie_dotari']
    search_fields = ['denumire']

class ImaginiAutoAdminList(ChangeList):
    def get_results(self, request):
        self.result_count = 0
        self.result_list = []
        self.full_result_count = 0
        self.multi_page = False
        self.can_show_all = False
  
class ImaginiAutoAdmin(admin.ModelAdmin):
    model = ImaginiAuto
    add_form_template = 'admin/post_form.html'
    change_form_template = 'admin/post_form.html'

    def get_form(self, request, obj=None, **kwargs):
        try:
            instance = kwargs['instance']
            return ImaginiAutoForm(instance=instance)
        except KeyError:
            return ImaginiAutoForm
    
    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = self.get_form(request)
        return super(ImaginiAutoAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
    
    def get_changelist(self, request):
            return ImaginiAutoAdminList

    def save_model(self, request, obj, form, change):
        bulk_foto_upload = request.FILES.getlist('bulk_foto_upload')
        for picture in sorted(bulk_foto_upload, key=lambda x: x.name):
            ImaginiAuto.objects.create(autovehicul=obj.autovehicul, foto=picture)
        return True



class AutovehiculAdmin(admin.ModelAdmin):
    model = Autovehicul
    list_display = ["titlu","vizibil","vandut","marca","model","versiune","data_adaugare"]
    filter_horizontal = ['dotari']
    readonly_fields  = ['slug','data_adaugare','data_modificare']
    list_filter = ['marca','data_adaugare']
    search_fields = ['titlu', 'marca', 'model','versiune']
    #prepopulated_fields = {"titlu": ("marca__denumire","model","versiune")}
    inlines = [ImaginiAutoInLine]

admin.site.register([
    Companie, 
    Categorie, 
    Marca, 
    Combustibil,
    Transmisie,
    CutieDeViteza, 
    Caroserie, 
    NormaDePoluare, 
    Stare,
    CategorieDotari])

admin.site.register(ImaginiAuto, ImaginiAutoAdmin)
admin.site.register(Dotare, DotariAdmin)
admin.site.register(Autovehicul, AutovehiculAdmin)
