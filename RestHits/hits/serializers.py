from rest_framework import serializers
from .models import Hit, Artist


# Serializer dla artysty
class ArtistSerializer(serializers.ModelSerializer):
    # odwołanie do funkcji 'formatted_created_at' w 'models.py' klasa 'Artist'
    created_at = serializers.ReadOnlyField(source='formatted_created_at')
    
    # metadane
    class Meta:
        model = Artist
        fields = ['id', 'first_name', 'last_name', 'created_at']


# Serializer dla widoku ogólnego
class HitSerializerAll(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )
    # odwołanie do funkcji 'formatted_updated_at' w 'models.py' klasa 'Hit'
    updated_at = serializers.ReadOnlyField(source='formatted_updated_at')

    # metadane
    class Meta:
        model = Hit
        fields = ['title', 'artist_id', 'updated_at']


# Serializer dla widoku szczegółowego
class HitSerializerOne(serializers.ModelSerializer):
    # artist_id = ArtistSerializer()
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        write_only=True
    )
    artist = ArtistSerializer(source='artist_id', read_only=True)
    # odwołanie do funkcji 'formatted_created_at' w 'models.py' klasa 'Hit'
    created_at = serializers.ReadOnlyField(source='formatted_created_at')
    # odwołanie do funkcji 'formatted_updated_at' w 'models.py' klasa 'Hit'
    updated_at = serializers.ReadOnlyField(source='formatted_updated_at')
    title_url = serializers.ReadOnlyField()

    # metadane
    class Meta:
        model = Hit
        fields = ['id', 'title', 'artist_id', 'artist', 'title_url', 'created_at', 'updated_at']
