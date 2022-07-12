from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
import things
import pages
import articles
import os
import mimetypes
from osj.views import getUserContext
from things.views import getJewelryContext


class Index(ListView):
    model = things.models.Thing
    template_name = 'pages/index.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(featured=True)
        queryset = queryset.order_by('date_featured')[::-1]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        pieces = context['object_list']
        context = {'pieces': getJewelryContext(pieces)}
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context


def page(request, slug):
    object = get_object_or_404(pages.models.Page, slug=slug)
    context = {'page': object}
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/page.html', context)

def downloadFile(request, pk):
    file = get_object_or_404(things.models.File, pk=pk)
    file.downloads += 1
    file.save()
    filepath = os.path.abspath(file.file.path)
    try:
        path = open(filepath, 'rb')
        mimetype, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mimetype)
        response['Content-Disposition'] = "attachment; filename=%s" % file.file.name
    except:
        response = HttpResponse("File not found")
    return response


def legal(request, slug):
    context = {
        "tos": False,
        "pp": False,
        "ug": False
    }
    if slug == "termsofservice":
        context.update({"tos": True})
    elif slug == "privacypolicy":
        context.update({"pp": True})
    elif slug == "userguidelines":
        context.update({"ug": True})
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/legal.html', context)


def notifications(request):
    context = {}
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/notifications.html', context)
