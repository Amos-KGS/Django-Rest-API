from django.urls import path
from . import views as uv
from  rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', uv.api_entry),
    # class-based urls (APIView)
    path('books1/', uv.allbooks.as_view(), name='bookall'),
    path('books1/<int:pk>/', uv.bookdetail.as_view()),

    # function-based urls(@api_view)
    path('books/', uv.allbookdata),
    path('books/<int:pk>/', uv.bookdetaildata),

    # class-based urls (mixins)
    path('books2/', uv.bookall.as_view()),
    path('books2/<int:pk>/', uv.detailbook.as_view()),

    # class-based urls (generic)
    path('books3/', uv.bookalldata.as_view()),
    path('books3/<int:pk>/', uv.detailbookdata.as_view()),

    path('users/', uv.UserAll.as_view(), name='userall'),
    path('users/<int:pk>/', uv.UserDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)