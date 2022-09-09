from django.contrib import admin
from .models import Director, Genre, Movie, MovieInstance, DirectorAdmin
import uuid


#admin.site.register(Movie)
admin.site.register(Genre)
# admin.site.register(Director)
# admin.site.register(MovieInstance)
admin.site.register(Director, DirectorAdmin)




@admin.register(MovieInstance)
class MovieInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('movie', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

