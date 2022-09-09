from django.urls import path
from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^movies/$', views.MovieListView.as_view(), name='movies'),
    re_path(r'^movie/(?P<pk>\d+)$', views.MovieDetailView.as_view(), name='movie-detail'),
]

urlpatterns += [
    re_path(r'^mymovies/$', views.LoanedMoviesByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    re_path(r'^movie/(?P<pk>[-\w]+)/renew/$', views.renew_movie_librarian, name='renew-movie-librarian'),
]

urlpatterns += [
    re_path(r'^director/create/$', views.DirectorCreate.as_view(), name='director_create'),
    re_path(r'^director/(?P<pk>\d+)/update/$', views.DirectorUpdate.as_view(), name='director_update'),
    re_path(r'^director/(?P<pk>\d+)/delete/$', views.DirectorDelete.as_view(), name='director_delete'),
]