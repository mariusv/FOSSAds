# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from cuZmeura.ads.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Advertiser'
        db.create_table('ads_advertiser', (
            ('id', orm['ads.Advertiser:id']),
            ('name', orm['ads.Advertiser:name']),
            ('url', orm['ads.Advertiser:url']),
        ))
        db.send_create_signal('ads', ['Advertiser'])
        
        # Adding model 'AdSize'
        db.create_table('ads_adsize', (
            ('id', orm['ads.AdSize:id']),
            ('name', orm['ads.AdSize:name']),
            ('size', orm['ads.AdSize:size']),
        ))
        db.send_create_signal('ads', ['AdSize'])
        
        # Adding model 'Publisher'
        db.create_table('ads_publisher', (
            ('id', orm['ads.Publisher:id']),
            ('name', orm['ads.Publisher:name']),
            ('slug', orm['ads.Publisher:slug']),
            ('url', orm['ads.Publisher:url']),
            ('owner', orm['ads.Publisher:owner']),
        ))
        db.send_create_signal('ads', ['Publisher'])
        
        # Adding model 'Ad'
        db.create_table('ads_ad', (
            ('id', orm['ads.Ad:id']),
            ('name', orm['ads.Ad:name']),
            ('url', orm['ads.Ad:url']),
            ('image', orm['ads.Ad:image']),
            ('advertiser', orm['ads.Ad:advertiser']),
            ('size', orm['ads.Ad:size']),
        ))
        db.send_create_signal('ads', ['Ad'])
        
        # Adding model 'Impression'
        db.create_table('ads_impression', (
            ('id', orm['ads.Impression:id']),
            ('ip', orm['ads.Impression:ip']),
            ('timestamp', orm['ads.Impression:timestamp']),
            ('referer', orm['ads.Impression:referer']),
            ('referer_netloc', orm['ads.Impression:referer_netloc']),
            ('publisher', orm['ads.Impression:publisher']),
            ('ad', orm['ads.Impression:ad']),
        ))
        db.send_create_signal('ads', ['Impression'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Advertiser'
        db.delete_table('ads_advertiser')
        
        # Deleting model 'AdSize'
        db.delete_table('ads_adsize')
        
        # Deleting model 'Publisher'
        db.delete_table('ads_publisher')
        
        # Deleting model 'Ad'
        db.delete_table('ads_ad')
        
        # Deleting model 'Impression'
        db.delete_table('ads_impression')
        
    
    
    models = {
        'ads.ad': {
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Advertiser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.AdSize']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'ads.adsize': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'size': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'ads.advertiser': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'ads.impression': {
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Ad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'publisher': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'referer_netloc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ads.publisher': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
