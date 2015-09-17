from milestones import (MilestoneListView,
                        MilestoneCreateView,
                        MilestoneDetailView,
                        MilestoneUpdateView,
                        MilestoneCloseView,
                        MilestoneReOpenView,
                        MilestoneNoteAction,
                        )
from literature import (MendeleyOAuth,
                        MendeleyLibrarySearchView,
                        LiteratureLandingView,
                        AddMendeleyObjectView,
                        LiteratureRedirectorView,
                        AddLiteratureObjectView,
                        CreateLiteratureObjectView,
                        LiteratureDetailView,
                        LiteratureDetailRedirector,
                        MendeleyDetailView,
                        MendeleySearchErrorView,)
from investigations import (InvestigationListView,
                            InvestigationDetailView,
                            InvestigationUpdateView,
                            InvestigationCreateView,)
from projects import (ProjectListView,
                      ProjectUpdateView,
                      ProjectDetailView,
                      AddUserToProjectGroupView,
                      RemoveUserFromProjectGroup,)
from tasks import (TaskListView,
                   TaskCreateView,
                   TaskCloseView,
                   TaskReOpenView,
                   TaskCreateAction,)
from utility import (LandingPageView,
                     NewsfeedView,)
