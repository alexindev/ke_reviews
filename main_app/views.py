from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data()
        context['title'] = 'KE Services'
        return context


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
