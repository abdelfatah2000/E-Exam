from django.http import Http404
from rest_framework import status
from .permissions import IsStudent
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Professor_Student, Professor_Level, User
from .serializers import StudentCreateSerializer, GetAllProfessorsSerializer, StudentProfileSerializer, StudentRequestSerializer,GetMyProfessorsSerializer


class StudentCreateView(APIView):
    def post(self, request):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllProfessorView(APIView):
    permission_classes = [IsStudent]
    def get(self, request):
        my_professors = Professor_Student.objects.filter(
            student__user=request.user).values('professor')
        professors = Professor_Level.objects.select_related('professor').filter(level=request.user.student.level).exclude(professor__in=my_professors).values(
            'professor', 'professor__user__first_name', 'professor__user__last_name', 'professor__avatar')
        serializer = GetAllProfessorsSerializer(professors, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentRequestView(APIView):
    permission_classes = [IsStudent]
    def post(self, request):
        serializer = StudentRequestSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentProfileView(APIView):
    permission_classes = [IsStudent]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = StudentProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_object(request.user.id)
        serializer = StudentProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStudentProfessorView(APIView):
    permission_classes = [IsStudent]
    def get(self, request):
        professors = Professor_Student.objects.select_related('professor').filter(student=request.user.student)\
            .values('professor', 'professor__user__first_name', 'professor__user__last_name', 'professor__avatar')
        serializer = GetMyProfessorsSerializer(professors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

