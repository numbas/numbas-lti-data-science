from django.conf import settings
from django.contrib import admin

from .models import Subtopic, Topic, CaseStudy, CaseStudyTopic
from numbas_lti.models import Resource

class CaseStudyTopicInline(admin.TabularInline):
    model = CaseStudyTopic

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    inlines = [ CaseStudyTopicInline ]

class SubtopicInline(admin.TabularInline):
    model = Subtopic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [ SubtopicInline ]

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'resource':
            kwargs['queryset'] = Resource.objects.filter(lti_13_links__context__in=settings.NCL_DATA_SCIENCE_CONTEXTS)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
