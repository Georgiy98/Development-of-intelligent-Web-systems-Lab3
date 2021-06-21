from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.apps import apps
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json


def _get_model(model):
    try:
        return apps.get_model('app', model)
    except LookupError:
        return None


def _create(model, request):
    if request.POST:
        data = {key: request.POST[key] for key in request.POST}
    else:
        data = json.loads(request.body)
    return model.objects.create(**data)


def _to_json(obj):
    res = vars(obj)
    res.pop('_state')
    return res


@csrf_exempt
def handle_api_list(request, model):
    model = _get_model(model)
    if model is None:
        return HttpResponse('No such model', status=400)
    if request.method == 'GET':
        return JsonResponse(list(model.objects.values()), safe=False)
    elif request.method == 'POST':
        return JsonResponse(_to_json(_create(model, request)))


@csrf_exempt
def handle_api_record(request, model, pk):
    model = _get_model(model)
    if model is None:
        return HttpResponse('No such model', status=400)
    try:
        res = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponse('No such object', status=400)
    if request.method == 'GET':
        return JsonResponse(_to_json(res))
    elif request.method == 'POST':
        data = request.POST or json.loads(request.body)
        for key, value in data.items():
            res.__setattr__(key, value)
        res.save()
        return JsonResponse(_to_json(res))
    elif request.method == 'DELETE':
        return JsonResponse(res.delete()[1])
