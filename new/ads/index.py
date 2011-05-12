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

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from ads.models import Article, Impression, Product, Publisher

def index(request):
    '''Front page - includes the total impressions so far.
    '''
    impressions = Impression.objects.count()
    product_count = Product.objects.count()
    publisher_count = Publisher.objects.count()

    posts = Article.objects.filter(published=True).order_by('-created_at')[:10]
    
    return render_to_response('index.html', {
        'impressions':impressions,
        'domain':settings.SITE_URL,
        'project_count': product_count,
        'publisher_count':publisher_count,
        'posts':posts,
        },
        context_instance=RequestContext(request))
