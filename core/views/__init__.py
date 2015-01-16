# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .utility import (ActiveListView,
                      ActionReloadView,
                      ExceptionHandlerView,
                      HomepageView,
                      ProtectedMediaView,
                      QuickSearchRedirectView)
from .user import (ActivateUserRedirectView,
                   DeactivateUserRedirectView,
                   UserListView)
from .project import (ActivateProjectRedirectView,
                      DeactivateProjectRedirectView,
                      ProjectCreateView,
                      ProjectDetailView,
                      ProjectListView,
                      ProjectUpdateView,
                      TrackProjectRedirectView,
                      TrackProjectView,
                      UntrackProjectRedirectView,
                      ActivateInvestigationRedirectView,
                      DeactivateInvestigationRedirectView,
                      InvestigationCreateView,
                      InvestigationDetailView,
                      InvestigationListView,
                      InvestigationUpdateView)
