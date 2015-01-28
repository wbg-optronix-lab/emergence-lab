# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.contrib.auth import get_user_model
from django import forms
from django.test import TestCase

from model_mommy import mommy
import six

from core.forms import (ChecklistForm, SampleForm, SampleSelectOrCreateForm,
                        SubstrateForm, TrackProjectForm)
from core.models import Project, Sample, Substrate


class TestSubstrateForm(unittest.TestCase):

    def test_clean_empty(self):
        form = SubstrateForm(data={})
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('__all__'))
        self.assertListEqual(errors.get('__all__'),
            ['Cannot leave all fields blank.'])

    def test_clean_single_specified(self):
        form = SubstrateForm(data={
            'comment': 'test',
        })
        errors = dict(form.errors)
        self.assertDictEqual(errors, {})


class TestSampleForm(TestCase):

    def test_save(self):
        substrate = mommy.make(Substrate)
        form = SampleForm(data={
            'substrate': substrate.id,
            'comment': 'test',
        })
        self.assertDictEqual(dict(form.errors), {})
        sample = form.save()
        self.assertEqual(sample.substrate_id, substrate.id)
        self.assertEqual(sample.comment, 'test')


class TestSampleSelectOrCreateForm(TestCase):

    def test_clean_specify_nonexistant_sample(self):
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': 's0001',
        })
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('sample_uuid'))
        self.assertListEqual(errors.get('sample_uuid'),
                             ['Sample s0001 not found'])

    def test_clean_specify_existing(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': sample.uuid,
        })
        errors = dict(form.errors)
        self.assertDictEqual(errors, {})

    def test_clean_specify_existing_and_new(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': sample.uuid,
            'sample_comment': 'sample comment',
            'substrate_comment': 'substrate comment',
            'substrate_serial': 'substrate serial',
            'substrate_source': 'substrate source',
        })
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('__all__'))
        self.assertListEqual(errors.get('__all__'),
                             ['Existing sample cannot be specified in '
                              'addition to creating a new sample'])

    def test_clean_new_sample(self):
        form = SampleSelectOrCreateForm(data={
            'sample_comment': 'sample comment',
            'substrate_comment': 'substrate comment',
            'substrate_serial': 'substrate serial',
            'substrate_source': 'substrate source',
        })
        errors = dict(form.errors)
        self.assertDictEqual(errors, {})

    def test_clean_empty(self):
        form = SampleSelectOrCreateForm(data={})
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('__all__'))
        self.assertListEqual(errors.get('__all__'),
            ['Cannot leave all fields blank.'])


class TestTrackProjectForm(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        cls.user = User.objects.create_user('username', password='')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()

    def test_save(self):
        project = mommy.make(Project)
        form = TrackProjectForm(data={
            'project': project.id,
            'is_owner': True,
        })
        tracking = form.save(user=self.user)
        self.assertEqual(project.id, tracking.project_id)
        self.assertEqual(self.user.id, tracking.user_id)
        self.assertTrue(tracking.is_owner)


class TestChecklistForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class TestChecklistForm(ChecklistForm):
            checklist_fields = [
                'first',
                'second',
                'third',
                'fourth',
            ]
        cls.form_class = TestChecklistForm

    def test_init(self):
        form = self.form_class()
        for i, ((name, field), label) in enumerate(zip(six.iteritems(form.fields),
                                                   self.form_class.checklist_fields)):
            self.assertEqual('field_{}'.format(i), name)
            self.assertEqual(field.label, label)
            self.assertTrue(field.required)
            self.assertEqual(field.__class__, forms.BooleanField)
