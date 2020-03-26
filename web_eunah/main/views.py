from django.shortcuts import render
from django.shortcuts import redirect
from .models import Photo
from .forms import PhotoForm
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PhotoList(ListView):
    model = Photo

    def get_queryset(self):
        return Photo.objects.order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)

        return context


def home(request):
    return render(request, 'main/home.html')

def login(request):
    return render(request, 'main/login.html')

class PhotoDetail(DetailView):
    model = Photo

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhotoDetail, self).get_context_data(**kwargs)
        return context


class PhotoUpdate(UpdateView):
    model = Photo
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]


def photo_list(request):
    photos = Photo.objects.all
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'main/photo_list.html', {'form': form, 'photos': photos})
