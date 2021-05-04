from rest_framework import  status
from rest_framework import serializers
from .models import Book
from .serializers import bookSerializer, UserSerializer
from rest_framework.decorators import api_view, APIView, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins
from rest_framework import  generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from . permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse

# Create your views here.
#                    <-- Entry point of the API -->

@api_view(['GET'])
def api_entry(request, format=None):
    return Response({
        'users': reverse('userall', request=request, format=format),
        'books': reverse('bookall', request=request, format=format)
    })


#                       <-- start of function-based @api_view -->

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])

def allbookdata(request, format=None):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = bookSerializer(books, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = bookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated,IsOwnerOrReadOnly])

def bookdetaildata(request, pk, format=None):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = bookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = bookSerializer(book, data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#                   <-- End of function-based @api_view -->
  
#                   <-- Beginning of Class-based APIView -->

class allbooks(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = bookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = bookSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
  
class bookdetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = bookSerializer(book)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = bookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#                       <-- End of class-bases APIView -->


#                           <-- using mixins -->
class bookall(mixins.ListModelMixin,
            mixins.CreateModelMixin,
            generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = bookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class detailbook(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = bookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#                                       <--End of mixins-->        

#                           <-- Using Generic class-based  views-->

class bookalldata(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    queryset = Book.objects.all()
    serializer_class = bookSerializer

class detailbookdata(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Book.objects.all()    
    serializer_class = bookSerializer

#                       <-- End of Generic class-based views -->  

#           <-- Users generic views -->

class UserAll(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer  