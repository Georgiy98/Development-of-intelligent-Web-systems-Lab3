from app.models import Page


def get_root_parent(page):
    if page.parent:
        return get_root_parent(page.parent)
    return page


def get_tree(parent):
    return {
        'name': parent.name,
        'pk': parent.pk,
        'child_ids': [get_tree(child) for child in parent.child_ids.all()]
    }


def get_all_pages(page, res=None):
    if res is None:
        res = []
    res.append(page.pk)
    for child in page.child_ids.all():
        get_all_pages(child, res)
    return res


def get_available_parent_set(page):
    pages = Page.objects.exclude(id__in=get_all_pages(page))
    return [{'name': page.name, 'pk': page.pk} for page in pages]
