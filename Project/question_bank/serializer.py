from rest_framework import serializers
from .models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'is_correct']


class AddQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'chapter', 'text', 'degree', 'difficulty',
                    'is_true_false', 'in_practice', 'answer']

    def create(self, validated_data):
        answers = validated_data.pop('answer')
        professor = self.context['request'].user.professor
        question = Question.objects.create(professor=professor, **validated_data)
        for obj in answers:
            new_obj = Answer()
            new_obj.question = question
            new_obj.answer = obj.pop('answer')
            new_obj.is_correct = obj.pop('is_correct')
            new_obj.save()
        return question

    def update(self, instance, validated_data):
        answer_data = validated_data.pop('answer')
        answers = (instance.answer).all()
        answers = list(answers)
        instance.text = validated_data.get('text', instance.text)
        instance.chapter = validated_data.get('chapter', instance.chapter)
        instance.difficulty = validated_data.get(
            'difficulty', instance.difficulty)
        instance.degree = validated_data.get('degree', instance.degree)
        instance.is_true_false = validated_data.get(
            'is_true_false', instance.is_true_false)
        instance.in_practice = validated_data.get(
            'in_practice', instance.in_practice)
        instance.save()
        for obj in answer_data:
            answer = answers.pop(0)
            answer.answer = obj.get('answer', answer.answer)
            answer.is_correct = obj.get('is_correct', answer.is_correct)
            answer.save()
        return instance


class GetQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(max_length=255)
    difficulty = serializers.CharField(max_length=10)
    degree = serializers.IntegerField()
    chapter = serializers.CharField(max_length=255, source="chapter_id")
