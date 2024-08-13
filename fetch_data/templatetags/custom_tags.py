from django import template

register = template.Library()

@register.simple_tag
def get_class(item):
    """Returns a class name based on item properties."""
    if hasattr(item, 'is_dev') and item.is_dev:
        print("Item is dev")
        return 'dev'
    elif hasattr(item, 'is_favorite') and item.is_favorite:
        print("Item is favorite")
        return 'favorite'
    elif hasattr(item, 'is_favorited_by') and item.is_favorited_by:
        print("Item is favorited by")
        return 'favorited_by'
    print("Item has no special class")
    return ''

def get_class(item):
    """Returns a class name based on item properties."""
    if item.is_dev:
        print("Item is dev")
        return 'dev'
    elif item.is_favorite:
        print("Item is favorite")
        return 'favorite'
    elif item.is_favorited_by:
        print("Item is favorited by")
        return 'favorited_by'
    print("Item has no special class")
    return ''


