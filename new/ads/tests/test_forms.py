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

from django.test import TestCase

from ads.models import Publisher

class PublisherFormTests(TestCase):
    fixtures = ['one_good_user', 'foo-bar-publisher']
    username = 'gigel'
    password = 'gigipass'
    publisher_one = {
            'name': 'Foo Bâr#$*',
            'url': 'http://example.com/'
        }
    publisher_two = {
            'name' : 'somethingelse',
            'url' : 'http://example2.com/'
        }
    slug = 'foo-bar'

    def test_two_names_same_slug_new(self):
        '''Two different names that generate the same slug must fail
        '''
        login = self.client.login(username=self.username,
                                  password=self.password)
        response = self.client.post('/user/profile/', self.publisher_one)
        self.assertFormError(response, 'form', 'name',
                             u'Există deja un sait cu acest nume sau unul '
                             u'similar.')

    def test_two_names_same_slug_edit(self):
        '''Test that two different names with the same slug fail when editing

        This has to be tested on a different publisher, otherwise we are just
        modifying the existing one, which is legal.
        '''
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.client.post('/user/profile/', self.publisher_two)
        response = self.client.post(
            '/user/pub/modify/%s' % self.publisher_two['name'],
            self.publisher_one)
        self.assertFormError(response, 'form', 'name',
                            u'Există deja un sait cu acest nume sau unul '
                            u'similar.')

    def test_edit_name_and_url(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        response = self.client.post('/user/pub/modify/%s' % self.slug,
                                    self.publisher_one)
        self.assertRedirects(response,
                             '/user/pub/modify/%s' % self.slug,
                             target_status_code=200)

    def test_modify_without_logging_in(self):
        response = self.client.post('/user/pub/modify/%s' % self.slug,
                                    self.publisher_one)
        self.assertRedirects(response,
                             "/login/?next=/user/pub/modify/%s" % self.slug)

    def test_modifiy_pub_does_not_exist(self):
        '''Try to modify a publisher that does not exist
        '''
        login = self.client.login(username=self.username,
                                  password=self.password)
        response = self.client.post('/user/pub/modify/%s' % self.slug,
                                    self.publisher_one)
        self.assertRedirects(response, '/user/pub/modify/%s' % self.slug)

    def test_new_publisher_create(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        response = self.client.post('/user/profile/', self.publisher_two)
        p = Publisher.objects.exclude(slug=self.slug).all()[0]
        
        self.assertEqual(p.name, self.publisher_two['name'])
        self.assertEqual(p.url, self.publisher_two['url'])
        self.assertEqual(p.owner.username, self.username)
