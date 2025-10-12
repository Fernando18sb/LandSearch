from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


from .models import House, HouseImage

class HouseListView(ListView):
    model = House
    template_name = 'blog/index.html'
    context_object_name = 'houses'
    ordering = ['-pub_date']
    paginate_by = 10

class UserHouseListView(ListView):
    model = House
    template_name = 'blog/user_houses.html'
    context_object_name = 'houses'
    ordering = ['-pub_date']
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return House.objects.filter(owner=user)

class HouseDetailView(DetailView):
    model = House

    def get_object(self, queryset=None):
        access_hash = self.kwargs.get('access_hash')
        return get_object_or_404(House, access_hash=access_hash)

class HouseCreateView(LoginRequiredMixin, CreateView):
    model = House
    fields = [
                'title', 'description',
                'length','width', 'faces', 'state',
                'district', 'municipality', 'latitude',
                'longitude', 'operationType', 'price',
                'status', 'available_from',
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        for file in self.request.FILES.getlist("images"):
            HouseImage.objects.create(house=self.object, image=file)

        return response

    def get_success_url(self):
        return reverse("detail", kwargs={"access_hash": self.object.access_hash})

class HouseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = House
    fields = [
        'title', 'description', 'length', 'width',
        'faces', 'state', 'district', 'municipality',
        'latitude', 'longitude', 'operationType', 'price',
        'status', 'available_from',
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.owner:
            return True
        return False

    def get_object(self, queryset=None):
        access_hash = self.kwargs.get('access_hash')
        return get_object_or_404(House, access_hash=access_hash)

class HouseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = House
    success_url = 'blog'

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.owner:
            return True
        return False

    def get_object(self, queryset=None):
        access_hash = self.kwargs.get('access_hash')
        return get_object_or_404(House, access_hash=access_hash)


