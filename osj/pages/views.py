from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.urls import reverse
from django.contrib import messages
from taggit.models import Tag
import things
import pages
import articles
import profiles
from .forms import ThingForm, ThingImageFormset, ThingFileFormset, ProfilePhotoForm, ProfileDataForm
import os
import json
from hitcount.views import HitCountDetailView
from osj.settings import MEDIA_ROOT
import mimetypes
from django.db.models import Count


def getJewelryContext(jewelry):
    pieces = []
    for piece in jewelry:
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
        pieces.append({
            'piece': piece,
            'created': piece.created.date,
            'modified': piece.modified.date,
            'featuredImage': featuredImage,
            'category': piece.category
        })
    return pieces


def getUserContext(request):
    context = {
        #'user': request.user,
        'currentuserprofile': profiles.models.Profile.objects.get(user=request.user)
    }
    return context


def index(request):
    pieces = things.models.Thing.objects.filter(featured=True).order_by('-id')[:9]
    context = {
        'pieces': getJewelryContext(pieces)
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/index.html', context)


def page(request, slug):
    object = get_object_or_404(pages.models.Page, slug=slug)
    context = {'page': object}
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'pages/page.html', context)


class JewelryListView(ListView):
    model = things.models.Thing
    template_name = 'pages/allJewelry.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = self.model.objects.all()
        category = self.request.GET.get('category', None)
        orderBy = self.request.GET.get('orderby', None)
        direction = self.request.GET.get('direction', None)
        area = self.request.GET.get('area', None)
        if category:
            queryset = queryset.distinct().filter(category__name=category)
        elif area:
            categories = get_object_or_404(things.models.SuperCategory, name=area).category_set.all()
            catNames = []
            for category in categories:
                catNames.append(category.name)
            queryset = queryset.distinct().filter(category__name__in=catNames)
        allowedFields = [f.name for f in things.models.Thing._meta.get_fields()] # maybe this list should just be hardcoded
        if orderBy in allowedFields:
            if orderBy == "likes":
                queryset = queryset.annotate(nLikes=Count('likes')).order_by('nLikes')
            else:
                queryset = queryset.order_by(orderBy)
            if direction == 'descending':
                return queryset.reverse()
            else:
                return queryset
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(JewelryListView, self).get_context_data(**kwargs)
        pieces = context['object_list']
        piecesContext = getJewelryContext(pieces)
        categoryContext = {}
        bodyParts = things.models.SuperCategory.objects.all()
        for part in bodyParts:
            categoryContext.update({
                part.name: part.category_set.all()
            })
        context.update({
            'pieces': piecesContext,
            'categories': categoryContext
            })
        category = self.request.GET.get('category', None)
        area = self.request.GET.get('area', None)
        if category:
            context.update({'category': category})
        elif area:
            context.update({'category': area})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context


class JewelryDetailView(HitCountDetailView):
    model = things.models.Thing
    template_name = 'pages/jewelry.html'
    context_object_name = 'piece'
    count_hit = True

    def get_context_data(self, **kwargs):
        piece = self.object
        files = piece.file_set.all()
        images = piece.image_set.all()
        likes = piece.likes.all() # set of users
        nLikes = len(likes)
        fileContext = []
        downloads = 0
        for fileObj in files:
            try:
                file = fileObj.file.file
                fileName = os.path.basename(fileObj.file.file.name)
            except:
                file = None
                fileName = "File Not Found"
            fileContext.append({
                'file': file,
                'filename': fileName,
                'name': fileObj.name,
                'url': fileObj.file.url,
                'id': fileObj.id,
                'downloads': fileObj.downloads
            })
            downloads += fileObj.downloads
        context = super(JewelryDetailView, self).get_context_data(**kwargs)
        context.update({
            'piece': piece,
            'created': piece.created.date,
            'modified': piece.modified.date,
            'files': fileContext,
            'images': images,
            'likes': nLikes,
            'downloads': downloads
        })
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
            userID = self.request.user.id
            if(likes.filter(id=userID).exists()):
                context.update({
                    'liked': True
                })
            if self.request.user == piece.creator:
                context.update({'editable': True})
        return context

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


def getTags():
    tags = Tag.objects.all()
    options = ''
    for tag in tags:
        options += str(tag) + ','
    return options.strip(',')

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
            'fileFormset': ThingFileFormset(),
            'tags': getTags()
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
        form.save_m2m() # needed to save tags
        for fs in [imageFormset, fileFormset]:
            if fs.is_valid():
                objSet = fs.save(commit=True)
                for obj in objSet:
                    obj.thing = self.object
                    obj.save()
                #else:
            #    print(fs.errors)
        return redirect(reverse('jewelryPiece', kwargs={'pk': self.object.id}))

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
            'fileFormset': ThingFileFormset(instance=self.object),
            'tags': getTags()
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
        form.save_m2m() # needed to save tags
        for fs in [imageFormset, fileFormset]:
            if fs.is_valid():
                objSet = fs.save(commit=True)
                for obj in objSet:
                    obj.thing = self.object
                    obj.save()
            #else:
            #    print(fs.errors)
        return redirect(reverse('jewelryPiece', kwargs={'pk': self.object.id}))
        #return super(JewelryUpdateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        handler = super(JewelryUpdateView, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        if self.object.creator != request.user:
            return HttpResponseForbidden(u"Can't touch this.")
        return handler


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
        if request.POST.get("operation") == "like_submit":# and request.is_ajax():
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


"""def tagged(request, slug=None):
    # Set up queryset
    tag = get_object_or_404(Tag, slug=slug)
    queryset = things.models.Thing.objects.filter(tags=tag)
    category = request.GET.get('category', None)
    orderBy = request.GET.get('orderby', None)
    direction = request.GET.get('direction', None)
    area = request.GET.get('area', None)
    if category:
        queryset = queryset.distinct().filter(category__name=category)
    elif area:
        categories = get_object_or_404(things.models.SuperCategory, name=area).category_set.all()
        catNames = []
        for category in categories:
            catNames.append(category.name)
        queryset = queryset.distinct().filter(category__name__in=catNames)
    allowedFields = [f.name for f in things.models.Thing._meta.get_fields()] # maybe this list should just be hardcoded
    if orderBy in allowedFields:
        if orderBy == "likes":
            queryset = queryset.annotate(nLikes=Count('likes')).order_by('nLikes')
        else:
            queryset = queryset.order_by(orderBy)
        if direction == 'descending':
            pieces = queryset.reverse()
        else:
            pieces = queryset
    else:
        pieces = queryset

    # Get context
    context = {
        'tag':tag
    }
    piecesContext = getJewelryContext(pieces)
    categoryContext = {}
    bodyParts = things.models.SuperCategory.objects.all()
    for part in bodyParts:
        categoryContext.update({
            part.name: part.category_set.all()
        })
    context.update({
        'pieces': piecesContext,
        'categories': categoryContext
        })
    if category:
        context.update({'category': category})
    elif area:
        context.update({'category': area})
    if request.user.is_authenticated:
            context.update(getUserContext(request))
    
    return render(request, 'pages/tagged.html', context)
"""

class Tagged(ListView):
    model = things.models.Thing
    template_name = 'pages/tagged.html'
    paginate_by = 20

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        queryset = self.model.objects.filter(tags=tag)
        category = self.request.GET.get('category', None)
        orderBy = self.request.GET.get('orderby', None)
        direction = self.request.GET.get('direction', None)
        area = self.request.GET.get('area', None)
        if category:
            queryset = queryset.distinct().filter(category__name=category)
        elif area:
            categories = get_object_or_404(things.models.SuperCategory, name=area).category_set.all()
            catNames = []
            for category in categories:
                catNames.append(category.name)
            queryset = queryset.distinct().filter(category__name__in=catNames)
        allowedFields = [f.name for f in self.model._meta.get_fields()] # maybe this list should just be hardcoded
        if orderBy in allowedFields:
            if orderBy == "likes":
                queryset = queryset.annotate(nLikes=Count('likes')).order_by('nLikes')
            else:
                queryset = queryset.order_by(orderBy)
            if direction == 'descending':
                return queryset.reverse()
            else:
                return queryset
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(Tagged, self).get_context_data(**kwargs)
        pieces = context['object_list']
        piecesContext = getJewelryContext(pieces)
        categoryContext = {}
        bodyParts = things.models.SuperCategory.objects.all()
        for part in bodyParts:
            categoryContext.update({
                part.name: part.category_set.all()
            })
        context.update({
            'pieces': piecesContext,
            'categories': categoryContext
            })
        category = self.request.GET.get('category', None)
        area = self.request.GET.get('area', None)
        if category:
            context.update({'category': category})
        elif area:
            context.update({'category': area})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context

class ProfileDetailView(DetailView):
    model = profiles.models.Profile
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        jewelry = self.object.user.thing_set.all()
        context.update({'pieces': getJewelryContext(jewelry)})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
            if self.request.user == self.object.user:
                liked = things.models.Thing.objects.filter(likes=self.request.user)
                context.update({
                    'editable': True,
                    'liked': liked
                    })
        return context


def profileUpdateView(request, slug):
    #https://stackoverflow.com/questions/54404250/django-populate-form-using-function-based-view-with-multiple-forms
    profile = get_object_or_404(profiles.models.Profile, slug=slug)
    if request.method == 'POST':
        photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        data_form = ProfileDataForm(request.POST, instance=profile)
        valid = False
        if photo_form.is_valid():
            valid = True
            photo_form.save()
        if data_form.is_valid():
            valid = True
            data_form.save()
    else:
        photo_form = ProfilePhotoForm(instance=profile)
        data_form = ProfileDataForm(instance=profile)
    
    context = {
        'photo_form': photo_form,
        'data_form': data_form
    }
    if request.user.is_authenticated:
        # they had better be authenticated
        context.update(getUserContext(request))

    if (request.method == 'POST' and valid):
        return redirect('profileUpdate', slug=slug)
    else:
        return render(request, 'pages/editProfile.html', context)


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
