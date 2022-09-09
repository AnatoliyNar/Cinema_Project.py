from django.db import models
from django.urls import reverse
import uuid
from django.contrib import admin
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр фильма:")

def __str__(self):
    return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    synopsis = models.TextField(max_length=1000, help_text="Введите краткое описание фильма:")
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр этого фильма:")

def __str__(self):
    return self.title


def get_absolute_url(self):
    return reverse('movie-detail', args=[str(self.id)])

class MovieInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный id для этого конкретного фильма во всём прокате")
    movie = models.ForeignKey('Movie', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    LOAN_STATUS = (
        ('Н', 'Нет наличии'),
        ('В', 'Взят'),
        ('Д', 'Доступен'),
        ('З', 'Зарезервирован'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='Д', help_text='Доступность фильмов')

@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False

class Meta:
    ordering = ["due_back"]
    permissions = (("can_mark_returned", "Set movie as returned"),)


def __str__(self):
    return '%s (%s)' % (self.id,self.movie.title)

class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Мёртв', null=True, blank=True)

def get_absolute_url(self):
    return reverse('director-detail', args=[str(self.id)])

def __str__(self):
    return '%s, %s' % (self.last_name, self.first_name)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

def display_genre(self):
    return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
display_genre.short_description = 'Genre'

class MoviesInstanceInline(admin.TabularInline):
    model = MovieInstance



def movie_detail_view(request,pk):
    try:
        movie_id=Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        raise Http404("Нет такого фильма")
    return render(
        request,
        'catalog/movie_detail.html',
        context={'movie':movie_id,}
    )

class Meta:
    ordering = ['last_name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [MoviesInstanceInline]

