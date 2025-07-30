"""
Database query optimization utilities for django-bulk-drf.
"""
import logging
from typing import List, Dict, Any, Optional
from django.db import connection
from django.db.models import Model, QuerySet
from django.conf import settings

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Utility class for optimizing database queries in bulk operations."""
    
    @staticmethod
    def analyze_query_performance(queryset: QuerySet, operation_name: str = "bulk_operation") -> Dict[str, Any]:
        """
        Analyze query performance and suggest optimizations.
        
        Args:
            queryset: The queryset to analyze
            operation_name: Name of the operation for logging
            
        Returns:
            Dictionary with performance analysis and suggestions
        """
        # Get the SQL query
        sql_query = str(queryset.query)
        
        # Count queries (requires DEBUG=True)
        if settings.DEBUG:
            initial_queries = len(connection.queries)
            list(queryset)  # Execute query
            final_queries = len(connection.queries)
            query_count = final_queries - initial_queries
        else:
            query_count = "Unknown (DEBUG=False)"
        
        # Analyze query complexity
        analysis = {
            "operation": operation_name,
            "sql_query": sql_query,
            "query_count": query_count,
            "suggestions": []
        }
        
        # Check for common optimization opportunities
        if "SELECT" in sql_query.upper():
            if "JOIN" not in sql_query.upper() and "related" in sql_query.lower():
                analysis["suggestions"].append(
                    "Consider using select_related() for foreign key relationships"
                )
            
            if "WHERE id IN" in sql_query.upper():
                analysis["suggestions"].append(
                    "ID-based queries are optimal - ensure 'id' field is indexed"
                )
        
        return analysis
    
    @staticmethod
    def suggest_indexes(model_class: Model, common_filters: List[str] = None) -> List[str]:
        """
        Suggest database indexes based on model fields and common filters.
        
        Args:
            model_class: The Django model class
            common_filters: List of commonly used filter fields
            
        Returns:
            List of suggested index definitions
        """
        suggestions = []
        
        # Always suggest primary key index (usually auto-created)
        suggestions.append("PRIMARY KEY (id) - usually auto-created")
        
        # Suggest indexes for common filter fields
        if common_filters:
            for field in common_filters:
                if hasattr(model_class, field):
                    suggestions.append(f"INDEX idx_{model_class._meta.db_table}_{field} ({field})")
        
        # Suggest indexes for foreign keys
        for field in model_class._meta.fields:
            if hasattr(field, 'related_model') and field.related_model:
                suggestions.append(f"INDEX idx_{model_class._meta.db_table}_{field.name} ({field.name})")
        
        # Suggest composite indexes for common filter combinations
        if common_filters and len(common_filters) > 1:
            # Common pattern: status + date range
            if 'status' in common_filters and any('date' in f for f in common_filters):
                date_field = next(f for f in common_filters if 'date' in f)
                suggestions.append(f"INDEX idx_{model_class._meta.db_table}_status_date (status, {date_field})")
        
        return suggestions
    
    @staticmethod
    def optimize_bulk_operations(model_class: Model, operation_type: str) -> Dict[str, Any]:
        """
        Provide optimization recommendations for bulk operations.
        
        Args:
            model_class: The Django model class
            operation_type: Type of bulk operation (create, update, delete, get)
            
        Returns:
            Dictionary with optimization recommendations
        """
        recommendations = {
            "model": model_class.__name__,
            "operation": operation_type,
            "recommendations": []
        }
        
        if operation_type == "create":
            recommendations["recommendations"].extend([
                "Use bulk_create() with batch_size=1000 for optimal performance",
                "Disable auto_now/auto_now_add fields during bulk operations",
                "Consider using ignore_conflicts=True for duplicate handling"
            ])
        
        elif operation_type == "update":
            recommendations["recommendations"].extend([
                "Use bulk_update() instead of individual save() calls",
                "Batch updates in groups of 1000 records",
                "Only update changed fields to reduce database load"
            ])
        
        elif operation_type == "delete":
            recommendations["recommendations"].extend([
                "Use bulk_delete() for large deletions",
                "Consider soft deletes for audit trails",
                "Use CASCADE carefully to avoid unintended deletions"
            ])
        
        elif operation_type == "get":
            recommendations["recommendations"].extend([
                "Use select_related() for foreign key relationships",
                "Use prefetch_related() for reverse foreign keys and many-to-many",
                "Use iterator() for large result sets to reduce memory usage",
                "Consider pagination for very large datasets"
            ])
        
        return recommendations


class DatabaseIndexManager:
    """Manages database indexes for optimal bulk operation performance."""
    
    @staticmethod
    def create_index_if_not_exists(model_class: Model, field_name: str, index_type: str = "btree") -> bool:
        """
        Create a database index if it doesn't exist.
        
        Args:
            model_class: The Django model class
            field_name: Name of the field to index
            index_type: Type of index (btree, hash, etc.)
            
        Returns:
            True if index was created, False if it already exists
        """
        table_name = model_class._meta.db_table
        index_name = f"idx_{table_name}_{field_name}"
        
        with connection.cursor() as cursor:
            # Check if index exists
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = %s AND indexname = %s
            """, [table_name, index_name])
            
            if cursor.fetchone():
                logger.info(f"Index {index_name} already exists")
                return False
            
            # Create index
            cursor.execute(f"""
                CREATE INDEX {index_name} ON {table_name} 
                USING {index_type} ({field_name})
            """)
            
            logger.info(f"Created index {index_name} on {table_name}.{field_name}")
            return True
    
    @staticmethod
    def create_composite_index_if_not_exists(
        model_class: Model, 
        field_names: List[str], 
        index_name: Optional[str] = None
    ) -> bool:
        """
        Create a composite index if it doesn't exist.
        
        Args:
            model_class: The Django model class
            field_names: List of field names for composite index
            index_name: Custom index name (optional)
            
        Returns:
            True if index was created, False if it already exists
        """
        table_name = model_class._meta.db_table
        
        if not index_name:
            index_name = f"idx_{table_name}_{'_'.join(field_names)}"
        
        fields_str = ", ".join(field_names)
        
        with connection.cursor() as cursor:
            # Check if index exists
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = %s AND indexname = %s
            """, [table_name, index_name])
            
            if cursor.fetchone():
                logger.info(f"Composite index {index_name} already exists")
                return False
            
            # Create composite index
            cursor.execute(f"""
                CREATE INDEX {index_name} ON {table_name} ({fields_str})
            """)
            
            logger.info(f"Created composite index {index_name} on {table_name} ({fields_str})")
            return True


class QueryMonitor:
    """Monitors query performance and provides insights."""
    
    def __init__(self):
        self.query_log = []
    
    def start_monitoring(self):
        """Start monitoring database queries."""
        if settings.DEBUG:
            connection.queries_log = True
            self.query_log = []
    
    def stop_monitoring(self) -> Dict[str, Any]:
        """
        Stop monitoring and return performance analysis.
        
        Returns:
            Dictionary with query performance analysis
        """
        if not settings.DEBUG:
            return {"error": "Query monitoring requires DEBUG=True"}
        
        queries = connection.queries
        total_time = sum(float(q['time']) for q in queries)
        
        analysis = {
            "total_queries": len(queries),
            "total_time": total_time,
            "average_time": total_time / len(queries) if queries else 0,
            "slow_queries": [q for q in queries if float(q['time']) > 0.1],  # > 100ms
            "queries": queries
        }
        
        return analysis 