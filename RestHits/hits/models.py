from django.db import models


# Tabela Artist
class Artist(models.Model):
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add - dopisanie daty automatycznie prz tworzeniu

    def formatted_created_at(self):  # Czytelna data i godzina
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")


# Tabela Hit
class Hit(models.Model):
    title = models.CharField(max_length=255)
    # przy usunięciu artysty, usunięte też zostaną powiązane utwory
    artist_id = models.ForeignKey(Artist, related_name="hits", on_delete=models.CASCADE)
    title_url = models.SlugField(unique=True)  # dane 'title-url' muszą być unikalne
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add - dopisanie daty automatycznie prz tworzeniu
    updated_at = models.DateTimeField(auto_now=True)  # auto_now - nadpisywanie daty automatycznie prz aktualizowaniu

    def formatted_created_at(self):  # Czytelna data i godzina
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    
    def formatted_updated_at(self):  # Czytelna data i godzina
        return self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
