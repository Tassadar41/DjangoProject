from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .permissions import *
from .forms import *
from .models import *
from .utils import *
from .serializers import *



class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    #paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items())+list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

class WomenViewSet(viewsets.ModelViewSet):
    #queryset = Women.objects.all()
    serializer_class = WomenSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Women.objects.all()[:3]
        return Women.objects.filter(pk=pk)
    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})

class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly,)


class WomenAPIView(APIView):
    def get(self, request):
        women = Women.objects.all()
        return Response({'posts': WomenSerializer(women, many=True).data})

    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #return Response({'post': model_to_dict(post_new)})
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object not found"})

        ser = WomenSerializer(data=request.data, instance=instance)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"post": ser.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Women.objects.get(pk=pk)

        except:
            return Response({"error": "Object not found"})

        instance.delete()
        return Response({"post": "Deleted post: "+str(pk)})

# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.filter(is_published=True).select_related('cat')
#     serializer_class = WomenSerializer



# Create your views here.
# def index(request):  # HttpRequest
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

@login_required()
def about(request):  # HttpRequest
    # return HttpResponse("Страница приложения women.")
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(page_obj)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': "О сайте"})


def categories(request, catid):  # HttpRequest
    return HttpResponse(f"<h1>Статьи по категория<h1> {catid} ")


def archive(request, year):  # HttpRequest
    # raise Http404 #бросаем исключение
    if int(year) > 2020:
        # red = HttpResponseRedirect('/')
        red = redirect('home', permanent=True)  # возвращает 500 если скобки в пути {} а не []
        return red
    return HttpResponse(f"<h1>Архив по годам<h1> {year} ")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             # try:
#             #     #Women.objects.create(**form.cleaned_data)   #для forms.Form а не forms.ModelForm распаковываеь
#             #     form.save()
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Ошибка добавления поста")
#
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

class addPage(LoginRequiredMixin, DataMixin, CreateView):

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    #login_url = '/admin/'
    login_url = reverse_lazy('home')
    #raise_exception = True #403 доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить запись')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

# def contact(request):
#     return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class LoginUser(DataMixin , LoginView):
    form_class = AuthenticationUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin ,CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin ,DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg  для поиска по id
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'],
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat_id=Category.objects.get(slug=cat_slug))
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin ,ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #если нет slug

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория ' + c.name,
                                      cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

def logout_user(request):
    logout(request)
    return redirect('home')