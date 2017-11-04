from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .emojipaths import translate_emoji_string

# Create your views here.
def index(request):
    return render(request, 'demoji.html')

def get_translation(request):
    # raise Exception(request.GET)
    # emoji = ''.join([bytes("\\x{}".format(s), 'ascii').decode('unicode-escape') for s in request.GET.getlist('emoji[]', None)])
    emoji = ''.join([bytes("\\u{}".format(s), 'ascii').decode('unicode-escape') for s in request.GET.getlist('emoji[]', None)])
    # emoji = ''.join(s for s in request.GET.getlist('emoji[]', None))
    # return JsonResponse({'translation': emoji})
    data = {
        'translation': translate_emoji_string(emoji)
    }
    return JsonResponse(data)
    