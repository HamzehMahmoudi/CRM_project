from django.views import generic


class Index(generic.TemplateView):
    """
    this view show the index page 
    """
    template_name = 'users/index.html'
