from django.urls import path
from .views import MovieList, MovieDetail


# Match url endpoint to an APIView class (for a model)
urlpatterns = [
    path("api/movies/", MovieList.as_view()),
    path("api/movies/<int:pk>/", MovieDetail.as_view()),
]
