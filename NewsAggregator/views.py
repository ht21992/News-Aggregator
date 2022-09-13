from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_vox_headlines, get_time_headlines, WEBSITE_DICT
import datetime


def main(request):
    headlines = get_vox_headlines()

    return render(request, 'main.html', context={'headlines': headlines})


def refresh_news(request):
    website = request.GET.get('website', '')
    try:
        headlines = WEBSITE_DICT[website]()
    except KeyError:
        return HttpResponse('Try Another Website')
    return render(request, 'partials/news.html', context={'headlines': headlines, 'update_time': datetime.datetime.now().strftime('%A %d-%b-%Y %H:%M:%S'), 'website': website})


def change_website(request):
    website = request.GET.get('website', '')
    try:
        headlines = WEBSITE_DICT[website]()
    except KeyError:
        return HttpResponse('Try Another Website')
    return render(request, 'partials/news.html', context={'headlines': headlines, 'update_time': datetime.datetime.now().strftime('%A %d-%b-%Y %H:%M:%S'), 'website': website})
