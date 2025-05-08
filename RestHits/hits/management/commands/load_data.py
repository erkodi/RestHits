from django.core.management.base import BaseCommand
from django.utils.text import slugify
from hits.models import Artist, Hit


class Command(BaseCommand):
    help = 'Load initial data'

    # punkt wejścia dla django
    def handle(self, *args, **kwargs):
        if Artist.objects.exists() or Hit.objects.exists():
            self.stdout.write(self.style.WARNING('Dane już istnieją - wczytywanie przerwane'))
            return

        # tworzenie obiektów artysty
        artist1 = Artist.objects.create(first_name="Artur", last_name="Artyk")
        artist2 = Artist.objects.create(first_name="Janusz", last_name="Jatuk")
        artist3 = Artist.objects.create(first_name="Zbigniew", last_name="Wolek")

        for i in range(1, 21):
            Hit.objects.create(
                title=f"Hit {i}",
                artist=[artist1, artist2, artist3][i % 3],
                title_url=slugify(f"hit {i}"),
            )

        self.stdout.write(self.style.SUCCESS('Wczytywanie danych początkowych zakończone sukcesem'))
        