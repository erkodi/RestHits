from django.urls import path
from .views import ViewHits, ViewOneHit

urlpatterns = [
    path('hits/', ViewHits.as_view(), name='hits-list'),
    path('hits/<slug:title_url>/', ViewOneHit.as_view(), name='hit-detail'),
]
