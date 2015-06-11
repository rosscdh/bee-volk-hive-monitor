# -*- coding: utf-8 -*-
from django.conf import settings
# from django.core.management import call_command
from django.test.simple import DjangoTestSuiteRunner

# from rainbowrunners.djrunner import NyanCatDiscoverRunner

# class AppTestRunner(NyanCatDiscoverRunner, DjangoTestSuiteRunner):
class AppTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        # not args passed in
        if not test_labels:
            test_labels = []
            # Remove path info and use only the app "label"
            for app in settings.PROJECT_APPS:
                app_name = app.split('.')[-1]
                test_labels.append(app_name)
            test_labels = tuple(test_labels)

        return super(AppTestRunner, self).build_suite(test_labels, *args, **kwargs)

    def setup_test_environment(self, *args, **kwargs):
        from django.db.models.loading import get_models
        #
        # Change all unmanaged models to use the default database for testing
        #
        self.unmanaged_models = [m for m in get_models()
                                 if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
            m.objects.__class__._db_original = m.objects.__class__._db
            m.objects.__class__._db = 'default'

        super(AppTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False
            m.objects.__class__._db = m.objects.__class__._db_original
        super(AppTestRunner, self).teardown_test_environment(*args, **kwargs)
