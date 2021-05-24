from django.shortcuts import render
from django.views import generic
from django.conf import settings

LEFT_OR_RIGHT_JSON_KEY = 'left_or_right'
LEFT_JSON_VALUE = 'left'
RIGHT_JSON_VALUE = 'right'
IMG_JSON_KEY = 'img'
TEXT_JSON_KEY = 'text'

# Create your views here.

class RecruitStudentsTemplateView(generic.TemplateView):
    template_name = 'content/recruit-student.html'

class CommonOrdersTemplateView(generic.TemplateView):
    template_name = 'content/common-order.html'

class SpecialProvisionsTemplateView(generic.TemplateView):
    template_name = 'content/special-provisions.html'

class FeeTemplateView(generic.TemplateView):
    template_name = 'content/fee.html'

class AboutTemplateView(generic.TemplateView):
    template_name = 'content/about.html'

class ReviewTemplateView(generic.TemplateView):
    template_name = 'content/review.html'