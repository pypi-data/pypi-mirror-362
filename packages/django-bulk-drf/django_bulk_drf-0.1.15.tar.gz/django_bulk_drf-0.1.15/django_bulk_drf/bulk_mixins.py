"""
Bulk operation mixins for DRF ViewSets.
"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Optional OpenAPI schema support
try:
    from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
    from drf_spectacular.types import OpenApiTypes
    SPECTACULAR_AVAILABLE = True
except ImportError:
    SPECTACULAR_AVAILABLE = False
    # Create dummy decorator if drf-spectacular is not available
    def extend_schema(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    # Create dummy classes for OpenAPI types
    class OpenApiParameter:
        QUERY = "query"
        def __init__(self, name, type, location, description, examples=None):
            pass
    
    class OpenApiExample:
        def __init__(self, name, value, description=None):
            pass
    
    class OpenApiTypes:
        STR = "string"

from django_bulk_drf.bulk_processing import (
    bulk_create_task,
    bulk_delete_task,
    bulk_get_task,
    bulk_replace_task,
    bulk_update_task,
    bulk_upsert_task,
)


class BulkOperationsMixin:
    """Mixin providing bulk operations through a single endpoint with different HTTP methods."""

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get("data", None)
        if data is not None and isinstance(data, list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=["get"], url_path="bulk")
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ids",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Comma-separated list of IDs to retrieve (e.g., '1,2,3,4,5')",
                examples=[
                    OpenApiExample(
                        "Small set",
                        value="1,2,3,4,5",
                        description="Returns data directly for ≤100 IDs"
                    ),
                    OpenApiExample(
                        "Large set", 
                        value="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150",
                        description="Returns task ID for async processing for >100 IDs"
                    )
                ]
            )
        ],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "filters": {
                        "type": "object",
                        "description": "Complex query filters using Django ORM lookups",
                        "examples": [
                            OpenApiExample(
                                "Simple filters",
                                value={
                                    "filters": {
                                        "name": {"icontains": "tech"},
                                        "status": "active",
                                        "created_at": {"gte": "2024-01-01"}
                                    }
                                }
                            ),
                            OpenApiExample(
                                "Complex filters",
                                value={
                                    "filters": {
                                        "amount": {"gte": 100, "lte": 1000},
                                        "category": {"in": [1, 2, 3]},
                                        "description": {"icontains": "payment"},
                                        "is_active": True
                                    }
                                }
                            )
                        ]
                    }
                }
            }
        },
        responses={
            200: {
                "description": "Direct response for small result sets (≤100 records)",
                "examples": [
                    OpenApiExample(
                        "Success Response",
                        value={
                            "count": 3,
                            "results": [
                                {"id": 1, "name": "Business 1", "status": "active"},
                                {"id": 2, "name": "Business 2", "status": "active"},
                                {"id": 3, "name": "Business 3", "status": "inactive"}
                            ],
                            "is_async": False
                        }
                    )
                ]
            },
            202: {
                "description": "Async response for large result sets (>100 records)",
                "examples": [
                    OpenApiExample(
                        "Async Response",
                        value={
                            "message": "Bulk get task started for 250 IDs",
                            "task_id": "abc123-def456-ghi789",
                            "total_items": 250,
                            "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/",
                            "is_async": True
                        }
                    )
                ]
            },
            400: {
                "description": "Bad request - invalid parameters",
                "examples": [
                    OpenApiExample(
                        "Invalid ID Format",
                        value={"error": "Invalid ID format. Use comma-separated integers."}
                    ),
                    OpenApiExample(
                        "Missing Parameters",
                        value={"error": "Provide either 'ids' query parameter or query filters in request body"}
                    ),
                    OpenApiExample(
                        "Invalid Query Structure",
                        value={"error": "Query data must be an object with filter parameters"}
                    )
                ]
            }
        },
        description="Retrieve multiple instances by IDs or query parameters. Supports ID-based retrieval via ?ids=1,2,3 or complex filters in request body. Returns serialized data directly for small results (≤100), or task ID for large results (>100).",
        summary="Bulk retrieve instances"
    )
    def bulk_get(self, request):
        """
        Retrieve multiple instances by IDs or query parameters.

        Supports ID-based retrieval via ?ids=1,2,3 or complex filters in request body.
        Returns serialized data directly for small results, or task ID for large results.
        """
        return self._bulk_get(request)

    @action(detail=False, methods=["post"], url_path="bulk")
    @extend_schema(
        request={
            "application/json": {
                "type": "array",
                "description": "Array of objects to create",
                "examples": [
                    OpenApiExample(
                        "JSON Create",
                        value=[
                            {"name": "Business 1", "status": "active", "category": 1},
                            {"name": "Business 2", "status": "active", "category": 2}
                        ]
                    )
                ]
            },
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "CSV file with headers matching model fields"
                    }
                }
            }
        },
        responses={
            202: {
                "description": "Bulk create task started",
                "examples": [
                    OpenApiExample(
                        "Task Started",
                        value={
                            "message": "Bulk create task started for 2 items",
                            "task_id": "abc123-def456-ghi789",
                            "total_items": 2,
                            "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/"
                        }
                    )
                ]
            },
            400: {
                "description": "Bad request",
                "examples": [
                    OpenApiExample(
                        "Invalid Data",
                        value={"error": "Expected a list (array) of objects."}
                    ),
                    OpenApiExample(
                        "Empty List",
                        value={"error": "Empty list provided"}
                    )
                ]
            }
        },
        description="Create multiple instances asynchronously. Supports JSON array or CSV file upload.",
        summary="Bulk create instances"
    )
    def bulk_create(self, request):
        """
        Create multiple instances asynchronously.

        Supports:
        - JSON: Content-Type: application/json - Array of objects to create
        - CSV: Content-Type: multipart/form-data - CSV file upload with headers

        Returns a task ID for tracking the bulk operation.
        """
        return self._handle_bulk_request(request, "create")

    @action(detail=False, methods=["patch"], url_path="bulk")
    @extend_schema(
        request={
            "application/json": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Array of objects with 'id' and fields to update",
                        "examples": [
                            OpenApiExample(
                                "JSON Update",
                                value=[
                                    {"id": 1, "name": "Updated Business 1", "status": "inactive"},
                                    {"id": 2, "status": "active"}
                                ]
                            )
                        ]
                    },
                    {
                        "type": "object",
                        "description": "Upsert mode - object with data, unique_fields, and optional update_fields",
                        "properties": {
                            "data": {
                                "type": "array",
                                "description": "Array of objects to upsert"
                            },
                            "unique_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of field names that form the unique constraint"
                            },
                            "update_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of field names to update on conflict (optional, auto-inferred if not provided)"
                            }
                        },
                        "examples": [
                            OpenApiExample(
                                "JSON Upsert",
                                value={
                                    "data": [
                                        {"financial_account": 1, "year": 2024, "month": 1, "revenue": 1000},
                                        {"financial_account": 1, "year": 2024, "month": 2, "revenue": 1500}
                                    ],
                                    "unique_fields": ["financial_account", "year", "month"],
                                    "update_fields": ["revenue"]
                                }
                            )
                        ]
                    }
                ]
            },
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "CSV file with 'id' column and fields to update"
                    },
                    "unique_fields": {
                        "type": "string",
                        "description": "Comma-separated list of unique field names (for upsert mode)"
                    },
                    "update_fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to update on conflict (optional, for upsert mode)"
                    }
                }
            }
        },
        responses={
            202: {
                "description": "Bulk update task started",
                "examples": [
                    OpenApiExample(
                        "Task Started",
                        value={
                            "message": "Bulk update task started for 2 items",
                            "task_id": "abc123-def456-ghi789",
                            "total_items": 2,
                            "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/"
                        }
                    )
                ]
            },
            400: {
                "description": "Bad request",
                "examples": [
                    OpenApiExample(
                        "Missing ID",
                        value={"error": "Item at index 0 is missing 'id' field"}
                    ),
                    OpenApiExample(
                        "Invalid Data",
                        value={"error": "Expected a list (array) of objects."}
                    )
                ]
            }
        },
        description="Update multiple instances asynchronously (partial updates). Requires 'id' field for each object. Also supports upsert mode when providing 'data', 'unique_fields', and optional 'update_fields'.",
        summary="Bulk update instances"
    )
    def bulk_update(self, request):
        """
        Update multiple instances asynchronously (partial updates).

        Supports:
        - JSON: Content-Type: application/json - Array of objects with 'id' and fields to update
        - CSV: Content-Type: multipart/form-data - CSV file with 'id' column and fields to update

        Returns a task ID for tracking the bulk operation.
        """
        return self._handle_bulk_request(request, "update")

    @action(detail=False, methods=["put"], url_path="bulk")
    @extend_schema(
        request={
            "application/json": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Array of complete objects with 'id' and all required fields",
                        "examples": [
                            OpenApiExample(
                                "JSON Replace",
                                value=[
                                    {"id": 1, "name": "Replaced Business 1", "status": "active", "category": 1},
                                    {"id": 2, "name": "Replaced Business 2", "status": "inactive", "category": 2}
                                ]
                            )
                        ]
                    },
                    {
                        "type": "object",
                        "description": "Upsert mode - object with data, unique_fields, and optional update_fields",
                        "properties": {
                            "data": {
                                "type": "array",
                                "description": "Array of objects to upsert"
                            },
                            "unique_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of field names that form the unique constraint"
                            },
                            "update_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of field names to update on conflict (optional)"
                            }
                        },
                        "examples": [
                            OpenApiExample(
                                "JSON Upsert",
                                value={
                                    "data": [
                                        {"financial_account": 1, "year": 2024, "month": 1, "revenue": 1000},
                                        {"financial_account": 1, "year": 2024, "month": 2, "revenue": 1500}
                                    ],
                                    "unique_fields": ["financial_account", "year", "month"],
                                    "update_fields": ["revenue"]
                                }
                            )
                        ]
                    }
                ]
            },
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "CSV file with 'id' column and all required fields"
                    },
                    "unique_fields": {
                        "type": "string",
                        "description": "Comma-separated list of unique field names (for upsert mode)"
                    },
                    "update_fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to update on conflict (optional, for upsert mode)"
                    }
                }
            }
        },
        responses={
            202: {
                "description": "Bulk replace task started",
                "examples": [
                    OpenApiExample(
                        "Task Started",
                        value={
                            "message": "Bulk replace task started for 2 items",
                            "task_id": "abc123-def456-ghi789",
                            "total_items": 2,
                            "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/"
                        }
                    )
                ]
            },
            400: {
                "description": "Bad request",
                "examples": [
                    OpenApiExample(
                        "Missing ID",
                        value={"error": "Item at index 0 is missing 'id' field"}
                    ),
                    OpenApiExample(
                        "Invalid Data",
                        value={"error": "Expected a list (array) of objects."}
                    )
                ]
            }
        },
        description="Replace multiple instances asynchronously (full updates). Requires 'id' field and all required fields for each object. Also supports upsert mode when providing 'data', 'unique_fields', and optional 'update_fields'.",
        summary="Bulk replace instances"
    )
    def bulk_replace(self, request):
        """
        Replace multiple instances asynchronously (full updates).

        Supports:
        - JSON: Content-Type: application/json - Array of complete objects with 'id' and all required fields
        - CSV: Content-Type: multipart/form-data - CSV file with 'id' column and all required fields

        Returns a task ID for tracking the bulk operation.
        """
        return self._handle_bulk_request(request, "replace")

    @action(detail=False, methods=["delete"], url_path="bulk")
    @extend_schema(
        request={
            "application/json": {
                "type": "array",
                "description": "Array of IDs to delete",
                "items": {"type": "integer"},
                "examples": [
                    OpenApiExample(
                        "JSON Delete",
                        value=[1, 2, 3, 4, 5]
                    )
                ]
            },
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "CSV file with 'id' column containing IDs to delete"
                    }
                }
            }
        },
        responses={
            202: {
                "description": "Bulk delete task started",
                "examples": [
                    OpenApiExample(
                        "Task Started",
                        value={
                            "message": "Bulk delete task started for 5 items",
                            "task_id": "abc123-def456-ghi789",
                            "total_items": 5,
                            "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/"
                        }
                    )
                ]
            },
            400: {
                "description": "Bad request",
                "examples": [
                    OpenApiExample(
                        "Invalid ID",
                        value={"error": "Item at index 0 is not a valid ID"}
                    ),
                    OpenApiExample(
                        "Invalid Data",
                        value={"error": "Expected a list (array) of IDs."}
                    )
                ]
            }
        },
        description="Delete multiple instances asynchronously. Provide array of IDs or CSV file with 'id' column.",
        summary="Bulk delete instances"
    )
    def bulk_delete(self, request):
        """
        Delete multiple instances asynchronously.

        Supports:
        - JSON: Content-Type: application/json - Array of IDs to delete
        - CSV: Content-Type: multipart/form-data - CSV file with 'id' column

        Returns a task ID for tracking the bulk operation.
        """
        return self._handle_bulk_request(request, "delete")



    def _handle_bulk_request(self, request, operation: str):
        """
        Route bulk requests based on Content-Type header.

        Args:
            request: The HTTP request
            operation: The operation type (create, update, replace, delete, upsert)

        Returns:
            Response based on content type (JSON or CSV file upload)
        """
        content_type = request.content_type.lower() if request.content_type else ""

        # Check if this is a file upload (multipart/form-data)
        if content_type.startswith("multipart/form-data"):
            return self._bulk_csv(request, operation)

        # Default to JSON processing for application/json or other content types
        elif content_type.startswith("application/json") or request.data:
            if operation == "create":
                return self._bulk_create(request)
            elif operation == "update":
                return self._bulk_update(request)
            elif operation == "replace":
                return self._bulk_replace(request)
            elif operation == "delete":
                return self._bulk_delete(request)

        else:
            return Response(
                {
                    "error": "Unsupported content type. Use 'application/json' for JSON data or 'multipart/form-data' for CSV file upload.",
                    "supported_formats": {
                        "JSON": "Content-Type: application/json",
                        "CSV": "Content-Type: multipart/form-data with 'file' parameter",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _bulk_create(self, request):
        """
        Create multiple instances asynchronously.

        Expects a JSON array of objects to create.
        Returns a task ID for tracking the bulk operation.
        """
        data_list = request.data
        if not isinstance(data_list, list):
            return Response(
                {"error": "Expected a list (array) of objects."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not data_list:
            return Response(
                {"error": "Empty list provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk create task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_create_task.delay(serializer_class_path, data_list, user_id)

        return Response(
            {
                "message": f"Bulk create task started for {len(data_list)} items",
                "task_id": task.id,
                "total_items": len(data_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _bulk_update(self, request):
        """
        Update multiple instances asynchronously.

        Supports:
        1. Standard update: array of objects with 'id' and update data
        2. Upsert: if ?unique_fields=... is present, treat payload as upsert data (list or single object)
        3. Upsert: if body has 'data' and 'unique_fields' keys (legacy)
        """
        # Salesforce-style: unique_fields in query params
        unique_fields_param = request.query_params.get("unique_fields")
        if unique_fields_param:
            unique_fields = [f.strip() for f in unique_fields_param.split(",") if f.strip()]
            # Accept both list and single-object payloads
            data = request.data
            if isinstance(data, dict):
                data_list = [data]
            elif isinstance(data, list):
                data_list = data
            else:
                return Response({"error": "Payload must be an object or array of objects for upsert."}, status=status.HTTP_400_BAD_REQUEST)
            # Auto-infer update_fields
            update_fields = self._infer_update_fields(data_list, unique_fields)
            return self._bulk_upsert_from_parts(data_list, unique_fields, update_fields, request)
        
        # Legacy upsert: body has 'data' and 'unique_fields'
        request_data = request.data
        if isinstance(request_data, dict) and "data" in request_data and "unique_fields" in request_data:
            return self._bulk_upsert(request)
        
        # Standard update mode
        updates_list = request_data
        if not isinstance(updates_list, list):
            return Response(
                {"error": "Expected a list (array) of objects."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not updates_list:
            return Response(
                {"error": "Empty list provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate that all items have an 'id' field
        for i, item in enumerate(updates_list):
            if not isinstance(item, dict) or "id" not in item:
                return Response(
                    {"error": f"Item at index {i} is missing 'id' field"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk update task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_update_task.delay(serializer_class_path, updates_list, user_id)

        return Response(
            {
                "message": f"Bulk update task started for {len(updates_list)} items",
                "task_id": task.id,
                "total_items": len(updates_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _bulk_replace(self, request):
        """
        Replace multiple instances asynchronously (full updates).

        Supports:
        1. Standard replace: array of complete objects with 'id' and all required fields
        2. Upsert: if ?unique_fields=... is present, treat payload as upsert data (list or single object)
        3. Upsert: if body has 'data' and 'unique_fields' keys (legacy)
        """
        # Salesforce-style: unique_fields in query params
        unique_fields_param = request.query_params.get("unique_fields")
        if unique_fields_param:
            unique_fields = [f.strip() for f in unique_fields_param.split(",") if f.strip()]
            # Accept both list and single-object payloads
            data = request.data
            if isinstance(data, dict):
                data_list = [data]
            elif isinstance(data, list):
                data_list = data
            else:
                return Response({"error": "Payload must be an object or array of objects for upsert."}, status=status.HTTP_400_BAD_REQUEST)
            # Auto-infer update_fields
            update_fields = self._infer_update_fields(data_list, unique_fields)
            return self._bulk_upsert_from_parts(data_list, unique_fields, update_fields, request)
        
        # Legacy upsert: body has 'data' and 'unique_fields'
        request_data = request.data
        if isinstance(request_data, dict) and "data" in request_data and "unique_fields" in request_data:
            return self._bulk_upsert(request)
        
        # Standard replace mode
        replacements_list = request_data
        if not isinstance(replacements_list, list):
            return Response(
                {"error": "Expected a list (array) of objects."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not replacements_list:
            return Response(
                {"error": "Empty list provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate that all items have an 'id' field
        for i, item in enumerate(replacements_list):
            if not isinstance(item, dict) or "id" not in item:
                return Response(
                    {"error": f"Item at index {i} is missing 'id' field"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk replace task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_replace_task.delay(
            serializer_class_path, replacements_list, user_id
        )

        return Response(
            {
                "message": f"Bulk replace task started for {len(replacements_list)} items",
                "task_id": task.id,
                "total_items": len(replacements_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _bulk_delete(self, request):
        """
        Delete multiple instances asynchronously.

        Expects a JSON array of IDs to delete.
        Returns a task ID for tracking the bulk operation.
        """
        ids_list = request.data
        if not isinstance(ids_list, list):
            return Response(
                {"error": "Expected a list (array) of IDs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not ids_list:
            return Response(
                {"error": "Empty list provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate that all items are integers (IDs)
        for i, item_id in enumerate(ids_list):
            if not isinstance(item_id, int):
                return Response(
                    {"error": f"Item at index {i} is not a valid ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Get the model class path
        model_class = self.get_queryset().model
        model_class_path = f"{model_class.__module__}.{model_class.__name__}"

        # Start the bulk delete task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_delete_task.delay(model_class_path, ids_list, user_id)

        return Response(
            {
                "message": f"Bulk delete task started for {len(ids_list)} items",
                "task_id": task.id,
                "total_items": len(ids_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _bulk_upsert(self, request):
        """
        Upsert multiple instances asynchronously.
        
        Similar to Django's bulk_create with update_conflicts=True, this method
        will create new records or update existing ones based on unique field constraints.
        
        Expects a JSON object with:
        - data: Array of objects to upsert
        - unique_fields: List of field names that form the unique constraint
        - update_fields: Optional list of field names to update on conflict (auto-inferred if not provided)
        
        Returns a task ID for tracking the bulk operation.
        """
        # Handle both JSON and form data formats
        if request.content_type and request.content_type.startswith("multipart/form-data"):
            # Handle CSV file upload
            return self._bulk_csv(request, "upsert")
        
        # Handle JSON data
        request_data = request.data
        
        # Validate request structure
        if not isinstance(request_data, dict):
            return Response(
                {"error": "Expected an object with 'data', 'unique_fields', and optional 'update_fields'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        data_list = request_data.get("data")
        unique_fields = request_data.get("unique_fields")
        update_fields = request_data.get("update_fields")
        
        # Validate required fields
        if not isinstance(data_list, list):
            return Response(
                {"error": "Expected 'data' to be a list (array) of objects."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not data_list:
            return Response(
                {"error": "Empty data list provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not unique_fields or not isinstance(unique_fields, list):
            return Response(
                {"error": "unique_fields parameter is required and must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Validate that all items are dictionaries
        for i, item in enumerate(data_list):
            if not isinstance(item, dict):
                return Response(
                    {"error": f"Item at index {i} is not a valid object"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        # Auto-infer update_fields if not provided
        if not update_fields:
            update_fields = self._infer_update_fields(data_list, unique_fields)
        
        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk upsert task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_upsert_task.delay(
            serializer_class_path, 
            data_list, 
            unique_fields, 
            update_fields, 
            user_id
        )

        return Response(
            {
                "message": f"Bulk upsert task started for {len(data_list)} items",
                "task_id": task.id,
                "total_items": len(data_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _bulk_upsert_from_parts(self, data_list, unique_fields, update_fields, request):
        """
        Helper for Salesforce-style upsert: directly call the upsert task with explicit params.
        """
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_upsert_task.delay(
            serializer_class_path,
            data_list,
            unique_fields,
            update_fields,
            user_id
        )
        return Response(
            {
                "message": f"Bulk upsert task started for {len(data_list)} items",
                "task_id": task.id,
                "total_items": len(data_list),
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _infer_update_fields(self, data_list: list[dict], unique_fields: list[str]) -> list[str]:
        """
        Automatically infer which fields should be updated based on the data payload.
        
        Args:
            data_list: List of data objects
            unique_fields: List of unique constraint fields
            
        Returns:
            List of field names that should be updated (all fields except unique_fields)
        """
        if not data_list:
            return []
        
        # Get all unique field names from the data
        all_fields = set()
        for item in data_list:
            if isinstance(item, dict):
                all_fields.update(item.keys())
        
        # Remove unique fields and return the rest as update fields
        update_fields = list(all_fields - set(unique_fields))
        
        # Sort for consistent ordering
        update_fields.sort()
        
        return update_fields

    def _bulk_get(self, request):
        """
        Retrieve multiple instances using bulk query.

        Supports two modes:
        1. Query parameters: ?ids=1,2,3,4,5 for simple ID-based retrieval
        2. POST body with complex filters for advanced queries

        Returns serialized data directly for small results, or task ID for large results.
        """
        # Mode 1: Simple ID-based retrieval via query params
        ids_param = request.query_params.get("ids")
        if ids_param:
            try:
                ids_list = [int(id_str.strip()) for id_str in ids_param.split(",")]

                # For small ID lists, return directly
                if len(ids_list) <= 100:  # Configurable threshold
                    queryset = self.get_queryset().filter(id__in=ids_list)
                    serializer = self.get_serializer(queryset, many=True)

                    return Response(
                        {
                            "count": len(serializer.data),
                            "results": serializer.data,
                            "is_async": False,
                        },
                        status=status.HTTP_200_OK,
                    )

                # For large ID lists, process asynchronously
                else:
                    model_class = self.get_queryset().model
                    model_class_path = (
                        f"{model_class.__module__}.{model_class.__name__}"
                    )
                    serializer_class = self.get_serializer_class()
                    serializer_class_path = (
                        f"{serializer_class.__module__}.{serializer_class.__name__}"
                    )

                    user_id = request.user.id if request.user.is_authenticated else None
                    task = bulk_get_task.delay(
                        model_class_path,
                        serializer_class_path,
                        {"ids": ids_list},
                        user_id,
                    )

                    return Response(
                        {
                            "message": f"Bulk get task started for {len(ids_list)} IDs",
                            "task_id": task.id,
                            "total_items": len(ids_list),
                            "status_url": f"/api/bulk-operations/{task.id}/status/",
                            "is_async": True,
                        },
                        status=status.HTTP_202_ACCEPTED,
                    )

            except ValueError:
                return Response(
                    {"error": "Invalid ID format. Use comma-separated integers."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Mode 2: Complex query via request body (treated as POST-style query)
        elif request.data:
            query_data = request.data

            # Validate query structure
            if not isinstance(query_data, dict):
                return Response(
                    {"error": "Query data must be an object with filter parameters"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Start async task for complex queries
            model_class = self.get_queryset().model
            model_class_path = f"{model_class.__module__}.{model_class.__name__}"
            serializer_class = self.get_serializer_class()
            serializer_class_path = (
                f"{serializer_class.__module__}.{serializer_class.__name__}"
            )

            user_id = request.user.id if request.user.is_authenticated else None
            task = bulk_get_task.delay(
                model_class_path, serializer_class_path, query_data, user_id
            )

            return Response(
                {
                    "message": "Bulk query task started",
                    "task_id": task.id,
                    "status_url": f"/api/bulk-operations/{task.id}/status/",
                    "is_async": True,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        else:
            return Response(
                {
                    "error": "Provide either 'ids' query parameter or query filters in request body"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _bulk_csv(self, request, operation: str):
        """
        Handle CSV file upload for bulk operations.

        Args:
            request: The HTTP request containing the CSV file
            operation: The type of operation (create, update, replace, delete)

        Returns:
            Response with task ID for tracking the bulk operation
        """
        import csv
        import io

        # Check if file was uploaded
        if "file" not in request.FILES:
            return Response(
                {"error": "No CSV file provided. Upload a file with key 'file'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        csv_file = request.FILES["file"]

        # Validate file type
        if not csv_file.name.lower().endswith(".csv"):
            return Response(
                {"error": "File must be a CSV file with .csv extension"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate file size (configurable limit - default 10MB)
        max_size = getattr(self, "csv_max_file_size", 10 * 1024 * 1024)  # 10MB
        if csv_file.size > max_size:
            return Response(
                {
                    "error": f"File too large. Maximum size is {max_size // (1024 * 1024)}MB"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Read and parse CSV
            csv_content = csv_file.read().decode("utf-8-sig")  # Handle BOM
            csv_reader = csv.DictReader(io.StringIO(csv_content))

            # Convert CSV rows to list of dictionaries
            data_list = []
            for row_num, row in enumerate(
                csv_reader, start=2
            ):  # Start at 2 (header is row 1)
                # Remove empty values and strip whitespace
                cleaned_row = {
                    k.strip(): v.strip() if v else None
                    for k, v in row.items()
                    if k.strip()
                }

                # Skip completely empty rows
                if not any(cleaned_row.values()):
                    continue

                # Validate required fields based on operation
                if operation in ["update", "replace", "delete"] and not cleaned_row.get(
                    "id"
                ):
                    return Response(
                        {
                            "error": f"Row {row_num}: 'id' field is required for {operation} operations"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                data_list.append(cleaned_row)

            if not data_list:
                return Response(
                    {"error": "CSV file is empty or contains no valid data rows"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Route to appropriate operation
            if operation == "create":
                return self._process_csv_create(request, data_list, csv_file.name)
            elif operation == "update":
                return self._process_csv_update(request, data_list, csv_file.name)
            elif operation == "replace":
                return self._process_csv_replace(request, data_list, csv_file.name)
            elif operation == "delete":
                return self._process_csv_delete(request, data_list, csv_file.name)
            else:
                return Response(
                    {"error": f"Unsupported operation: {operation}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except UnicodeDecodeError:
            return Response(
                {"error": "Invalid file encoding. Please save CSV as UTF-8"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except csv.Error as e:
            return Response(
                {"error": f"CSV parsing error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"File processing error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _process_csv_create(self, request, data_list, filename):
        """Process CSV data for create operations."""
        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk create task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_create_task.delay(serializer_class_path, data_list, user_id)

        return Response(
            {
                "message": f"Bulk create task started from CSV '{filename}' with {len(data_list)} rows",
                "task_id": task.id,
                "total_items": len(data_list),
                "source_file": filename,
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _process_csv_update(self, request, data_list, filename):
        """Process CSV data for update operations."""
        # Check if this is an upsert request (has unique_fields parameter)
        unique_fields_str = request.POST.get("unique_fields")
        if unique_fields_str:
            return self._process_csv_upsert(request, data_list, filename)
        
        # Standard update mode
        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk update task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_update_task.delay(serializer_class_path, data_list, user_id)

        return Response(
            {
                "message": f"Bulk update task started from CSV '{filename}' with {len(data_list)} rows",
                "task_id": task.id,
                "total_items": len(data_list),
                "source_file": filename,
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _process_csv_replace(self, request, data_list, filename):
        """Process CSV data for replace operations."""
        # Check if this is an upsert request (has unique_fields parameter)
        unique_fields_str = request.POST.get("unique_fields")
        if unique_fields_str:
            return self._process_csv_upsert(request, data_list, filename)
        
        # Standard replace mode
        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk replace task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_replace_task.delay(serializer_class_path, data_list, user_id)

        return Response(
            {
                "message": f"Bulk replace task started from CSV '{filename}' with {len(data_list)} rows",
                "task_id": task.id,
                "total_items": len(data_list),
                "source_file": filename,
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _process_csv_delete(self, request, data_list, filename):
        """Process CSV data for delete operations."""
        # Extract IDs from CSV data
        ids_list = []
        for row in data_list:
            try:
                id_value = int(row["id"])
                ids_list.append(id_value)
            except (ValueError, KeyError):
                return Response(
                    {"error": f"Invalid or missing 'id' value in CSV: {row}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Get the model class path
        model_class = self.get_queryset().model
        model_class_path = f"{model_class.__module__}.{model_class.__name__}"

        # Start the bulk delete task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_delete_task.delay(model_class_path, ids_list, user_id)

        return Response(
            {
                "message": f"Bulk delete task started from CSV '{filename}' with {len(ids_list)} IDs",
                "task_id": task.id,
                "total_items": len(ids_list),
                "source_file": filename,
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def _process_csv_upsert(self, request, data_list, filename):
        """Process CSV data for upsert operations."""
        # Get unique_fields and update_fields from form data
        unique_fields_str = request.POST.get("unique_fields")
        update_fields_str = request.POST.get("update_fields")
        
        if not unique_fields_str:
            return Response(
                {"error": "unique_fields parameter is required for CSV upsert operations"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Parse comma-separated fields
        unique_fields = [field.strip() for field in unique_fields_str.split(",") if field.strip()]
        update_fields = None
        if update_fields_str:
            update_fields = [field.strip() for field in update_fields_str.split(",") if field.strip()]
        
        # Validate that all required unique fields are present in CSV headers
        csv_headers = set(data_list[0].keys()) if data_list else set()
        missing_fields = [field for field in unique_fields if field not in csv_headers]
        if missing_fields:
            return Response(
                {"error": f"Missing required unique fields in CSV: {missing_fields}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Auto-infer update_fields if not provided
        if not update_fields:
            update_fields = self._infer_update_fields(data_list, unique_fields)
        
        # Get the serializer class path
        serializer_class = self.get_serializer_class()
        serializer_class_path = (
            f"{serializer_class.__module__}.{serializer_class.__name__}"
        )

        # Start the bulk upsert task
        user_id = request.user.id if request.user.is_authenticated else None
        task = bulk_upsert_task.delay(
            serializer_class_path, 
            data_list, 
            unique_fields, 
            update_fields, 
            user_id
        )

        return Response(
            {
                "message": f"Bulk upsert task started from CSV '{filename}' with {len(data_list)} rows",
                "task_id": task.id,
                "total_items": len(data_list),
                "source_file": filename,
                "unique_fields": unique_fields,
                "update_fields": update_fields,
                "status_url": f"/api/bulk-operations/{task.id}/status/",
            },
            status=status.HTTP_202_ACCEPTED,
        )


# Keep individual mixins for backward compatibility
class BulkCreateMixin:
    """Mixin to add bulk create functionality to ViewSets."""

    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create_action(self, request):
        """
        Create multiple instances asynchronously.

        Expects a JSON array of objects to create.
        Returns a task ID for tracking the bulk operation.
        """
        return BulkOperationsMixin._bulk_create(self, request)


class BulkUpdateMixin:
    """Mixin to add bulk update functionality to ViewSets."""

    @action(detail=False, methods=["patch"], url_path="bulk-update")
    def bulk_update_action(self, request):
        """
        Update multiple instances asynchronously.

        Expects a JSON array of objects with 'id' and update data.
        Returns a task ID for tracking the bulk operation.
        """
        return BulkOperationsMixin._bulk_update(self, request)


class BulkDeleteMixin:
    """Mixin to add bulk delete functionality to ViewSets."""

    @action(detail=False, methods=["delete"], url_path="bulk-delete")
    def bulk_delete_action(self, request):
        """
        Delete multiple instances asynchronously.

        Expects a JSON array of IDs to delete.
        Returns a task ID for tracking the bulk operation.
        """
        return BulkOperationsMixin._bulk_delete(self, request)


class BulkReplaceMixin:
    """Mixin to add bulk replace functionality to ViewSets."""

    @action(detail=False, methods=["put"], url_path="bulk-replace")
    def bulk_replace_action(self, request):
        """
        Replace multiple instances asynchronously (full updates).

        Expects a JSON array of complete objects with 'id' and all required fields.
        Returns a task ID for tracking the bulk operation.
        """
        return BulkOperationsMixin._bulk_replace(self, request)


class BulkGetMixin:
    """Mixin to add bulk get functionality to ViewSets."""

    @action(detail=False, methods=["get"], url_path="bulk-get")
    def bulk_get_action(self, request):
        """
        Retrieve multiple instances using bulk query.

        Supports ID-based retrieval via query params or complex filters via request body.
        Returns serialized data or task ID for tracking the bulk operation.
        """
        return BulkOperationsMixin._bulk_get(self, request)



