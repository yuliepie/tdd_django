from rest_framework import serializers

from .models import Movie

# Movie Serializer (ModelSerializer)
# Assign a model to ModelSerializer -> outputs all fields from model
# Can identify read-only fields which will not be modified by the serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_date",
            "updated_date",
        )
