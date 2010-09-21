# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Band'
        db.create_table('band_band', (
            ('actor_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['actors.Actor'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=40, db_index=True)),
            ('founded_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('genres', self.gf('tagging.fields.TagField')()),
            ('influences', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['world.Place'], null=True, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['minisite.Minisite'], null=True, blank=True)),
            ('technical_sheet', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('band', ['Band'])

        # Adding model 'BandPicture'
        db.create_table('band_bandpicture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pictures', to=orm['band.Band'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_avatar', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('band', ['BandPicture'])

        # Adding model 'BandRole'
        db.create_table('band_bandrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('band', ['BandRole'])

        # Adding model 'BandMember'
        db.create_table('band_bandmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='band_memberships', to=orm['auth.User'])),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(related_name='band_members', to=orm['band.Band'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('band', ['BandMember'])

        # Adding unique constraint on 'BandMember', fields ['user', 'band']
        db.create_unique('band_bandmember', ['user_id', 'band_id'])

        # Adding M2M table for field roles on 'BandMember'
        db.create_table('band_bandmember_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bandmember', models.ForeignKey(orm['band.bandmember'], null=False)),
            ('bandrole', models.ForeignKey(orm['band.bandrole'], null=False))
        ))
        db.create_unique('band_bandmember_roles', ['bandmember_id', 'bandrole_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BandMember', fields ['user', 'band']
        db.delete_unique('band_bandmember', ['user_id', 'band_id'])

        # Deleting model 'Band'
        db.delete_table('band_band')

        # Deleting model 'BandPicture'
        db.delete_table('band_bandpicture')

        # Deleting model 'BandRole'
        db.delete_table('band_bandrole')

        # Deleting model 'BandMember'
        db.delete_table('band_bandmember')

        # Removing M2M table for field roles on 'BandMember'
        db.delete_table('band_bandmember_roles')


    models = {
        'actors.actor': {
            'Meta': {'object_name': 'Actor'},
            'calendar': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['agenda.Calendar']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registered_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'agenda.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'calendars'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['agenda.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'agenda.event': {
            'Meta': {'ordering': "['-event_date', '-start_time', '-title']", 'unique_together': "(('event_date', 'slug'),)", 'object_name': 'Event'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 21, 19, 1, 9, 61302)'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'V'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'band.band': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Band', '_ormbases': ['actors.Actor']},
            'actor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['actors.Actor']", 'unique': 'True', 'primary_key': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'founded_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genres': ('tagging.fields.TagField', [], {}),
            'influences': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bands'", 'symmetrical': 'False', 'through': "orm['band.BandMember']", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.Place']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'technical_sheet': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['minisite.Minisite']", 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'band.bandmember': {
            'Meta': {'unique_together': "(('user', 'band'),)", 'object_name': 'BandMember'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'band_members'", 'to': "orm['band.Band']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'roles'", 'symmetrical': 'False', 'to': "orm['band.BandRole']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'band_memberships'", 'to': "orm['auth.User']"})
        },
        'band.bandpicture': {
            'Meta': {'object_name': 'BandPicture'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': "orm['band.Band']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'band.bandrole': {
            'Meta': {'object_name': 'BandRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'elsewhere.socialnetwork': {
            'Meta': {'object_name': 'SocialNetwork'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'elsewhere.socialnetworkprofile': {
            'Meta': {'object_name': 'SocialNetworkProfile'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'social_network_profiles'", 'to': "orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profiles'", 'to': "orm['elsewhere.SocialNetwork']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'elsewhere.websiteprofile': {
            'Meta': {'object_name': 'WebsiteProfile'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'website_profiles'", 'to': "orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'minisite.layout': {
            'Meta': {'object_name': 'Layout'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template': ('django.db.models.fields.TextField', [], {})
        },
        'minisite.minisite': {
            'Meta': {'object_name': 'Minisite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['minisite.Layout']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'world.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['band']
