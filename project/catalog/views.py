from django.shortcuts import render
from .models import Movie, Director, MovieInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    num_movies=Movie.objects.all().count()
    num_instances=MovieInstance.objects.all().count()
    num_instances_available=MovieInstance.objects.filter(status__exact='Д').count()
    num_directors=Director.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={'num_movies':num_movies,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_directors':num_directors,'num_visits':num_visits},
    )



class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 10

class MovieDetailView(generic.DetailView):
    model = Movie



class LoanedMoviesByUserListView(LoginRequiredMixin,generic.ListView):

    model = MovieInstance
    template_name ='catalog/movieinstance_list_borrowed_user.html'
    paginate_by = 10

def get_queryset(self):
    return MovieInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewMovieForm

@permission_required('catalog.can_mark_returned')
def renew_movie_librarian(request, pk):
    movie_inst = get_object_or_404(MovieInstance, pk=pk)

    if request.method == 'POST':

        form = RenewMovieForm(request.POST)

        if form.is_valid():
            movie_inst.due_back = form.cleaned_data['renewal_date']
            movie_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewMovieForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/movie_renew_librarian.html', {'form': form, 'movieinst':movie_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Director

class DirectorCreate(CreateView):
    model = Director
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}

class DirectorUpdate(UpdateView):
    model = Director
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class DirectorDelete(DeleteView):
    model = Director
    success_url = reverse_lazy('directors')