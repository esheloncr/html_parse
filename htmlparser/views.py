from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.core.serializers.json import Serializer
from django.views.decorators.csrf import csrf_exempt
from .models import HtmlData, Links
from .parser import HtmlParser
import json
import re


@csrf_exempt
def index(request):
    if request.method == "POST":
        body = request.body.decode("UTF-8")
        url = validate_json(body)
        if type(url) == JsonResponse:
            return url
        parse_status = parse(url)
        if type(parse_status) == int:
            return JsonResponse({"error": parse_status})
        elif type(parse_status) == JsonResponse:
            return parse_status
        else:
            return JsonResponse({"status": "success"})
    return HttpResponse("Welcome. To start just go to /page/")


def get_object(request, pk=None):
    query = HtmlData.objects.filter(pk=pk)
    serializer_data = Serializer().serialize(query, use_natural_foreign_keys=True)
    data = json.loads(serializer_data)
    cleaned_data = data[0].get('fields')
    return JsonResponse(cleaned_data, safe=False)


def all_objects(request):
    queryset = HtmlData.objects.all()
    serializer_data = Serializer().serialize(queryset, use_natural_foreign_keys=True)
    data = json.loads(serializer_data)
    cleaned_data = clean_data(data)
    return JsonResponse(cleaned_data, safe=False)


def parse(url):
    arr = []
    parser = HtmlParser(url)
    if not parser.status:
        return JsonResponse({"error": "incorrect url"})
    if parser.status_code != 200:
        return parser.status_code
    for l in parser.links:
        link = Links.objects.create(link=l)
        arr.append(link)
    htmldata = HtmlData(h1_count=parser.h1, h2_count=parser.h2, h3_count=parser.h3)
    htmldata.save()
    htmldata.links.add(*arr)


def clean_data(data):
    cleaned_data = []
    for i in data:
        del i['model']
        i['page_id'] = i.pop('pk')
        cleaned_data.append(i)
    return cleaned_data


def validate_json(data):
    try:
        data = json.loads(data)
        url = data.get('url')
        if re.match(r'http', url):
            return url
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'incorrect json'})
