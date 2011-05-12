# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2009-2010 Ionuț Arțăriși

# cuZmeură is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# cuZmeură is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with cuZmeură.  If not, see <http://www.gnu.org/licenses/>.

import datetime, hashlib, random

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from ads.forms import UserRegistrationForm, PublisherForm
from ads.models import (Ad, Impression, Product, Publisher, User,
                        UserActivation)
from ads.stats import graph_monthly_imp

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # Build the activation key
            salt = hashlib.md5(str(random.random())).hexdigest()[-5:]
            activation_key = hashlib.md5(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            new_activ = UserActivation(user=new_user,
                                       activation_key=activation_key,
                                       key_expires=key_expires)
            new_activ.save()

            # FIXME: move this to a template?
            # Send email with the activation information
            email_subject = _(u"Contul tău cuZmeură")
            email_body = _(u"Salut %s, \n\n"
                           u"Îți mulțumim că te-ai înregistrat în rețeaua "
                           u"cuZmeură.\n\n Îți poți activa contul în "
                           u"următoarele două zile, urmând legătură aceasta:"
                           u"\n %s" % (
                               new_user.username,
                               settings.SITE_URL+'user/confirm/'+activation_key))
            send_mail(email_subject, email_body, settings.SITE_EMAIL,
                      [new_user.email])

            return render_to_response("register.html", {"thanks": True},
                                    context_instance=RequestContext(request))
    else:
        form = UserRegistrationForm()
    return render_to_response("register.html", {
        'form': form},
        context_instance=RequestContext(request))

def confirm(request, activation_key):
    '''Handles confirmation of user accounts with email received activation key
    '''
    if request.user.is_authenticated():
        return redirect("/user/profile/")
    
    activation = get_object_or_404(UserActivation,
                                   activation_key=activation_key)

    if activation.key_expires < datetime.datetime.today():
        return render_to_response("confirm.html", {"expired":True},
                                  context_instance=RequestContext(request))

    user = activation.user

    if user.is_active:
        return render_to_response("confirm.html", {"already_active":True},
                                  context_instance=RequestContext(request))
    else:
        user.is_active = True
        user.save()
        return render_to_response("confirm.html", {"success":True},
                                  context_instance=RequestContext(request))
    
@login_required
def profile(request):
    '''User profile.

    Returns a list of the total impressions on all the user`s Publishers.
    :pub_imp: a list of publisher details formed like this:
    [publisher name, publisher slug, total impressions, real impressions]
    :domain: use this to build nice snippets (should go away at some point)
    :products: a list of Product objects belonging to the user
    '''
    form = PublisherForm()
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            new_pub = form.save(commit=False)
            new_pub.owner = request.user
            new_pub.save()
            request.user.message_set.create(message=_(
                u"Noul sait a fost adaugat cu succes."))
        
    publishers = Publisher.objects.filter(owner=request.user)

    products = Product.objects.filter(owner=request.user)

    pub_imp = []
    for pub in publishers:
        imp = Impression.objects.filter(publisher=pub.url).count()
        real_imp = Impression.objects.filter(referer_netloc=pub.url).count()
        pub_imp.append([pub.name, pub.slug, imp, real_imp])
    
    return render_to_response("profile.html", {
        'pub_imp':pub_imp,
        'domain': settings.SITE_URL,
        'products': products,
        'form':form,
        },
        context_instance=RequestContext(request))

@login_required
def product(request, product):
    '''Get a product and its corresponding ads
    '''
    ads = Ad.objects.filter(product__name=product)
    return render_to_response("product.html", {
        'ads':ads,
        'product':product,
        },
        context_instance=RequestContext(request))
    
@login_required
def delete_pub(request, pub_slug):
    '''Deletes the Publisher coresponding to the pub_slug

    only if the publisher belongs to the current user.
    '''
    # FIXME: test me!
    try:
        pub = Publisher.objects.get(slug=pub_slug)
    except Publisher.DoesNotExist:
        request.user.message_set.create(message=_(u"Saitul apelat nu exista!"))
        return redirect("/user/profile/")
    else:
        if request.user == pub.owner:
            pub.delete()
            request.user.message_set.create(message=_(u"Saitul a fost sters cu"
                                            u" succes!"))
        else:
            request.user.message_set.create(message=_(u"Nu ai dreptul de a "
                                                      u"șterge acest sait!"))
        return redirect("/user/profile/")

@login_required
def modify_pub(request, pub_slug):
    '''Page to do various modifications to an ad and delete it
    '''
    try:
        pub = Publisher.objects.get(slug=pub_slug)
    except Publisher.DoesNotExist:
        request.user.message_set.create(message=_(u"Saitul apelat nu exista!"))
        return redirect("/user/profile/")
    else:
        if request.method == 'POST':
            if request.user == pub.owner:
                form = PublisherForm(request.POST, instance=pub)
                if form.is_valid():
                    pub = form.save()
                    request.user.message_set.create(message=_(
                        u'Saitul a fost modificat cu succes!'))
                else:
                    return render_to_response("modify_pub.html", {
                        'form':form,
                        'form_action': '/user/pub/modify/'+pub.slug,
                        'pub_slug':pub.slug,
                        'pub':pub,
                        }, context_instance=RequestContext(request))
            else:
                request.user.message_set.create(message=_(
                    u'Nu ai dreptul de a modifica acest sait!'))
            return redirect("/user/pub/modify/%s" % pub.slug)
                
        else: # GET
            form = PublisherForm(instance=pub)
            graph_url = graph_monthly_imp(pub)
            return render_to_response("modify_pub.html", {
                'domain':settings.SITE_URL,
                'form':form,
                'form_action': '/user/pub/modify/'+pub.slug,
                'pub_slug':pub.slug,
                'pub':pub,
                'graph_url':graph_url,
                }, context_instance=RequestContext(request))
