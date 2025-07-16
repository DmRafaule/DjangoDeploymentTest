from django.shortcuts import render
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from django.http.response import HttpResponse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination

from .models import Post, Tag, Media
from .forms import PostModelForm, TagModelForm, MediaModelForm

class CustomNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = 4

class ListView(
    generics.mixins.ListModelMixin, 
    generics.mixins.CreateModelMixin, 
    generics.mixins.DestroyModelMixin, 
    generics.mixins.UpdateModelMixin, 
    generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Backend/Parts/pagination.html'
    pagination_class = CustomNumberPagination
    model_form = PostModelForm
    call_root = 'posts'
    model_inst_rend_templ="Backend/Parts/post.html"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'queryset': list(self.filter_queryset(self.get_queryset()))})
        return context

    def get(self, request, *args, **kwargs):
        ''' Получить список постов '''
        queryset = self.get_queryset()
        posts = []
        if queryset is not None:
            posts = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(posts)
        if page is not None:
            return Response({
                "posts": page,
                "post_form": self.model_form,
                "call_root": self.call_root,
                "model_inst_rend_templ": self.model_inst_rend_templ,
                "next_link": self.paginator.get_next_link(),
                "prev_link": self.paginator.get_previous_link(),
            })

        return Response({"posts": page})

    def post(self, request, *args, **kwargs):
        ''' Добавить пост '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        form = self.model_form(request.POST, request.FILES)
        if form.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            posts = []
            if self.get_queryset() is not None:
                posts = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(posts)
            return Response({
                "to_update": True,
                'messages': [_("Успешно добавил пост")] },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            headers = self.get_success_headers(serializer.data)
            posts = []
            if self.get_queryset() is not None:
                posts = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(posts)
            return Response({
                "to_update": True,
                'messages': [_("Не удалось добавить пост")] },
                status=status.HTTP_204_NO_CONTENT,
                headers=headers
            )


    def put(self, request, *args, **kwargs):
        ''' Изменить пост '''
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ''' Удалить пост '''
        return self.destroy(request, *args, **kwargs)
    
class DetailedView(
    generics.RetrieveAPIView, 
    generics.DestroyAPIView, 
    generics.UpdateAPIView, 
    generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Backend/Parts/post.html'
    model_form = PostModelForm

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'post': instance})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'is_delete': True})

    def put(self, request, *args, **kwargs):
        messages = []
        messages.append(_("Что-то пошло не так. Не смог обновить фид. ＼（〇_ｏ）／"))
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        form =  self.model_form(serializer.data)
        if form.is_valid():
            messages[0] = _("Успешно обновил пост. （￣︶￣）↗　")
            return Response({
                'post': instance,
                'messages': messages
            })
        else:
            messages[0] = _("Не смог обновить пост, неправильно заполненна форма.")
            return Response({
                'post_edit_form': form,
                'pk': instance.pk,
                'messages': messages
            })

class PostListView(ListView):
    ''' Представление для пагинации объектов модели Post '''

    def get_queryset(self):
        ''' Отфильтровать объекты модели Post по тегам '''
        queryset = self.queryset.order_by('-timeCreated') 
        tags_str: list[str] = self.request.query_params.getlist('tag')
        tags = Tag.objects.filter(slug__in=tags_str)
        for tag in tags:
            queryset = queryset.filter(tags=tag)
        return queryset

class PostDetailedView(DetailedView):
    ''' Представление для работы с отдельными объектами модели Tag '''
    pass


class TagListView(ListView):
    ''' Представление для пагинации объектов модели Tag '''

    # Какую форму использовать для создания, редактирования объекта модели Media
    model_form = TagModelForm
    # Суффикс для вызова соответствующих представлений
    call_root = 'tags'
    # Какой шаблон использовать для рендеринга одного объекта модели Tag
    model_inst_rend_templ="Backend/Parts/tag.html"

    def get_queryset(self):
        ''' Отфильтровать Tag объекты '''
        queryset = self.queryset.order_by('name')
        return queryset

class TagDetailedView(DetailedView):
    ''' Представление для работы с отдельными объектами модели Tag '''

    # Какой шаблон использовать для рендеринга одного объекта модели Tag
    template_name = 'Backend/Parts/tag.html'
    # Какую форму использовать для создания, редактирования объекта модели Tag
    model_form = TagModelForm


class MediaListView(ListView):
    ''' Представление для пагинации объектов модели Media '''

    # Какую форму использовать для создания, редактирования объекта модели Media
    model_form = MediaModelForm
    # Суффикс для вызова соответствующих представлений
    call_root = 'medias'
    # Какой шаблон использовать для рендеринга одного объекта модели Media
    model_inst_rend_templ="Backend/Parts/media.html"

    def get_queryset(self):
        ''' Отфильтровать Media объекты '''
        queryset = self.queryset.order_by('name')
        return queryset

class MediaDetailedView(DetailedView):
    ''' Представление для работы с отдельными объектами модели Media '''

    # Какой шаблон использовать для рендеринга одного объекта модели Media
    template_name = 'Backend/Parts/media.html'
    # Какую форму использовать для создания, редактирования объекта модели Media
    model_form = MediaModelForm

def get_post_form(request, pk: int):
    ''' Возвращет форму создания постов (Post - модель) '''
    post = Post.objects.get(pk=pk)
    post_form = PostModelForm(instance=post)
    return render(request, 'Backend/Parts/post.html', context={'post_edit_form': post_form, 'pk': post.pk})

def get_tag_form(request, pk: int):
    ''' Возвращет форму создания тегов (Tag - модель) '''
    tag = Tag.objects.get(pk=pk)
    tag_form = TagModelForm(instance=tag)
    return render(request, 'Backend/Parts/tag.html', context={'post_edit_form': tag_form, 'pk': tag.pk})

def get_media_form(request, pk: int):
    ''' Возвращет форму создания медиа (Media - модель) '''
    media = Media.objects.get(pk=pk)
    media_form = MediaModelForm(instance=media)
    return render(request, 'Backend/Parts/media.html', context={'post_edit_form': media_form, 'pk': media.pk})

def remove_part(request):
    return HttpResponse("")