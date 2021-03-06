# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse_lazy

from ..signals import (ensure_project_slug,)

from jsonfield import JSONField


class Project(models.Model):
    slug = models.SlugField(blank=True)  # blank to allow slug to be auto-generated
    name = models.CharField(null=True, blank=True, max_length=255)
    url = models.URLField(help_text='URL to the resource', max_length=255)
    date_created = models.DateTimeField(auto_now=False,
                                        auto_now_add=True,
                                        db_index=True)
    collaborators = models.ManyToManyField('auth.User',
                                           through='project.ProjectCollaborator',
                                           through_fields=('project', 'user'))

    client = models.ForeignKey('client.Client', null=True, blank=True)

    data = JSONField(default={})

    class Meta:
        ordering = ['name']

    @property
    def is_facebook_feed(self):
        return self.data.get('is_facebook_feed', False)

    @is_facebook_feed.setter
    def is_facebook_feed(self, value):
        self.data['is_facebook_feed'] = value

    @property
    def is_rss_atom(self):
        return self.data.get('is_rss_atom', False)

    @is_rss_atom.setter
    def is_rss_atom(self, value):
        self.data['is_rss_atom'] = value

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse_lazy('project:detail', kwargs={'slug': self.slug})

    def feed(self, playlists=()):
        if not playlists:
            return self.feeditem_set.all()

        else:
            for playlist in self.playlist_set.filter(pk__in=[p.pk for p in playlists]):
                return playlist.feed.all()

#
# Signals
#
pre_save.connect(ensure_project_slug, sender=Project, dispatch_uid='project.pre_save.ensure_project_slug')
