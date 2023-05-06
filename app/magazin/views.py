from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from django.contrib.auth import logout, login as Login


class Index(DataMixin, ListView):
    model = Product
    template_name = 'magazin/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна')
        return dict(list(context.items()) + list(c_def.items()))


class Shop(DataMixin, ListView):
    model = Product
    template_name = 'magazin/shop.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Товари')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):   # будут показываться только те статьи которые отмечены для публикации
        return Product.objects.filter(is_published=True).select_related('saleornew')


class ShowPost(LoginRequiredMixin, DataMixin, DeleteView):     # LoginRequiredMixin не показывает данную страницу не авторизованому пользователю, для функций используется дерокатор login_required
    model = Product
    template_name = 'magazin/shop-details.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    # login_url = reverse_lazy('home')      # перенаправляет не зарегестрированого пользователя на нужную страницу
    raise_exception = True      # генерирует страницу 403 доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        c_defs = self.get_user_context(postphoto=PostPhoto.objects.filter(product__slug=self.kwargs['post_slug']))
        active_photo = self.get_user_context(active_photo=PostPhoto.objects.filter(product__slug=self.kwargs['post_slug'])[0])
        return dict(list(context.items()) + list(c_def.items()) + list(c_defs.items()) + list(active_photo.items()))

    # def get_queryset(self):
    #     return PostPhoto.objects.filter(product__slug=self.kwargs['category_slug'], is_published=True)


class ShowCategory(DataMixin, ListView):  # ListView возвращает список
    model = Product
    template_name = 'magazin/shop.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = Category.objects.filter(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title=f'Категорія - {title[0]}')
        c_defs = self.get_user_context(cat_selected=self.kwargs['category_slug'])
        return dict(list(context.items()) + list(c_def.items()) + list(c_defs.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'magazin/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'magazin/register.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        Login(self.request, user)   # Login переименован
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


# @login_required
def blog(request):
    return render(request, 'magazin/blog.html', {'title': 'Блог', 'menu': menu})


def contacts(request):
    return render(request, 'magazin/contacts.html', {'title': 'Контакти', 'menu': menu})


def about(request):
    return render(request, 'magazin/about.html', {'title': 'Про нас', 'menu': menu, 'l': list(range(1, 9))})


def page_not_found(request, *args, **kwargs):
    return HttpResponseNotFound('<h1>Страница не найдена, долбоеб</h1>')


def shopping_cart(request):
    return render(request, 'magazin/shopping-cart.html', {'title': 'Кошик', 'menu': menu})


def checkout(request):
    return render(request, 'magazin/checkout.html', {'title': 'Оплата', 'menu': menu})

