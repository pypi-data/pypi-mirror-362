"""
Database optimization utilities for django-bulk-drf.
"""
import logging
from typing import List, Dict, Any, Optional, Generator
from django.db import connection, transaction
from django.db.models import Model, QuerySet
from django.conf import settings
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseOptimizer:
    """Database optimization utilities for bulk operations."""
    
    @staticmethod
    @contextmanager
    def optimized_connection():
        """
        Context manager for optimized database connections.
        
        Optimizes connection settings for bulk operations.
        """
        # Store original settings
        original_autocommit = connection.autocommit
        original_isolation_level = connection.isolation_level
        
        try:
            # Optimize for bulk operations
            connection.autocommit = False
            connection.isolation_level = 'READ_COMMITTED'
            
            yield connection
            
        finally:
            # Restore original settings
            connection.autocommit = original_autocommit
            connection.isolation_level = original_isolation_level
    
    @staticmethod
    def batch_queryset(queryset: QuerySet, batch_size: int = 1000) -> Generator[QuerySet, None, None]:
        """
        Split a queryset into batches for memory-efficient processing.
        
        Args:
            queryset: The queryset to batch
            batch_size: Size of each batch
            
        Yields:
            Batched querysets
        """
        offset = 0
        
        while True:
            batch = queryset[offset:offset + batch_size]
            
            # Check if batch has any results
            if not batch.exists():
                break
                
            yield batch
            offset += batch_size
    
    @staticmethod
    def optimize_bulk_create(model_class: Model, instances: List[Model], **kwargs) -> List[Model]:
        """
        Optimized bulk_create with automatic batch sizing and conflict handling.
        
        Args:
            model_class: The model class
            instances: List of model instances to create
            **kwargs: Additional arguments for bulk_create
            
        Returns:
            List of created instances
        """
        batch_size = kwargs.get('batch_size', 1000)
        ignore_conflicts = kwargs.get('ignore_conflicts', False)
        
        created_instances = []
        
        # Process in batches
        for i in range(0, len(instances), batch_size):
            batch = instances[i:i + batch_size]
            
            with transaction.atomic():
                batch_created = model_class.objects.bulk_create(
                    batch,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts,
                    **{k: v for k, v in kwargs.items() if k not in ['batch_size', 'ignore_conflicts']}
                )
                created_instances.extend(batch_created)
        
        return created_instances
    
    @staticmethod
    def optimize_bulk_update(model_class: Model, instances: List[Model], fields: List[str], **kwargs) -> int:
        """
        Optimized bulk_update with automatic batch sizing.
        
        Args:
            model_class: The model class
            instances: List of model instances to update
            fields: List of fields to update
            **kwargs: Additional arguments for bulk_update
            
        Returns:
            Number of updated instances
        """
        batch_size = kwargs.get('batch_size', 1000)
        total_updated = 0
        
        # Process in batches
        for i in range(0, len(instances), batch_size):
            batch = instances[i:i + batch_size]
            
            with transaction.atomic():
                updated_count = model_class.objects.bulk_update(
                    batch,
                    fields,
                    batch_size=batch_size,
                    **{k: v for k, v in kwargs.items() if k != 'batch_size'}
                )
                total_updated += updated_count
        
        return total_updated


class QueryBatcher:
    """Batches database operations for optimal performance."""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
        self.current_batch = []
        self.total_processed = 0
    
    def add(self, item: Any):
        """Add an item to the current batch."""
        self.current_batch.append(item)
        
        if len(self.current_batch) >= self.batch_size:
            self.flush()
    
    def flush(self):
        """Process the current batch."""
        if self.current_batch:
            # Process batch (implemented by subclasses)
            self._process_batch(self.current_batch)
            self.total_processed += len(self.current_batch)
            self.current_batch = []
    
    def _process_batch(self, batch: List[Any]):
        """Process a batch of items. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement _process_batch")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()


class BulkCreateBatcher(QueryBatcher):
    """Batches bulk create operations."""
    
    def __init__(self, model_class: Model, batch_size: int = 1000, **kwargs):
        super().__init__(batch_size)
        self.model_class = model_class
        self.kwargs = kwargs
        self.created_instances = []
    
    def _process_batch(self, batch: List[Model]):
        """Process a batch of model instances for bulk create."""
        with transaction.atomic():
            created = self.model_class.objects.bulk_create(
                batch,
                batch_size=self.batch_size,
                **self.kwargs
            )
            self.created_instances.extend(created)


class BulkUpdateBatcher(QueryBatcher):
    """Batches bulk update operations."""
    
    def __init__(self, model_class: Model, fields: List[str], batch_size: int = 1000, **kwargs):
        super().__init__(batch_size)
        self.model_class = model_class
        self.fields = fields
        self.kwargs = kwargs
        self.total_updated = 0
    
    def _process_batch(self, batch: List[Model]):
        """Process a batch of model instances for bulk update."""
        with transaction.atomic():
            updated_count = self.model_class.objects.bulk_update(
                batch,
                self.fields,
                batch_size=self.batch_size,
                **self.kwargs
            )
            self.total_updated += updated_count


class DatabaseMetrics:
    """Collects and reports database performance metrics."""
    
    def __init__(self):
        self.metrics = {
            'queries_executed': 0,
            'total_time': 0.0,
            'slow_queries': [],
            'batch_operations': 0,
            'bulk_operations': 0
        }
    
    def record_query(self, sql: str, time_taken: float):
        """Record a database query."""
        self.metrics['queries_executed'] += 1
        self.metrics['total_time'] += time_taken
        
        if time_taken > 0.1:  # 100ms threshold
            self.metrics['slow_queries'].append({
                'sql': sql,
                'time': time_taken
            })
    
    def record_batch_operation(self, operation_type: str, count: int):
        """Record a batch operation."""
        self.metrics['batch_operations'] += 1
        self.metrics['bulk_operations'] += count
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics."""
        return {
            **self.metrics,
            'average_query_time': (
                self.metrics['total_time'] / self.metrics['queries_executed']
                if self.metrics['queries_executed'] > 0 else 0
            ),
            'slow_query_count': len(self.metrics['slow_queries'])
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {
            'queries_executed': 0,
            'total_time': 0.0,
            'slow_queries': [],
            'batch_operations': 0,
            'bulk_operations': 0
        } 