# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Actor.calendar'
        db.delete_column('actors_actor', 'calendar_id')


    def backwards(self, orm):
        
        # Adding field 'Actor.calendar'
        db.add_column('actors_actor', 'calendar', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['agenda.Calendar'], unique=True, null=True, blank=True), keep_default=False)


    models = {
        'actors.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registered_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['actors']
