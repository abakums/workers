from django.views import generic
from .models import Worker
from .generate import generate_workers


class WorkersListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.get(chief=None)
    context_object_name = 'tree_from_list'
    template_name = 'workers_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {'tree_from_list': self.queryset.generate_tree_from_node()}
