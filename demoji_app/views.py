from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import demoji_app.demoji_cfg as d_cfg
import json

# Create your views here.
def index(request):
    return render(request, 'demoji.html')

def get_translation(request):
    # raise Exception(request.GET)
    # emoji = ''.join([bytes("\\x{}".format(s), 'ascii').decode('unicode-escape') for s in request.GET.getlist('emoji[]', None)])
    # emoji = ''.join([bytes("\\u{}".format(s), 'ascii').decode('unicode-escape') for s in request.GET.getlist('emoji[]', None)])
    # emoji = ''.join('\\x{}'.format(s) for s in request.GET.getlist('emoji[]', None))
    
    emoji = ''.join(s for s in request.GET.getlist('emoji', None))
    # raise Exception(emoji)
    # return JsonResponse({'translation': emoji})
    data = {
        'translation': d_cfg.get_sentence(emoji)
    }
    return JsonResponse(data)
    