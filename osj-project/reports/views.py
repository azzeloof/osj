from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.views.generic import CreateView
from .forms import ReportForm
from things.models import Thing
from profiles.models import Profile

# Create your views here.
class NewReport(CreateView):
    form_class = ReportForm
    template_name = 'reports/new.html'

    def get(self, request, *args, **kwargs):
        #target = Thing.objects.get(pk=999)
        modelType = kwargs['model']
        targetID = kwargs['pk']
        if modelType == "thing":
            model = Thing
        elif modelType == "profile":
            model = Profile
        else:
            return HttpResponseNotFound("Invalid model")
        target = get_object_or_404(model, pk=targetID)
        context = {
            'model': modelType,
            'target': target,
            'report_form': ReportForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        modelType = kwargs['model']
        targetID = kwargs['pk']
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, modelType, targetID)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, modelType, targetID):
        self.object = form.save(commit=False)
        self.object.reporter = self.request.user
        if modelType == "thing":
            model = Thing
        elif modelType == "profile":
            model = Profile
        else:
            return HttpResponseNotFound("Invalid model")
        target = get_object_or_404(model, pk=targetID)
        self.object.content_object = target
        self.object.save()
        if modelType == "thing":
            return redirect(reverse('jewelryPiece', kwargs={'pk': targetID}))
        elif modelType == "profile":
            return redirect(reverse('profile', kwargs={'slug': target.user}))
        else:
            return HttpResponseNotFound("Invalid model")

    def form_invalid(self, form):
        pass
