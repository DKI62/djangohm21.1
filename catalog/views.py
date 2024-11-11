from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from .forms import BlogPostForm
from .models import Product, BlogPost


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'object_list'


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}, ({email}): {message}')
        return self.render_to_response(self.get_context_data())


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        # Фильтруем только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # Увеличиваем счетчик просмотров
        self.object.views_count += 1
        self.object.save()  # Сохраняем изменения в базе данных
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'catalog/blogpost_form.html'

    def form_valid(self, form):
        # Сохраняем статью
        new_blog = form.save(commit=False)
        # Генерация slug на основе заголовка
        new_blog.slug = slugify(new_blog.title)
        new_blog.save()  # Сохраняем статью с уникальным slug
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'slug': self.object.slug})


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'catalog/blogpost_form.html'

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'slug': self.object.slug})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'

    def get_success_url(self):
        return reverse('catalog:blogpost_list')


# Функция для отправки письма
def send_congratulation_email(post):
    subject = 'Поздравляем с 100 просмотров!'
    message = f"Поздравляем! Ваша статья '{post.title}' достигла 100 просмотров!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['your-email@yandex.ru']  # Тот же email для получения уведомления

    send_mail(subject, message, from_email, recipient_list)


# Сигнал для отслеживания количества просмотров
@receiver(post_save, sender=BlogPost)
def check_views_count(sender, instance, created, **kwargs):
    # Проверяем, если статья была обновлена, а не создана
    if not created and instance.views_count >= 100:
        send_congratulation_email(instance)
