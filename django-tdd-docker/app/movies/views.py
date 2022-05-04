from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .serializers import MovieSerializer

# All movies
class MovieList(APIView):
    # Define HTTP request method as function name
    def post(self, request, format=None):
        # Serializer takes JSON data and converts to Movie object
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save model with json data
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Return created data as response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Single movie
class MovieDetail(APIView):
    # Helper method for GET - access db object
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    # GET method
    # url: /movies/<int:pk>/
    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)  # Serialize object to JSON
        return Response(serializer.data)
