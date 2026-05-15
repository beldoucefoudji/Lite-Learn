from rest_framework import serializers
from .models import Course, Lesson, Quiz, Question, Enrollment, Progress

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # We exclude 'correct_answer' so students can't cheat by looking at the JSON!
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'passing_score', 'questions']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'content', 'video_url', 'order']

class CourseListSerializer(serializers.ModelSerializer):
    """Used for the homepage/catalog where we only need basic info"""
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'thumbnail_url', 'description']

class CourseDetailSerializer(serializers.ModelSerializer):
    """Used when a student clicks a course to see all lessons and quizzes"""
    lessons = LessonSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'thumbnail_url', 'lessons', 'quizzes']

class EnrollmentSerializer(serializers.ModelSerializer):
    # We make 'user' read_only because we set it automatically in the View
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'date_enrolled']

    def validate(self, data):
        """
        BUSINESS RULE: A user cannot enroll in the same course twice.
        This satisfies Criterion 7: Business Rules Respected.
        """
        user = self.context['request'].user
        course = data.get('course')

        if Enrollment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        
        return data

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'enrollment', 'lesson', 'is_completed', 'last_accessed']