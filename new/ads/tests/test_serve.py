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

import os
from django.test import TestCase
from ads.models import Impression, Ad, Product

class ServeTests(TestCase):
    fixtures = ['ads.json']

    def _test_get_publisher(self, puburl):
        """
        Test for default publisher.
        """
        response = self.client.get('/serve/' + puburl)

        # get the ads belonging to the first Product
        ads = [a.name for a in Product.objects.all()[0].ad_set.all()]
        
        self.assertEqual(response.status_code, 200)
        self.assert_(response.context['ad_name'] in ads)

    def test_no_publisher(self):
        self._test_get_publisher('')
        
    def test_default_publisher(self):
        self._test_get_publisher('default')

    def test_notexists_publisher(self):
        response = self.client.get('/serve/notfound')
        self.assertEqual(response.status_code, 404)

    def test_size_match_regex(self):
        response = self.client.get('/serve/default/')
        self.assertEqual(response.context['ad_size'], '120x90')
        
        response = self.client.get('/serve/default/120x90')
        self.assertEqual(response.context['ad_size'], '120x90')

    def test_size_not_found(self):
        response = self.client.get('/serve/default/0x0')
        self.assertEqual(response.status_code, 404)

    def test_size_mismatch_regex(self):
        invalid_url = ['/serve/x125',
                        '/serve/x125',
                        '/serve/x12y',
                        '/serve/125x',
                        '/serve/12yx',
                        '/serve/125x1y',
                        '/serve/12yx125',
                        '/serve/y']
        for res in invalid_url:
            response = self.client.get(res)
            self.assertEqual(response.status_code, 404)

    def test_correct_referer_netloc(self):
        '''Test that the referer and the referer_netloc are stored correctly
        '''
        response = self.client.get('/serve/default/120x90',
                                   HTTP_REFERER='http://cuzmeura.org/xmpl')
        impre = Impression.objects.all()[0]
        self.assertEqual(impre.referer, 'http://cuzmeura.org/xmpl')
        self.assertEqual(impre.referer_netloc, 'http://cuzmeura.org/')
        # clean up
        Impression.objects.all()[0].delete()

    def test_www_referer_netloc(self):
        '''Referer with 'www.' is stored correctly
        '''
        response = self.client.get('/serve/',
                                   HTTP_REFERER='http://www.cuzmeura.org/xmpl')
        impre = Impression.objects.all()[0]
        self.assertEqual(impre.referer, 'http://cuzmeura.org/xmpl')
        self.assertEqual(impre.referer_netloc, 'http://cuzmeura.org/')
        # clean up
        Impression.objects.all()[0].delete()
        
    def test_ads_sequentiality(self):
        '''Serve ads from each product sequentially
        '''

        ads1 = Product.objects.all()[0].ad_set.all()
        ads2 = Product.objects.all()[1].ad_set.all()

        ads = [[a.name for a in ads] for ads in [ads1, ads2]]

        for req in [0,1,0,1]:
            response = self.client.get('/serve/default/120x90')
            self.assert_(response.context['ad_name'] in ads[req])
    def test_no_unaccepted_ads(self):
        '''Unaccepted ads never get shown
        '''
        bogus = Ad.objects.filter(accepted=False).all()[0]
        for req in range(10):
            response = self.client.get('/serve/default/')
            self.assertNotEquals(bogus.name, response.context['ad_name'])
    def test_all_ads_in_fixtures_exist(self):
        '''Test that all the ads in the fixtures exist in the filesystem

        ads in the fixtures should also be present in /media/ads
        '''
        paths = [ad.image.path for ad in Ad.objects.all()]
        for path in paths:
            self.failUnless(os.path.exists(path))
