from rest_framework import viewsets, permissions
from .models import Course, Lesson, Quiz, Enrollment, Progress
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, EnrollmentSerializer, 
    LessonSerializer, ProgressSerializer, QuizSerializer, QuestionSerializer
    
)

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes all courses to any logged-in user.
    ReadOnly because students don't create courses; only Admins do.
    """
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    CRITICAL: Criterion 1 Requirement - Filtering by owner 
    A student should only see their own enrollments.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # We will define the serializer for this soon

    def get_queryset(self):
        # Only returns enrollments belonging to the logged-in user 
        return Enrollment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user when enrolling
        serializer.save(user=self.request.user)