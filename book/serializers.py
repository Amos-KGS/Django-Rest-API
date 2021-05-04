from django.db.models.deletion import SET_NULL
from rest_framework import serializers
from . models import  Book
from django.contrib.auth.models import User

class bookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'genre', 'price','created_at']
        # fields = '__all__'

class bookRepr(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title','genre', 'price']

class UserSerializer(serializers.ModelSerializer):
    books = bookRepr(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'books']