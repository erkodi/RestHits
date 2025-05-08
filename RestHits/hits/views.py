from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hit
from .serializers import HitSerializerOne, HitSerializerAll
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


# widok dla listy hitów
class ViewHits(APIView):
    def get(self, request):
        hits = Hit.objects.all().order_by('-created_at')[:20]
        serializer = HitSerializerAll(hits, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['title_url'] = slugify(
            data.get('title', ''))
        serializer = HitSerializerOne(data=data)
    
        if serializer.is_valid():
            instance = serializer.save()
            # Generujemy title_url, jeśli nie zostało podane
            if not instance.title_url:
                instance.title_url = slugify(instance.title)
                instance.save(update_fields=["title_url"])  # Aktualizacja pola title_url
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# widok dla pojedynczego rekordu
class ViewOneHit(APIView):
    def get(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        serializer = HitSerializerOne(hit)
        return Response(serializer.data)

    def put(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        serializer = HitSerializerOne(hit, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.title_url = slugify(instance.title)
            instance.save(update_fields=["title_url"])  # Aktualizacja pola title_url
            return Response(HitSerializerOne(instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        hit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
