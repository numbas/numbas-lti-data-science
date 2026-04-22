from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.utils.translation import gettext_lazy as _, gettext

from .models import CaseStudy, Topic

from numbas_lti.models import Resource, Attempt
import numbas_lti.views.lti_13
from numbas_lti.views.lti_13 import resource_launch_handlers, MustBeDeepLinkMixin
from numbas_lti.views.mixins import reverse_with_lti

class IndexView(generic.TemplateView):
    template_name = 'ncl_data_science/index.html'

class CaseStudiesView(generic.ListView):
    model = CaseStudy
    template_name = 'ncl_data_science/case_studies.html'
    context_object_name = 'case_studies'

    def get_queryset(self):
        objects = super().get_queryset()
        return [(case_study, case_study.progress_for_user(self.request.user)) for case_study in objects]


class TopicsView(generic.ListView):
    model =  Topic
    template_name = 'ncl_data_science/topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        objects = super().get_queryset()
        return [(topic, topic.progress_for_user(self.request.user)) for topic in objects]


class TopicView(generic.DetailView):
    model = Topic
    template_name = 'ncl_data_science/topic.html'
    context_object_name = 'topic'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        topic = self.object

        context['topic_progress'] = topic.progress_for_user(self.request.user)

        context['completion_status'] = topic.progress_for_user(self.request.user)

        context['subtopics'] = [(subtopic, subtopic.progress_for_user(self.request.user)) for subtopic in topic.subtopics.all()]

        case_studies = topic.case_studies.all()
        context['case_studies'] = [(case_study, case_study.progress_for_user(self.request.user)) for case_study in case_studies]

        return context

def handle_data_science_launch(view, *args, **kwargs):
    page = view.get_custom_param('page')
    args = ()
    if page == 'topic':
        args = (view.get_custom_param('topic'),)
    return redirect(view.reverse_with_lti(f'ncl_data_science:{page}', args=args))

resource_launch_handlers['ncl_data_science'] = handle_data_science_launch


class DeepLinkView(MustBeDeepLinkMixin, generic.TemplateView):
    template_name = 'ncl_data_science/deep_link.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['topics'] = Topic.objects.all()

        return context

def deep_link_options(view):
    context, resource_link_id = view.get_lti_context()

    if context.pk in settings.NCL_DATA_SCIENCE_CONTEXTS:
        yield ('ncl_data_science:deep_link', _('Data science material'))

numbas_lti.views.lti_13.DeepLinkView.extra_options.append(deep_link_options)
