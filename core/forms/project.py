# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from core.models import Project, ProjectTracking


class TrackProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.active.all())

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        user = kwargs.pop('user')

        instance = super(TrackProjectForm, self).save(commit=False)
        instance.user = user

        if commit:
            instance.save()

        return instance

    class Meta:
        model = ProjectTracking
        fields = ['project', 'is_owner']
