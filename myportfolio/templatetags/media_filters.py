from django import template

register = template.Library()


@register.filter
def is_video(url):
    return url.lower().endswith(".mp4")
