"""
Redis-based caching for bulk operation status and progress tracking.
"""
import json
from typing import Any

from django.core.cache import cache


class BulkOperationCache:
    """Redis-based cache for bulk operation status and progress."""

    @staticmethod
    def _make_key(task_id: str, key_type: str = "status") -> str:
        """Generate a cache key for a task."""
        return f"bulk_operation:{task_id}:{key_type}"

    @classmethod
    def set_task_status(cls, task_id: str, status_data: dict[str, Any] | list[dict[str, Any]], timeout: int = 86400) -> None:
        """
        Store task status in Redis.

        Args:
            task_id: The Celery task ID
            status_data: Status information dictionary or list of dictionaries
            timeout: Cache timeout in seconds (default: 24 hours)
        """
        key = cls._make_key(task_id, "status")
        cache.set(key, json.dumps(status_data), timeout)

    @classmethod
    def get_task_status(cls, task_id: str) -> dict[str, Any] | list[dict[str, Any]] | None:
        """
        Retrieve task status from Redis.

        Args:
            task_id: The Celery task ID

        Returns:
            Status information dictionary, list of dictionaries, or None if not found
        """
        key = cls._make_key(task_id, "status")
        cached_data = cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    @classmethod
    def set_task_result(cls, task_id: str, result_data: dict[str, Any] | list[dict[str, Any]], timeout: int = 86400) -> None:
        """
        Store final task result in Redis.

        Args:
            task_id: The Celery task ID
            result_data: Final result data (dict or list of dicts)
            timeout: Cache timeout in seconds (default: 24 hours)
        """
        key = cls._make_key(task_id, "result")
        cache.set(key, json.dumps(result_data), timeout)

    @classmethod
    def get_task_result(cls, task_id: str) -> dict[str, Any] | list[dict[str, Any]] | None:
        """
        Retrieve final task result from Redis.

        Args:
            task_id: The Celery task ID

        Returns:
            Result data dictionary, list of dictionaries, or None if not found
        """
        key = cls._make_key(task_id, "result")
        cached_data = cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    @classmethod
    def set_task_progress(cls, task_id: str, current: int, total: int, message: str, timeout: int = 86400) -> None:
        """
        Store task progress in Redis.

        Args:
            task_id: The Celery task ID
            current: Current progress count
            total: Total items to process
            message: Progress message
            timeout: Cache timeout in seconds (default: 24 hours)
        """
        progress_data = {
            "current": current,
            "total": total,
            "percentage": round((current / total * 100) if total > 0 else 0, 2),
            "message": message,
        }
        key = cls._make_key(task_id, "progress")
        cache.set(key, json.dumps(progress_data), timeout)

    @classmethod
    def get_task_progress(cls, task_id: str) -> dict[str, Any] | None:
        """
        Retrieve task progress from Redis.

        Args:
            task_id: The Celery task ID

        Returns:
            Progress data dictionary or None if not found
        """
        key = cls._make_key(task_id, "progress")
        cached_data = cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
