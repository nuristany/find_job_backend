from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    #permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='result')
    def result(self, request, pk=None):
        job = self.get_object()

        # Check if the job is completed
        if job.status != Job.STATUS_COMPLETED:
            raise PermissionDenied("Results are only available for completed jobs.")
        
        # Return the job's status directly
        return Response({
            "status": job.status
        })



