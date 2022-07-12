from django.shortcuts import render, redirect, get_object_or_404
from django.http import  HttpResponseForbidden
from django.views.generic import DetailView
from taggit.models import Tag
import things
import profiles
from .forms import ProfilePhotoForm, ProfileDataForm, UserDataForm
from osj.views import getUserContext
from things.views import getJewelryContext

class ProfileDetailView(DetailView):
    model = profiles.models.Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        jewelry = self.object.user.thing_set.all()
        context.update({'pieces': getJewelryContext(jewelry)})
        if self.request.user.is_authenticated:
            context.update(getUserContext(self.request))
            if self.request.user == self.object.user:
                likedPieces = things.models.Thing.objects.filter(likes=self.request.user)
                liked = getJewelryContext(likedPieces)
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
        user_data_form = UserDataForm(request.POST, instance=profile.user)
        profile_data_form = ProfileDataForm(request.POST, instance=profile)
        valid = False
        if photo_form.is_valid():
            valid = True
            photo_form.save()
        if profile_data_form.is_valid():
            valid = True
            currentEmail = profile.user.email
            newEmail = user_data_form.data['email']
            if currentEmail != newEmail:
                # The email has changed
                profile.email_verified = False
            profile_data_form.save()
        if user_data_form.is_valid():
            valid = True
            user_data_form.save()
    else:
        photo_form = ProfilePhotoForm(instance=profile)
        profile_data_form = ProfileDataForm(instance=profile)
        user_data_form = UserDataForm(instance=profile.user)
    
    context = {
        'photo_form': photo_form,
        'profile_data_form': profile_data_form,
        'user_data_form': user_data_form
    }
    if request.user.is_authenticated:
        # they had better be authenticated
        context.update(getUserContext(request))

    if profile.user != request.user:
        return HttpResponseForbidden(u"Can't touch this.")
    if (request.method == 'POST' and valid):
        return redirect('profileUpdate', slug=slug)
    else:
        return render(request, 'profiles/editProfile.html', context)

