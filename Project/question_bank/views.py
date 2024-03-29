from .models import Question
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from user.permissions import IsProfessor
from rest_framework.response import Response
from .serializer import AddQuestionSerializer, GetQuestionSerializer, getQuestionSerializer


class AddQuestionView(APIView):
    permission_classes = [IsProfessor]
    def post(self, request,level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        serializer = AddQuestionSerializer(
            data=request.data, context={'request': request,'level':LEVEL_CHOICES[level]})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetQuestionView(APIView):
    permission_classes = [IsProfessor]
    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        questions = Question.objects.filter(
            professor=request.user.professor, level=LEVEL_CHOICES[level])
        serializer = GetQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDetialsView(APIView):
    permission_classes = [IsProfessor]
    def get_object(self, pk):
        try:
            return Question.objects.select_related('chapter').get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, id):
        question = self.get_object(id)
        serializer = getQuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        question = self.get_object(id)
        serializer = AddQuestionSerializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        question = self.get_object(id)
        question.delete()
        return Response("Question is deleted", status=status.HTTP_200_OK)

class DeleteQuestionsView(APIView):
    permission_classes = [IsProfessor]
    def delete(self, request):
        if all(isinstance(x, int) for x in request.data):
            for id in  request.data:
                question = Question.objects.get(id = id)
                question.delete()
            return Response('Questions are deleted', status=status.HTTP_200_OK)
        return Response('Error, please try again', status=status.HTTP_400_BAD_REQUEST)
    