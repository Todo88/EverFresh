from django import template


register = template.Library()


@register.filter()
def get_item(dictionary, key):
    print("lookin in dict with this key:", key)
    print(dictionary.get(str(key)))
    return dictionary.get(str(key))
