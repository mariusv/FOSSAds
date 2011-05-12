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

import datetime

from django.core import mail
from django.test import TestCase

from ads.models import Publisher, User, UserActivation
from ads.forms import UserRegistrationForm

DEFAULTURL = 'http://example.org/'
class RegistrationTests(TestCase):
    good_data = {
        'username':'gigi',
        'email': 'gigi@gigi.gi',
        'password': 'gigipass',
        'password2': 'gigipass'
        }
    def test_get_registration_form(self):
        '''GET the registration form
        '''
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_empty_registration_post(self):
        '''POST an empty dictionary to the registration form
        '''
        response = self.client.post('/user/register/', {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        required = 'This field is required.'
        self.assertFormError(response,'form','email', required)
        self.assertFormError(response, 'form', 'username', required)
        self.assertFormError(response, 'form', 'password', required)
        self.assertFormError(response, 'form', 'password2', required)
        
    def test_post_correct_form(self):
        '''POST correct data to registration form

        Verify that the email is sent and the thank you message is displayed.
        '''
        response = self.client.post('/user/register/', self.good_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertTrue(response.context['thanks'])
        self.assertEquals(len(mail.outbox), 1)
        self.failUnless('gigi' in mail.outbox[0].body)

    def test_differing_passwords(self):
        '''POST differing passwords to registration form'''
        post_data = {
            'username': 'gigi',
            'email': 'gigi@example.com',
            'password': 'gigi',
            'password2': 'NOTgigi'
            }

        response = self.client.post('/user/register/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'password2',
                             u"Cele două câmpuri pentru parolă trebuie să fie "
                             u"identice.")

    def test_user_exists(self):
        '''POST two users with the same name

        make two requests, we do not bother with the first one,
        it should have been tested elsewhere
        '''
        self.client.post('/user/register/', self.good_data)
        response = self.client.post('/user/register/', self.good_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'username',
                             u'Există deja un cont cu acest nume.')
                             
    def test_activate_with_key(self):
        '''POST good data and use validation key to confirm'''
        self.client.post('/user/register/', self.good_data)

        ua = UserActivation.objects.get(pk=1)
        self.assertFalse(ua.user.is_active)

        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm.html")
        self.assertTrue(response.context['success'])

        # reget to refresh the cache
        ua = UserActivation.objects.get(pk=1)
        self.assertTrue(ua.user.is_active)

        # second time, it should already be active
        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertTemplateUsed(response, "confirm.html")
        self.assertTrue(response.context["already_active"])

    def test_bad_activation(self):
        '''GET with a bad activation key'''
        response = self.client.get('/user/confirm/THIS_IS_NO_MD5')
        self.assertEqual(response.status_code, 404)

    def test_user_login_without_activation(self):
        '''Users cannot login without activation'''
        self.client.post('/user/register/', self.good_data)

        login = self.client.login(username=self.good_data['username'],
                                  password=self.good_data['password'])
        self.failIf(login)
        
    def test_expired_activation_key(self):
        '''Activation key should expire in 2 days'''
        self.client.post('/user/register/', self.good_data)

        ua = UserActivation.objects.get(pk=1)

        # key expires somewhere between tomorow and the day after tomorow
        self.assert_(datetime.timedelta(1) <
                     (ua.key_expires - datetime.datetime.today()))
        self.assert_(datetime.timedelta(2) >
                     (ua.key_expires - datetime.datetime.today()))

        # expire it now and see what happens
        ua.key_expires = datetime.datetime.now()
        ua.save()

        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['expired'])
        self.assertTemplateUsed(response, 'confirm.html')

    def test_user_is_authenticated(self):
        '''Authenticated users should be redirected to their profile page
        '''
        self.client.post('/user/register/', self.good_data)

        # activate account before logging in
        ua = UserActivation.objects.get(pk=1)
        ua.user.is_active = True
        ua.user.save()
        
        login = self.client.login(username=self.good_data['username'],
                                  password=self.good_data['password'])
        self.assertTrue(login)
        
        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertRedirects(response, '/user/profile/')

class LoginTests(TestCase):
    # FIXME: the data in the fixtures is rather too tight-coupled
    # with the class attributes
    fixtures = ['one_good_user.json']
    user_name = 'gigel'
    user_pass = 'gigipass'
    
    def test_successful_login(self):
        '''Test successful login and viewing restricted page
        '''
        login = self.client.login(username=self.user_name,
                                  password=self.user_pass)
        self.assertTrue(login)

        response = self.client.get('/user/profile/')
        self.assertEqual(response.status_code, 200)
        
    def test_login_fails_with_bad_credentials(self):
        login = self.client.login(username='badman', password='badpassword')
        self.failIf(login)

    def test_login_form_success(self):
        '''Login using the form and get redirected to the user profile page
        '''
        post_data = {'username':self.user_name,
                     'password':self.user_pass
                     }
        response = self.client.post('/login/', post_data)
        self.assertRedirects(response, '/user/profile/')
        self.failIf('Parola sau numele de utilizator' in response.content)

    def test_user_profile(self):
        login = self.client.login(username=self.user_name,
                                  password=self.user_pass)
        response = self.client.get('/user/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')
        self.failUnless(self.user_name in response.content)
        
    def test_failed_login_using_form(self):
        post_data = {'username':'intruder', 'password':'3l33T'}
        response = self.client.post('/login/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless('Parola sau numele de utilizator' in response.content)

class ProfileTests(TestCase):
    '''Test profile page content(context)
    '''
    fixtures = ['ads.json', 'one_good_user']
    username = 'gigel'
    password = 'gigipass'

    def test_profile(self):
        u = User.objects.all()[0]
        pub1, pub2 = u.publisher_set.all()[:2]

        login = self.client.login(username=self.username,
                                  password=self.password)

        # generate some requests and then create a mockup list
        self.client.get('/serve/%s/' % pub1.slug)
        self.client.get('/serve/%s/' % pub1.slug,
                        HTTP_REFERER=DEFAULTURL)
        self.client.get('/serve/%s/' % pub2.slug,
                        HTTP_REFERER=pub2.url)
        self.client.get('/serve/%s/' % pub2.slug)
        pub_imp = [[pub1.name, pub1.slug, 2, 1],
                   [pub2.name, pub2.slug, 2, 1]]

        self.response = self.client.get('/user/profile/')
        
        self.assertEqual(len(self.response.context['pub_imp']),
                         Publisher.objects.filter(
                             owner__username=self.username).count())
#        self.assertEqual(self.response.context['domain'], DEFAULTURL)
        self.assertEqual(self.response.context['pub_imp'], pub_imp)
        
    def test_delete_publisher(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        user = User.objects.filter(username=self.username)
        p = Publisher.objects.filter(owner=user)[0]
        pid = p.id
        self.client.get('/user/pub/remove/%s' % p.slug)
        self.assertEqual(Publisher.objects.filter(id=pid).count(), 0)
