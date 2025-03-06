from django import template

register = template.Library()

@register.inclusion_tag('includes/card.html')
def card(img_url, title, descr, file_url):
    return {'img_url': img_url, 'title': title, 'descr': descr, 'file_url': file_url}
