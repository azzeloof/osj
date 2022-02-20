from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
import things
import pages
import articles
import profiles
from .forms import ThingForm, ThingImageFormset, ThingFileFormset
import os
import json


def getUserContext(request):
    context = {
        'user': request.user,
        'profile': profiles.models.Profile.objects.get(user=request.user)
    }
    return context


def index(request):
    context = {}
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/index.html', context)


def page(request, slug):
    object = get_object_or_404(pages.models.Page, slug=slug)
    context = {'page': object}
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/page.html', context)


def allJewelry(request):
    pieces = things.models.Thing.objects.all()
    piecesContext = []
    for piece in pieces:
        images = piece.image_set.all()
        hasFeatured = False
        if len(images) > 0:
            for image in images:
                if image.featured:
                    hasFeatured = True
                    featuredImage = image
            if hasFeatured == False:
                featuredImage = images[0]
        else:
            featuredImage = None
        piecesContext.append({
            'piece': piece,
            'created': piece.created.date,
            'modified': piece.modified.date,
            'featuredImage': featuredImage,
            'categories': piece.category
        })
    context = {
        'pieces': piecesContext
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/allJewelry.html', context)


def jewelryPiece(request, objID):
    piece = get_object_or_404(things.models.Thing, id=objID)
    files = piece.file_set.all()
    images = piece.image_set.all()
    likes = piece.likes.all() # set of users
    nLikes = len(likes)
    fileContext = []
    for fileObj in files:
        fileContext.append({
            'file': fileObj.file.file,
            'filename': os.path.basename(fileObj.file.file.name),
            'name': fileObj.name,
            'url': fileObj.file.url
        })
    context = {
        'piece': piece,
        'created': piece.created.date,
        'modified': piece.modified.date,
        'files': fileContext,
        'images': images,
        'likes': nLikes
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
        userID = request.user.id
        if(likes.filter(id=userID).exists()):
            context.update({
                'liked': True
            })
        if request.user == piece.creator:
            context.update({'editable': True})
    return render(request, 'pages/jewelry.html', context)


def allArticles(request):
    articleObjs = articles.models.Article.objects.all()
    context = {
        'articles': articleObjs
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/allArticles.html', context)


def article(request, objID):
    articleObj = get_object_or_404(articles.models.Article, id=objID)
    context = {
        'article': articleObj
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/article.html',context)


#@login_required
#def editJewelry(request, objID=None):
#    context = {}
#    form = ThingForm(request.POST or None, request.FILES or None)
#    if form.is_valid():
#        form.save()
#    context['form'] = form
#    return render(request, 'pages/editJewelry.html', context)


def getLicenceContext():
    licences = things.models.Licence.objects.all()
    licenceContext = []
    for licence in licences:
        licenceContext.append(licence)
    return licenceContext

class JewelryCreateView(CreateView):
    form_class = ThingForm
    template_name = 'pages/editJewelry.html'

    def get_context_data(self, **kwargs):
        context = super(JewelryCreateView, self).get_context_data(**kwargs)
        context.update({
            'imageFormset': ThingImageFormset(),
            'fileFormset': ThingFileFormset()
        })
        context.update({'licences': getLicenceContext()})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imageFormset = ThingImageFormset(self.request.POST, self.request.FILES)
        fileFormset = ThingFileFormset(self.request.POST, self.request.FILES)
        if form.is_valid():
            return self.form_valid(form, imageFormset, fileFormset)
        else:
            return self.form_invalid(form, imageFormset, fileFormset)

    def form_valid(self, form, imageFormset, fileFormset):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        for fs in [imageFormset, fileFormset]:
            if fs.is_valid():
                objSet = fs.save(commit=False)
                for obj in objSet:
                    obj.thing = self.object
                    obj.save()
            else:
                print(fs.errors)
        return redirect(reverse('jewelry'))

    def form_invalid(self, form, imageFormset, fileFormset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                    imageFormset=imageFormset,
                                    fileFormset=fileFormset)
        )


class JewelryUpdateView(UpdateView):
    model = things.models.Thing
    form_class = ThingForm
    template_name = 'pages/editJewelry.html'

    def get_context_data(self, **kwargs):
        self.object=self.get_object()
        context = super(JewelryUpdateView, self).get_context_data(**kwargs)
        context.update({
            'imageFormset': ThingImageFormset(instance=self.object),
            'fileFormset': ThingFileFormset(instance=self.object)
        })
        context.update({'licences': getLicenceContext()})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imageFormset = ThingImageFormset(self.request.POST, self.request.FILES, instance=self.object)
        fileFormset = ThingFileFormset(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid(form, imageFormset, fileFormset)
        else:
            return self.form_invalid(form, imageFormset, fileFormset)

    def form_valid(self, form, imageFormset, fileFormset):
        self.object = form.save(commit=False)
        self.object.save()
        for fs in [imageFormset, fileFormset]:
            if fs.is_valid():
                objSet = fs.save(commit=False)
                for obj in objSet:
                    obj.thing = self.object
                    obj.save()
            else:
                print(fs.errors)
        return redirect(reverse('jewelry'))
        #return super(JewelryUpdateView, self).form_valid(form)

    #def get_success_url(self):                
    #   return redirect(reverse('jewelry'))

    def form_invalid(self, form, imageFormset, fileFormset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                    imageFormset=imageFormset,
                                    fileFormset=fileFormset)
        )

@login_required
def like_button(request):
    #https://medium.com/@nishalk25121999/how-to-make-a-like-button-using-django-ajax-d2db38e6d2f8
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            thingID=request.POST.get("piece_id",None)
            thing=get_object_or_404(things.models.Thing,pk=thingID)
            if thing.likes.filter(id=request.user.id): #already liked the content
                thing.likes.remove(request.user) #remove user from likes 
                liked=False
            else:
                thing.likes.add(request.user) 
                liked=True
            context={"likes":thing.totalLikes,"liked":liked,"thingID":thingID}
            return HttpResponse(json.dumps(context), content_type='application/json')
    """     
   contents=things.models.Thing.objects.all()
   already_liked=[]
   id=request.user.id
   for content in contents:
       if(content.likes.filter(id=id).exists()):
        already_liked.append(content.id)
   ctx={"contents":contents,"already_liked":already_liked}
   return render(request,"like/like_template.html",ctx)
   """
