"""
Views for bulk operation status tracking.
"""
from celery.result import AsyncResult
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_bulk_drf.bulk_cache import BulkOperationCache


class BulkOperationStatusView(APIView):
    """
    API view to check the status of bulk operations.
    """

    def get(self, request, task_id):
        """
        Get the status and results of a bulk operation task.

        Args:
            task_id: The Celery task ID

        Returns:
            Task status, results, and progress information
        """
        try:
            task_result = AsyncResult(task_id)
        except (ValueError, TypeError) as exc:
            msg = "Task not found"
            raise Http404(msg) from exc

        # Try to get cached progress first
        progress_data = BulkOperationCache.get_task_progress(task_id)
        cached_result = BulkOperationCache.get_task_result(task_id)

        if task_result.state == "PENDING":
            response_data = {
                "task_id": task_id,
                "state": task_result.state,
                "status": "Task is pending execution",
                "progress": progress_data,
            }
        elif task_result.state == "PROGRESS":
            response_data = {
                "task_id": task_id,
                "state": task_result.state,
                "progress": progress_data or {
                    "current": task_result.info.get("current", 0),
                    "total": task_result.info.get("total", 1),
                    "percentage": 0,
                    "message": task_result.info.get("status", ""),
                },
            }
        elif task_result.state == "SUCCESS":
            # Use cached result if available, otherwise use Celery result
            result = cached_result or task_result.result
            response_data = {
                "task_id": task_id,
                "state": task_result.state,
                "result": result,
                "progress": progress_data,
                "status": "Task completed successfully",
            }
        else:
            # Task failed
            response_data = {
                "task_id": task_id,
                "state": task_result.state,
                "error": str(task_result.info),
                "result": cached_result,
                "status": "Task failed",
            }

        return Response(response_data, status=status.HTTP_200_OK)
