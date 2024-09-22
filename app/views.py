from django.shortcuts import render, redirect

from django.http import JsonResponse

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/"
    client_class = OAuth2Client

def email_confirmation(request, key):
    return redirect(f"http://localhost:3000/dj-rest-auth/registration/account-confirm-email/{key}")

def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:3000/reset/password/confirm/{uid}/{token}")


from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from .serializers import *

# Create your views here.
class BlogListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 10

#Blogs List
class BlogList(ListAPIView):
    queryset = Blog.objects.all().order_by('-date')
    serializer_class = BlogViewSerializer
    pagination_class = BlogListPagination
    permission_classes = [AllowAny]

#Single Blog view
from urllib.parse import unquote


class BlogView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogViewSerializer
    lookup_field = 'url'
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # Increment the view count
        instance.save(update_fields=['views'])  # Save the updated view count
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#Blogs List
class BlogIndex(ListAPIView):
    queryset = Blog.objects.all().order_by('-date')
    serializer_class = BlogViewSerializer
    permission_classes = [AllowAny]


#Get blog comments
def get_blog_comments(request, url):
    try:
        # Decode the title from URL encoding
        decoded_url = unquote(url)

        # Fetch the blog by its title
        blog = get_object_or_404(Blog, url=decoded_url)

        # Fetch the comments related to the blog
        blog_comments = Comment.objects.filter(blog=blog)
        serializer = CommentGetSerializer(blog_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Blog.DoesNotExist:
        return JsonResponse({'error': 'Blog not found.'}, status=404)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)



#Post comments
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        data = request.data.copy()
        data['user'] = request.user.id
        data['blog'] = blog_id
        data['username'] = request.user.username  # Add username to the data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## add blog
class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##blog functionality end


#Language
class LanguageLists(generics.ListAPIView):
    queryset = ProgrammingLanguage.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]



class TopicsView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        lang_url = self.kwargs['url']
        language = generics.get_object_or_404(ProgrammingLanguage, url=lang_url)
        topics = Topics.objects.filter(language=language)
        return topics


class CodeView(generics.ListCreateAPIView):
    serializer_class = CodeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        code_url = self.kwargs['url']
        topic = generics.get_object_or_404(Topics, url=code_url)
        return CodeSnippet.objects.filter(topic=topic)

#single code view
class CodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSerializer
    lookup_field = 'url'
    permission_classes = [AllowAny]



#Each Tutorial view
class TutorialDetail(generics.ListCreateAPIView):
    serializer_class = TutorialPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tutorial_url = self.kwargs['url']
        tutorial = generics.get_object_or_404(ProgrammingLanguage, url=tutorial_url)
        return TutorialPost.objects.filter(language=tutorial)

#List of each Tutorial Topics
class PostView(generics.ListAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        url = self.kwargs['url']

        post = TutorialPost.objects.filter(url=url)
        return post

#List of Post view
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'url'


class TutorialCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, url):
        data = request.data.copy()
        data['user'] = request.user.id
        data['post'] = url
        data['username'] = request.user.username  # Add username to the data
        serializer = TutorialCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_post_comments(request, url):
    try:
        post_comments = Comment_tutorials.objects.filter(url=url)
        serializer = CommentGetTutSerializer(post_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)



#Blog Post and delete view
class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#Loggedin user Blogs
class BlogsUserListView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        blog = Blog.objects.filter(user=user)
        return blog

#Single blog view of user
class BlogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogViewSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        blog_id = self.kwargs['blog_id']

        user = User.objects.get(id=user_id)
        blog = Blog.objects.get(id=blog_id, user=user)

        return blog



def search_blog(request):
    query = request.GET.get('query', '')
    results = Blog.objects.filter(url__icontains=query)

    # Serialize the blog data
    data = []
    for result in results:
        blog_data = {
            'title': result.title,
            'content': result.content,
            'id': result.id,
            'views': result.views,
            'date': result.date,
            # Serialize user as a dictionary
            'user': {
                'id': result.user.id,
                'username': result.user.username,
                'email': result.user.email,  # Include any other user fields you need
            }
        }
        data.append(blog_data)

    return JsonResponse(data, safe=False)

def search_code(request):
    query = request.GET.get('query', '')
    results = CodeSnippet.objects.filter(url__icontains=query)

    # Serialize the code snippet data
    data = []
    for result in results:
        snippet_data = {
            'title': result.title,
            'content': result.content,
            'code_id': result.code_id,
            'code': result.code,
            # Assuming there's an 'author' field which is a foreign key to the User model
            'user': {
                'id': result.user.id,
                'username': result.user.username,
                'email': result.user.email,  # Include other necessary fields
            } if hasattr(result, 'user') and result.user else None
        }
        data.append(snippet_data)

    return JsonResponse(data, safe=False)



@api_view(['POST'])
@permission_classes([AllowAny])
def contact_handler(request):
    if request.method == "POST":
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Send email to user
            subject = 'THANK YOU FOR CONTACTING ME'
            html_content = render_to_string('contact_html.html', {'name': serializer.data["name"]})
            text_content = strip_tags(html_content)  # Strip the html tag
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [serializer.data["email"]]
            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Send email notification to owner
            subject1 = 'HELLO SIR, YOU GOT A NEW MAIL'
            message1 = f'Hi k satyanarayana chary, Someone contacted you details are:- \nUsername: {serializer.data["name"]},\nEmail: {serializer.data["email"]},\nSubject: {serializer.data["subject"]},\nMessage: {serializer.data["message"]} \n'
            email_from = settings.EMAIL_HOST_USER
            recipient_list1 = ['acadamicfolio@gmail.com']
            send_mail(subject1, message1, email_from, recipient_list1)

            return Response({'message': 'Thanks for contacting me. I will look forward to utilizing this opportunity.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortListCreateView(generics.ListCreateAPIView):
    queryset = Short.objects.all().order_by('-created_at')
    serializer_class = ShortSerializer
    permission_classes = [AllowAny]

@require_GET  # Ensures the view only responds to GET requests
def get_latest_update(request):
    # Fetch the latest update by ordering by date and taking the first result
    latest_update = Latest_update.objects.order_by('-date').first()

    if latest_update:
        # Serialize the latest update to JSON
        data = {
            'update': latest_update.update,
            'date': latest_update.date,
        }
    else:
        # If there are no updates, return a message
        data = {
            'error': 'No updates found',
        }

    return JsonResponse(data)


class ShortListView(generics.ListAPIView):
    serializer_class = ShortSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            return Short.objects.filter(category_id=category_id)
        return Short.objects.all()


class McqTopicsView(generics.ListCreateAPIView):
    serializer_class = McqTopicsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        lang_url = self.kwargs['url']  # Get the language URL from the request
        language = get_object_or_404(ProgrammingLanguage, url=lang_url)
        topics = McqTopics.objects.filter(language=language)
        return topics


class CheckAnswersView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data.get('answers', [])
        correct_count = 0
        total_questions = len(data)

        for answer in data:
            question_id = answer.get('question_id')
            selected_option_id = answer.get('selected_option_id')
            try:
                question = Question.objects.get(id=question_id)
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    correct_count += 1
            except (Question.DoesNotExist, Option.DoesNotExist):
                continue

        return Response({
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'incorrect_answers': total_questions - correct_count,
        })


class QuestionsByTopicView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']  # Fetch the topic ID from the URL
        topic = get_object_or_404(McqTopics, id=topic_id)
        return topic.questions.all()  # Return all questions related to the topic
    
class ModelCountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        counts = {
            'programming_language_count': ProgrammingLanguage.objects.count(),
            'blog_count': Blog.objects.count(),
            'comment_count': Comment.objects.count(),
            'tutorial_post_count': TutorialPost.objects.count(),
            'comment_tutorials_count': Comment_tutorials.objects.count(),
            'topics_count': Topics.objects.count(),
            'code_snippet_count': CodeSnippet.objects.count(),
            'short_count': Short.objects.count(),
            'mcq_topics_count': McqTopics.objects.count(),
            'question_count': Question.objects.count(),
            'option_count': Option.objects.count(),
            'latest_update_count': Latest_update.objects.count(),
            'contact_count': Contact.objects.count(),
        }
        serializer = ModelCountSerializer(data=counts)
        serializer.is_valid()
        return Response(serializer.data)