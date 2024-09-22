from django.urls import path
from .views import *


urlpatterns = [
    path('blogs/', BlogList.as_view(), name='blog-list'),
    path('blogsindex/', BlogIndex.as_view(), name='blog-index'),
    path("blogs/<str:url>/",BlogView.as_view(), name='blog'),
    path("blog/<user_id>/", BlogsUserListView.as_view()),
    path("blog/<user_id>/<blog_id>/", BlogsDetailView.as_view()),
    path('blogs/<str:url>/comments/', get_blog_comments, name='get_blog_comments'),
    path('post-blog/', BlogPostCreateView.as_view(), name='post-blog'),
    path('blog/<str:url>/comment/create/', CommentCreateView.as_view(), name='comment_create'),

    path('languages/', LanguageLists.as_view(), name='languages-list'), 
    path('languages/<str:url>/topics/', TopicsView.as_view(), name='topics-details'),
    path('languages/<str:url>/codes/', CodeView.as_view(), name='code-details'),
    path('languages/codes/<str:url>/', CodeDetail.as_view(), name='code-detailsview'),

    path('tutorials/<str:url>/', TutorialDetail.as_view(), name='tutorial-detail'),
    path('post/<str:url>/', PostView.as_view(), name='post-details'),
    path('tutorials/posts/<str:url>/', PostDetail.as_view(), name='post-detailsview'),

    path('search/', search_blog, name='search_model'),
    path('search_code/',search_code, name='search_model'),
    path('shorts/', ShortListCreateView.as_view(), name='shorts-list-create'),
    path('latest-update/', get_latest_update, name='latest-update'),
    path('contact/', contact_handler, name='search_model'),

    path('api/shorts/', ShortListView.as_view(), name='short-list'),
    
    path('mcq-topics/<str:url>/', McqTopicsView.as_view(), name='mcq-topics'),
     # Endpoint to list questions based on the selected topic ID
    path('topics/<int:topic_id>/questions/', QuestionsByTopicView.as_view(), name='questions_by_topic'),

    # Endpoint to check answers submitted by the user
    path('check-answers/', CheckAnswersView.as_view(), name='check_answers'),
    path('model-count/', ModelCountView.as_view(), name='model-count'),
]