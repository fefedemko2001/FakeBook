from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from book.views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name = 'book-home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('book/', include('book.urls')),
    path('friends/', include('friends.urls')),
    path('chats/', include('chat.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)