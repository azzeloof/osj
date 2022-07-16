from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from taggit.models import Tag
from .forms import ThingForm, ThingImageFormset, ThingFileFormset
from .models import Thing, SuperCategory, Licence
import os
from hitcount.views import HitCountDetailView
from osj.settings import MEDIA_ROOT
from django.db.models import Count
from osj.views import getUserContext
from django.contrib.auth.decorators import login_required
import json

def getDownloadCount(piece):
    files = piece.file_set.all()
    downloads = 0
    for fileObj in files:
        downloads += fileObj.downloads
    return downloads

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
            'category': piece.category,
            'likes': len(piece.likes.all()),
            'downloads': getDownloadCount(piece)
        })
    return pieces

def getLicenceContext():
    licences = Licence.objects.all()
    licenceContext = []
    for licence in licences:
        licenceContext.append(licence)
    return licenceContext

def getTags():
    tags = Tag.objects.all()
    options = ''
    for tag in tags:
        options += str(tag) + ','
    return options.strip(',')

class JewelryListView(ListView):
    model = Thing
    template_name = 'things/allJewelry.html'
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
            categories = get_object_or_404(SuperCategory, name=area).category_set.all()
            catNames = []
            for category in categories:
                catNames.append(category.name)
            queryset = queryset.distinct().filter(category__name__in=catNames)
        allowedFields = [f.name for f in Thing._meta.get_fields()] # maybe this list should just be hardcoded
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
        bodyParts = SuperCategory.objects.all()
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
    model = Thing
    template_name = 'things/jewelry.html'
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
        context.update({
            'piece': piece,
            'created': piece.created.date,
            'modified': piece.modified.date,
            'files': fileContext,
            'featuredImage': featuredImage,
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


class JewelryDeleteView(DeleteView):
    model = Thing
    success_url = reverse_lazy('jewelry')
    template_name = 'things/deleteJewelry.html'

    def get_context_data(self, **kwargs):
        context = super(JewelryDeleteView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            # they had better be
            if obj.creator != self.request.user:
                return HttpResponseForbidden("You don't have permission to do that!")
            else:
                return super(JewelryDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("C'mon, you aren't even logged in!")

class JewelryCreateView(CreateView):
    form_class = ThingForm
    template_name = 'things/editJewelry.html'

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
                objSet = fs.save(commit=False) # This used to be True, setting it to False fixed this error:
                # "save() prohibited to prevent data loss due to unsaved related object"
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
    model = Thing
    form_class = ThingForm
    template_name = 'things/editJewelry.html'

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
            #print(fs.deleted_forms)
            if fs.is_valid():
                objSet = fs.save(commit=True)
                for obj in objSet:
                    obj.thing = self.object
                    obj.save()
                for obj in fs.deleted_objects:
                    if (obj.image):
                        try:
                            os.remove(os.path.join(MEDIA_ROOT, str(obj.image)))
                        except:
                            print("could not remove " + os.path.join(MEDIA_ROOT, str(obj.image)))
                    elif (obj.file):
                        try:
                            os.remove(os.path.join(MEDIA_ROOT, str(obj.file)))
                        except:
                            print("could not remove " + os.path.join(MEDIA_ROOT, str(obj.file)))
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



class Tagged(ListView):
    model = Thing
    template_name = 'things/tagged.html'
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
            categories = get_object_or_404(SuperCategory, name=area).category_set.all()
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
        context.update({'tag':self.kwargs['tag']})
        piecesContext = getJewelryContext(pieces)
        categoryContext = {}
        bodyParts = SuperCategory.objects.all()
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

@login_required
def like_button(request):
    #https://medium.com/@nishalk25121999/how-to-make-a-like-button-using-django-ajax-d2db38e6d2f8
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit":# and request.is_ajax():
            thingID=request.POST.get("piece_id",None)
            thing=get_object_or_404(Thing, pk=thingID)
            if thing.likes.filter(id=request.user.id): #already liked the content
                thing.likes.remove(request.user) #remove user from likes 
                liked=False
            else:
                thing.likes.add(request.user) 
                liked=True
            context={"likes":thing.totalLikes,"liked":liked,"thingID":thingID}
            return HttpResponse(json.dumps(context), content_type='application/json')