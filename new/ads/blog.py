# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2010 Ionuț Arțăriși

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

from django.shortcuts import render_to_response
from django.template import RequestContext
from ads.models import Article

def get_post(request, slug):
    '''Return a given post
    '''

    post = Article.objects.get(slug=slug)

    return render_to_response('article.html', {
        'post':post,
        },
        context_instance=RequestContext(request))
