from django import template

register = template.Library()


@register.filter
def is_video(file_url):
    if not file_url:
        return False
    return str(file_url).lower().endswith(".mp4")
