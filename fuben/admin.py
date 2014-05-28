from django.contrib import admin
from fuben.models import ComicBook, ComicVolume, ComicPage
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_volume', 'des')


admin.site.register(ComicBook, BookAdmin)
admin.site.register(ComicVolume)
admin.site.register(ComicPage)



