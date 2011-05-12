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

import random
from urlparse import urlparse

from django.shortcuts import (render_to_response, get_object_or_404)
from django.http import Http404
from ads.models import Impression, Product, Publisher

DEFAULTSLUG = 'default'
DEFAULT_SIZE= '120x90'
NOIP = '10.0.0.1'

def serve_ad(request, slugpub=None, size=DEFAULT_SIZE):
    '''Serve an ad with the given slugpub and size
 
    see the get_ad docstring for how
    '''
    if size == None:
        size = DEFAULT_SIZE

    ad = get_ad(size)

    try:
        referer = request.META["HTTP_REFERER"].replace('://www.', '://')
    except KeyError:
        referer = None
    else:
        # get schema and netloc from the referer url
        referer_loc = '%s://%s/' % urlparse(referer)[:2]


    publisher = get_object_or_404(Publisher, slug=(slugpub or DEFAULTSLUG))

    impression = Impression.objects.create(
        ip=request.META.get("REMOTE_ADDR", NOIP),
        referer = referer,
        referer_netloc = referer_loc if referer else None,
        publisher = publisher.url,
        ad = ad)
    impression.save()

    return render_to_response('serve.html', {
        'ad_url' : ad.url,
        'ad_name' : ad.name,
        'ad_img_url' : ad.image.url,
        'ad_size' : ad.size.size
        })

def get_ad(size):
    '''Get the ad from the database.

    Go through each Product and get the first Ad of that Product. If the
    Product has more than one Ad, get the next one, next time we get to that
    Ad.

    Return a 404 if nothing is found
    '''

    products = Product.objects.filter(ad__size__size__exact=size,
                                      ad__accepted=True).distinct()
    if not products:
        raise Http404
    
    product = products[Impression.objects.count() % len(products)]

    # FIXME: maybe we can make this sequential rather than random
    return random.choice(product.ad_set.filter(accepted=True).all())
