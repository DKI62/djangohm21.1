from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProductListView, ProductDetailView, ContactView, BlogPostListView, BlogPostDetailView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('blog/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blog/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blog/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
