from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from ..models import Profile, Song, SongPart
from functools import reduce
from django.db.models import Q
import operator

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'musicnotes/index.html'

    def get_queryset(self):
        return self.apply_search()

    def apply_search(self):
        result = Song.objects.all()

        query = self.request.GET.get('q')
        if query:

            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(title__icontains=w) for w in query_list)))

        return result.order_by('title')[:100]


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context


        #context['search_list'] = ItemListView.get_queryset(self)
     # context['total'] = sum(prices)
    

