from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api", views.basic_graph, name="api"),
    path("wordcloud", views.wordcloud, name="api"),
]