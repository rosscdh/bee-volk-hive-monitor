# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Project


class ProjectTest(TestCase):
    subject = Project

    def test_model_gets_slug_automatically(self):
        project = mommy.make('project.Project', name='I should be turned into a slug')
        self.assertEqual(project.slug, 'i-should-be-turned-into-a-slug')
