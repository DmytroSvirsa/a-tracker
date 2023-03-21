from django.urls import path

from amedia_tracker import views
from amedia_tracker.views import TitleListView, mark_episode_as_watched

urlpatterns = [
    path("", TitleListView.as_view(), name="title_list"),
    path("title/<int:pk>/", views.title_detail, name="title_detail"),
    path("episode/", views.episode_detail, name="episode_detail"),
    path(
        "title/<int:pk>/mark-episode-as-watched",
        mark_episode_as_watched,
        name="mark-episode-as-watched",
    ),
]

app_name = "amedia_tracker"
