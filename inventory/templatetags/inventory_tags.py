from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene un valor de un diccionario usando una clave"""
    try:
        return dictionary.get(int(key), 0)
    except (ValueError, TypeError):
        return dictionary.get(str(key), 0) 