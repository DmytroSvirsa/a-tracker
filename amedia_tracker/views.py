from django.shortcuts import render
from django.views import generic

from amedia_tracker.models import Title, Episode


class TitleListView(generic.ListView):
    model = Title
    # paginate_by = 5


def title_detail(request, pk):
    title = Title.objects.get(id=pk)
    context = {"title": title}
    return render(request, "amedia_tracker/title_detail.html", context)


def episode_detail(request):
    episode = Episode.objects.get(id=request.GET.get("id_episode"))
    context = {"episode": episode}
    return render(request, "partials/episode_detail.html", context)


def mark_episode_as_watched(request, pk):
    title = Title.objects.get(id=pk)
    id_episode = request.GET.get("id_episode")
    episode = Episode.objects.get(id=id_episode)
    title.last_watched_episode = episode.number
    title.save()
    context = {"last_watched_episode": episode.number}
    return render(request, "partials/last_watched_episode.html", context)
