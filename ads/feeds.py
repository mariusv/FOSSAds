# -*- coding: utf-8 -*-
# This file is part of FOSSAds.
# Copyright (c) 2011 Marius Voilă

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

from django.contrib.syndication.feeds import Feed
from ads.models import Article

class latest(Feed):
    title = "FOSSAds News"
    link = "/feed/"
    description = "News about FOSSAds development and project work"

    def items(self):
        return Article.objects.order_by('-created_at')[:10]
