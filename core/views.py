import os

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView, View
import gitlab

from .models import investigation, operator, platter, project, project_tracking
from growths.models import growth, sample


class SessionHistoryMixin(object):
    max_history = 5
    request = None

    def add_breadcrumb_history(self, request):
        history = request.session.get('breadcrumb_history', [])

        if not history or history[-1] != request.path:
            history.append(request.path)

        if len(history) > self.max_history:
            history.pop(0)

        request.session['breadcrumb_history'] = history
        return history

    def get_context_data(self, **kwargs):
        kwargs['breadcrumb'] = self.add_breadcrumb_history(self.request)
        return super(SessionHistoryMixin, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(SessionHistoryMixin, self).dispatch(request, *args, **kwargs)


class ActiveListView(ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.current.all()
        context['inactive_list'] = self.model.retired.all()
        return context


class QuickSearchRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        growth_number = self.request.GET.get('growth', None)
        try:
            growth.get_growth(growth_number)
            return reverse('growth_detail', args=(growth_number,))
        except:
            try:
                obj = sample.get_sample(growth_number)
                return reverse('sample_detail', args=(obj.id,))
            except:
                pass
        return reverse('afm_filter')


class homepage(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


class Dashboard(DetailView):
    """
    Main dashboard for the user with commonly used actions.
    """
    template_name = 'core/dashboard.html'
    model = operator
    object = None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['growths'] = growth.objects.filter(operator=self.object).order_by('-growth_number')[:25]
        projects = growth.objects.filter(operator=self.object).values_list('project', flat=True).distinct()
        context['active_projects'] = project.current.filter(id__in=projects)
        context['inactive_projects'] = project.retired.filter(id__in=projects)
        return context

    def get_object(self, queryset=None):
        return self.object

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = operator.objects.get(user=request.user)
        except:
            self.object = operator(name=request.user.first_name, active=1, user_id=request.user.id)
            self.object.save()
            core_projects = project.objects.filter(core=True).values_list('id', flat=True)
            for proj in core_projects:
                core_project_tracking = project_tracking(operator=self.object, project_id=proj, is_pi=True)
                core_project_tracking.save()
        return super(Dashboard, self).dispatch(request, *args, **kwargs)


def protected_media(request, filename):
    fullpath = os.path.join(settings.MEDIA_ROOT, filename)
    response = HttpResponse(mimetype='image/jpeg')
    response['X-Sendfile'] = fullpath
    return response


class operator_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/operator_list.html"
    model = operator


class operator_create(CreateView):
    """
    View to create operators.
    """
    template_name = "core/operator_create.html"
    model = operator
    fields = ['name']

    def get_success_url(self):
        return reverse('operator_list')


class platter_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/platter_list.html"
    model = platter


class ProjectDetailView(DetailView):
    """
    View for details of a project.
    """
    template_name = 'core/project_detail.html'
    model = project

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = operator.objects.filter(user__username=self.kwargs['username']).values('id')
            context['growths'] = (growth.objects.filter(project=self.object,
                                                        operator_id=userid)
                                                .order_by('-growth_number')[:25])
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
        return context


class project_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = project


class investigation_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = investigation


class ExceptionHandlerView(View):

    def post(self, request, *args, **kwargs):
        path = request.POST.get('path', '')
        user = request.POST.get('user', 0)
        title = request.POST.get('title', 'Exception Form Issue')
        tags = request.POST.getlist('tag[]')
        tags.append('exception-form')
        complaint = request.POST.get('complaint', '')
        if complaint:
            git = gitlab.Gitlab(settings.GITLAB_HOST,
                                token=settings.GITLAB_PRIVATE_TOKEN, verify_ssl=False)
            success = git.createissue(8, title=title, labels=', '.join(tags),
                                      description='User: {0}\nPage: {1}\nProblem: {2}'.format(user, path, complaint))
            if not success:
                raise Exception('Error submitting issue')
        return HttpResponseRedirect(path)
