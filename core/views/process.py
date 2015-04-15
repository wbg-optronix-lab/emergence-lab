# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import groupby

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from braces.views import LoginRequiredMixin

from core.models import Process, Sample, DataFile
from core.forms import DropzoneForm, ProcessCreateForm
from core.polymorphic import get_subclasses


class ProcessDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'core/process_detail.html'
    model = Process
    context_object_name = 'process'
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_context_data(self, **kwargs):
        context = super(ProcessDetailView, self).get_context_data(**kwargs)
        context['samples'] = set(node.get_sample() for node in
                                 self.object.processnode_set.get_queryset())
        context['datafiles'] = {k: list(g)
                                for k, g in groupby(self.object.datafiles.all(),
                                             lambda x: type(x))}
        if type(self.object).name == 'D180 Growth':
            context['readings'] = True
        return context


class ProcessCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/process_create.html'
    model = Process
    fields = ('comment', 'user',)

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class ProcessListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/process_list.html'
    model = Process
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ProcessListView, self).get_context_data(**kwargs)
        context['process_list'] = get_subclasses(Process)
        context['user_list'] = get_user_model().objects.all().filter(is_active=True)
        context['slug'] = self.kwargs.get('slug', 'all')
        context['username'] = self.kwargs.get('username', 'all')
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug', 'all')
        username = self.kwargs.get('username', 'all')
        queryset = super(ProcessListView, self).get_queryset().order_by('-created')
        if username != 'all':
            queryset = queryset.filter(user__username=username)
        if slug != 'all':
            queryset = [i for i in queryset if i.slug == slug]
        return queryset


class ProcessUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'core/process_edit.html'
    model = Process
    context_object_name = 'process'
    lookup_url_kwarg = 'uuid'
    fields = ('comment',)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class CreateUploadProcessView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/process_create.html'

    def get_form(self, form_class):
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        return form_class(pieces=sample.pieces, **self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        pieces = form.cleaned_data['pieces']
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        for piece in pieces:
            sample.run_process(self.object, piece=piece)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class RunProcessView(CreateUploadProcessView):
    model = Process
    form_class = ProcessCreateForm


class UploadFileView(LoginRequiredMixin, generic.CreateView):
    """
    Add files to an existing process
    """
    model = DataFile
    template_name = 'core/process_upload.html'
    form_class = DropzoneForm

    def get_context_data(self, **kwargs):
        context = super(UploadFileView, self).get_context_data(**kwargs)
        context['process'] = self.kwargs['uuid']
        return context

    def form_valid(self, form):
        print('entering form_valid')
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))

        uploaded_file, file_kwargs = self.process_file(process,
                                                       self.request.FILES['file'])
        print('processed file')
        with transaction.atomic():
            self.save_file(process,
                           uploaded_file, self.request.FILES['file'],
                           content_type=None, **file_kwargs)
        print('saved file')
        return JsonResponse({'status': 'success'})

    def process_file(self, process, uploaded_file):
        return (uploaded_file, {})

    def save_file(self, process, processed_file, raw_file, content_type=None, **file_kwargs):
        if content_type is None:
            try:
                content_type = processed_file.content_type
            except AttributeError:
                content_type = 'application/octet-stream'
        obj = self.model.objects.create(data=processed_file,
                                        content_type=content_type,
                                        **file_kwargs)
        obj.processes.add(process)