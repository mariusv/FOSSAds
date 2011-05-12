# -*- coding: utf-8 -*-
# This file is part of FOSSAds.
# Copyright (c) 2009-2010 Marius Voilă

# FOSSAds is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# FOSSAds is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with FOSSAds.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from ads.models import Publisher, User

class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(_(u"There is already an account with this name."
                                          ))
        return unicode(username)

    def clean_password2(self):
        password = self.cleaned_data['password'] or ''
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_(u"The two password fields "
                                          u"must be identical."))
        return password2

    def save(self):
        new_user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password2'])
        new_user.is_active = False
        new_user.save()
        return new_user

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name', 'url')
    def clean_name(self):
        name = self.cleaned_data['name']
        if Publisher.objects.filter(slug=slugify(name)
                                ).exclude(id=self.instance.id):
            raise forms.ValidationError(_(
                u'EThere is already a site with that name or similar.'))
        return name
    def clean_url(self):
        url = self.cleaned_data['url']
        if Publisher.objects.filter(url=url).exclude(id=self.instance.id):
            raise forms.ValidationError(_(
                u'There is already a site with this url'))
        return url
