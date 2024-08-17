
from rest_framework import serializers
from django.utils import timezone
from .models import Job
from datetime import datetime, timedelta
from job.tasks import process_job




class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField()
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'posted_by', 'created_at', 'updated_at', 'scheduled_time', 'status']
        read_only_fields = ['posted_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        job = Job.objects.create(posted_by=user, **validated_data)
        
        # Schedule the Celery task for job processing
        if job.scheduled_time:
            # If the job has a scheduled time, use that time
            process_job.apply_async((job.id,), eta=job.scheduled_time)
        else:
            # If no scheduled time, run immediately
            process_job.delay(job.id)
        
        return job

    def validate_scheduled_time(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Scheduled time cannot be in the past.")
        return value




