# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import randint
from time import sleep

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .models import SEMScan
from .forms import DropzoneForm
from .response import JSONResponse, response_mimetype


class SEMList(LoginRequiredMixin, ListView):
    """
    List the most recent sem data
    """
    model = SEMScan
    template_name = 'sem/sem_list.html'
    paginate_by = 25


class SEMDetail(LoginRequiredMixin, DetailView):
    """
    Detail view of the sem model.
    """
    model = SEMScan
    template_name = 'sem/sem_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SEMDetail, self).get_context_data(**kwargs)
        context['sample_siblings'] = []
        context['pocket_siblings'] = []
        context['growth_siblings'] = []
        return context


class SEMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_create.html'


class SEMUpload(LoginRequiredMixin, CreateView):
    """
    View for creation of new sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_upload.html'
    form_class = DropzoneForm

    def form_valid(self, form):
        self.object = form.save()
        #self.object = SEMScan()
        #self.object.image = self.request.FILES.getlist('file')[0]
        #self.object.image_number = 0
        #self.object.image_source = 'esem_600'
        #sleep(0.001*randint(1,99))
        #self.object.select_for_update().save()
        data = {'status': 'success'}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        return response


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
