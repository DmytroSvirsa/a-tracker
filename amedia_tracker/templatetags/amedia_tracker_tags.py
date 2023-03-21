from django import template
from django.db.models import QuerySet

from amedia_tracker.parse_animedia import Parser


register = template.Library()


@register.simple_tag
def run_parse():
    parser = Parser()
    parser.get_all_titles()


@register.filter
def get_shorten_name(name):
    return name.split(":")[0].split("!")[0]


@register.filter
def next_episode(episode_number):
    return episode_number + 1
