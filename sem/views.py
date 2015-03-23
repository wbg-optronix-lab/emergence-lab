# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.core.urlresolvers import reverse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView,
                                  UpdateView, )
from braces.views import LoginRequiredMixin

from core.models import DataFile, SampleManager
from core.views import ActionReloadView
from .models import SEMScan
from .forms import DropzoneForm
from .response import JSONResponse, response_mimetype
from .image_helper import (convert_tiff,)


class SEMList(LoginRequiredMixin, ListView):
    """
    List the most recent sem data
    """
    model = SEMScan
    template_name = 'sem/sem_list.html'
    paginate_by = 25


class SEMAutoCreate(LoginRequiredMixin, ActionReloadView):
    """
    Creates an sem process to for SEMAddFiles view
    """
    def perform_action(self, request, *args, **kwargs):
        process = SEMScan.objects.create()
        sample = SampleManager().get_by_uuid(self.kwargs['uuid'])
        sample.run_process(process)
        self.process_id = process.id

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sem_files', args=(self.process_id,))


class SEMAddFiles(LoginRequiredMixin, CreateView):
    """
    Add files to an existing sem process
    """
    model = DataFile
    template_name = 'sem/sem_upload.html'
    form_class = DropzoneForm

    def get_context_data(self, **kwargs):
        context = super(SEMAddFiles, self).get_context_data(**kwargs)
        context['process_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        image = self.request.FILES['file']
        # source = get_image_source(image)
        image = convert_tiff(image)
        process = SEMScan.objects.get(id=self.kwargs['pk'])
        with transaction.atomic():
            obj = DataFile.objects.create(data=image,
                                          content_type=image.content_type)
            obj.processes.add(process)
        data = {'status': 'success'}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        return response


class SEMDetail(LoginRequiredMixin, DetailView):
    """
    Detail view of the sem model.
    """
    model = SEMScan
    template_name = 'sem/sem_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SEMDetail, self).get_context_data(**kwargs)
        process = SEMScan.objects.get(id=self.kwargs['pk'])
        context['process_id'] = process.id
        context['sample_siblings'] = []
        context['pocket_siblings'] = []
        context['growth_siblings'] = []
        context['images'] = [i.data for i in process.datafiles.get_queryset()]
        return context


class SEMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_create.html'


class SEMUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_update.html'


class SEMDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting sem data
    """
    model = SEMScan
    template_name = 'sem/sem_delete.html'

    def get_success_url(self):
        return reverse('sem_list')
