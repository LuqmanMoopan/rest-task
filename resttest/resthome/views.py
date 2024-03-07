from rest_framework.response import Response
from rest_framework.decorators import api_view
from resthome.models import Person
from resthome.serializer import LoginSerializer, PersonSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegisterAPI(APIView):
    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data = _data)

        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.save()

        return Response({'message': 'user created'}, status=status.HTTP_201_CREATED)
    
class LoginAPI(APIView):
    def post(self,request):
        _data = request.data
        serializer = LoginSerializer(data = _data)   

        if not serializer.is_valid(): 
            return Response({'message': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
    
        user = authenticate(username= serializer.data['username'], password= serializer.data['password'])

        if not user:
            return Response({'message': "Invalid"}, status=status.HTTP_404_NOT_FOUND)
    
        token, _= Token.objects.get_or_create(user=user)

        return Response({'message0': 'Login successfull', 'token': str(token)}, status=status.HTTP_200_OK)

class ClassPerson(APIView):
    def get(self, request):
        objPerson = Person.objects.all()
        serializer = PersonSerializer(objPerson, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        return Response("This is a post method from APIView")

@api_view(['GET','POST','PUT'])
def index(request):
    if request.method == 'GET':
        people_detail = {
            'name': 'Luqman',
            'age': 22,
            'job': 'python developer'
        }

        return Response(people_detail)
    elif request.method == 'POST':
        print("THIS IS A POST METHOD")
        return Response("THIS IS A POST METHOD")
    elif request.method == 'PUT':
        print("THIS IS A PUT METHOD")
        return Response("THIS IS A PUT METHOD")

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        objPerson = Person.objects.all()
        serializer = PersonSerializer(objPerson, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data = data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message': 'Person deleted'})
    
class PersonViewSets(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset

        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PersonSerializer(queryset, many= True)
        return Response({'status':200, 'data': serializer.data},status= status.HTTP_204_NO_CONTENT)