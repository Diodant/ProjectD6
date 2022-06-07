from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse
from django.views import View
from .tasks import send_mail_for_sub_test
import logging

logger = logging.getLogger(__name__)


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsDetail(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = 'newsdetail'


class NewsSearch(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsCreate(CreateView):
    template_name = 'add.html'
    form_class = PostForm


class NewsUpdate(UpdateView):
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AddNews(PermissionRequiredMixin, NewsCreate):
    permission_required = ('news.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsUpdate):
    permission_required = ('news.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDelete):
    permission_required = ('news.delete_post',)


class IndexView(View):
    def get(self, request):
        # printer.apply_async([10], countdown=10)
        # hello.delay()
        send_mail_for_sub_test.delay()
        return HttpResponse('Hello!')