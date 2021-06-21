from django.shortcuts import render
from app.models import Page
from app.tools import get_root_parent, get_tree, get_available_parent_set


def handle_view_list(request):
    return render(request, 'list.html', context={
        'page_list': Page.objects.all()
    })


def handle_view_create(request):
    return render(request, 'form_create.html', context={
        'page_list': Page.objects.all()
    })


def handle_view_record(request, pk):
    page = Page.objects.get(pk=pk)
    return render(request, 'form.html', context={
        'page': {
            'name': page.name,
            'pk': page.pk,
            'content': page.content,
            'parent_id': page.parent.pk if page.parent else 0
        },
        'tree': get_tree(get_root_parent(page)) or 0,
        'available_parents': list(get_available_parent_set(page))
    })
