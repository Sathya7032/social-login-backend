

from rest_framework import serializers
from .models import *

        
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ['id', 'name', 'description', 'image' ,'url']
        
class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views','url']


class BlogViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views','url']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeSnippet
        fields = ['code_id', 'title', 'code', 'content', 'topic','url']



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id','topic','url']


class TutorialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialPost
        fields = ['post_id', 'post_title', 'post_content', 'post_file', 'language', 'post_video','url']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class TutorialCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']

class CommentGetTutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

class McqTopicsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = McqTopics
        fields = ['id', 'name', 'language', 'url', 'questions']

class ShortSerializer(serializers.ModelSerializer):
    category = LanguageSerializer()

    class Meta:
        model = Short
        fields = ['id', 'title', 'video_url', 'description', 'created_at', 'views', 'category']
        
class ModelCountSerializer(serializers.Serializer):
    programming_language_count = serializers.IntegerField()
    blog_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    tutorial_post_count = serializers.IntegerField()
    comment_tutorials_count = serializers.IntegerField()
    topics_count = serializers.IntegerField()
    code_snippet_count = serializers.IntegerField()
    short_count = serializers.IntegerField()
    mcq_topics_count = serializers.IntegerField()
    question_count = serializers.IntegerField()
    option_count = serializers.IntegerField()
    latest_update_count = serializers.IntegerField()
    contact_count = serializers.IntegerField()