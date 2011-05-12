# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from cuZmeura.ads.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Article'
        db.create_table('ads_article', (
            ('id', orm['ads.article:id']),
            ('title', orm['ads.article:title']),
            ('slug', orm['ads.article:slug']),
            ('created_at', orm['ads.article:created_at']),
            ('published', orm['ads.article:published']),
            ('body', orm['ads.article:body']),
        ))
        db.send_create_signal('ads', ['Article'])
        
        # Changing field 'Impression.referer_netloc'
        # (to signature: django.db.models.fields.URLField(max_length=400, null=True))
        db.alter_column('ads_impression', 'referer_netloc', orm['ads.impression:referer_netloc'])
        
        # Changing field 'Impression.referer'
        # (to signature: django.db.models.fields.URLField(max_length=400, null=True))
        db.alter_column('ads_impression', 'referer', orm['ads.impression:referer'])
        
        # Changing field 'Publisher.slug'
        # (to signature: django.db.models.fields.SlugField(unique=True, max_length=15, db_index=True))
        db.alter_column('ads_publisher', 'slug', orm['ads.publisher:slug'])
        
        # Creating unique_together for [url] on Publisher.
        db.create_unique('ads_publisher', ['url'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [url] on Publisher.
        db.delete_unique('ads_publisher', ['url'])
        
        # Deleting model 'Article'
        db.delete_table('ads_article')
        
        # Changing field 'Impression.referer_netloc'
        # (to signature: django.db.models.fields.URLField(max_length=200, null=True))
        db.alter_column('ads_impression', 'referer_netloc', orm['ads.impression:referer_netloc'])
        
        # Changing field 'Impression.referer'
        # (to signature: django.db.models.fields.URLField(max_length=200, null=True))
        db.alter_column('ads_impression', 'referer', orm['ads.impression:referer'])
        
        # Changing field 'Publisher.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=10, unique=True, db_index=True))
        db.alter_column('ads_publisher', 'slug', orm['ads.publisher:slug'])
        
    
    
    models = {
        'ads.ad': {
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Product']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.AdSize']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'ads.adsize': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'size': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'ads.article': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'ads.impression': {
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Ad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'publisher': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True'}),
            'referer_netloc': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ads.product': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ads.publisher': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'ads.useractivation': {
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['ads']
