"""
Django Bulk DRF - Asynchronous bulk operations for Django REST Framework

Provides mixins for ViewSets to handle bulk create, update, and delete operations
asynchronously using Celery workers with Redis for progress tracking.
"""

__version__ = "0.1.62"
__author__ = "Konrad Beck"
__email__ = "konrad.beck@merchantcapital.co.za"

# Make common imports available at package level
from .bulk_mixins import (
    BulkCreateMixin,
    BulkDeleteMixin,
    BulkGetMixin,
    BulkOperationsMixin,
    BulkReplaceMixin,
    BulkUpdateMixin,
)
from .bulk_views import BulkOperationStatusView

__all__ = [
    "BulkCreateMixin",
    "BulkDeleteMixin",
    "BulkGetMixin",
    "BulkOperationsMixin",
    "BulkReplaceMixin", 
    "BulkUpdateMixin",
    "BulkOperationStatusView",
]