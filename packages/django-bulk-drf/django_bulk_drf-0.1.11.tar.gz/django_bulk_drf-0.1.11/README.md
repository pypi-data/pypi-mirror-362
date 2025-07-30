# Django Bulk DRF

Asynchronous bulk operations for Django REST Framework using Celery workers and Redis for progress tracking.

## Installation

```bash
pip install django-bulk-drf
```

### Requirements

- Python 3.11+
- Django 4.0+
- Django REST Framework 3.14+
- Celery 5.2+
- Redis 4.3+
- django-redis 5.2+

## Quick Setup

1. Add to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... your other apps
    'rest_framework',
    'django_bulk_drf',
]
```

2. Configure Redis cache:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

3. Configure Celery:
```python
# settings.py
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
```

This implementation provides asynchronous bulk operations for your Django REST Framework API endpoints using Celery workers and Redis for progress tracking.

## Overview

The bulk operations system consists of:

1. **Bulk Processing Tasks** (`django_bulk_drf.bulk_processing`) - Celery tasks for handling bulk operations
2. **Bulk Mixins** (`django_bulk_drf.bulk_mixins`) - DRF ViewSet mixins to add bulk endpoints
3. **Redis Cache** (`django_bulk_drf.bulk_cache`) - Progress tracking and result caching
4. **Status Views** (`django_bulk_drf.bulk_views`) - API endpoints to check task status

## Features

- ✅ **Asynchronous Processing**: Long-running bulk operations don't block the API
- ✅ **Progress Tracking**: Real-time progress updates via Redis
- ✅ **Error Handling**: Detailed error reporting for failed items
- ✅ **Result Caching**: Final results cached in Redis for 24 hours
- ✅ **Validation**: Full DRF serializer validation for all items
- ✅ **Atomic Operations**: Database transactions ensure data consistency
- ✅ **Unified Endpoint**: Single `/bulk` endpoint supports both JSON and CSV via Content-Type detection
- ✅ **RESTful Design**: Uses HTTP methods (GET, POST, PATCH, PUT, DELETE) for different operations

## Content-Type Detection

The system automatically detects the input format based on the HTTP `Content-Type` header:

- **`Content-Type: application/json`** → JSON data processing
- **`Content-Type: multipart/form-data`** → CSV file upload processing

This means you can use the same `/bulk` endpoint for both JSON and CSV operations, making the API clean and RESTful.

## Available Operations

### JSON-based Operations

### 1. Bulk Retrieve
- **Endpoint**: `GET /api/{model}/bulk/?ids=1,2,3`
- **Method**: GET
- **Input**: Query parameters (`ids`) or request body (complex filters)
- **Output**: Serialized data (direct) or Task ID for large results

### 2. Bulk Create
- **Endpoint**: `POST /api/{model}/bulk/`
- **Method**: POST
- **Input**: Array of objects to create
- **Output**: Task ID and status URL

### 3. Bulk Update (Partial)
- **Endpoint**: `PATCH /api/{model}/bulk/`
- **Method**: PATCH
- **Input**: Array of objects with `id` and partial update data
- **Output**: Task ID and status URL

### 4. Bulk Replace (Full Update)
- **Endpoint**: `PUT /api/{model}/bulk/`
- **Method**: PUT
- **Input**: Array of complete objects with `id` and all required fields
- **Output**: Task ID and status URL

### 5. Bulk Delete
- **Endpoint**: `DELETE /api/{model}/bulk/`
- **Method**: DELETE
- **Input**: Array of IDs to delete
- **Output**: Task ID and status URL

### CSV-based Operations (Salesforce-style)

All CSV operations use the same `/bulk` endpoint with `Content-Type: multipart/form-data`:

### 6. CSV Bulk Create
- **Endpoint**: `POST /api/{model}/bulk/`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Input**: CSV file upload with headers matching model fields
- **Output**: Task ID and status URL

### 7. CSV Bulk Update (Partial)
- **Endpoint**: `PATCH /api/{model}/bulk/`
- **Method**: PATCH
- **Content-Type**: `multipart/form-data`
- **Input**: CSV file with `id` column and fields to update
- **Output**: Task ID and status URL

### 8. CSV Bulk Replace (Full Update)
- **Endpoint**: `PUT /api/{model}/bulk/`
- **Method**: PUT
- **Content-Type**: `multipart/form-data`
- **Input**: CSV file with `id` column and all required fields
- **Output**: Task ID and status URL

### 9. CSV Bulk Delete
- **Endpoint**: `DELETE /api/{model}/bulk/`
- **Method**: DELETE
- **Content-Type**: `multipart/form-data`
- **Input**: CSV file with `id` column containing IDs to delete
- **Output**: Task ID and status URL

### 10. Status Tracking
- **Endpoint**: `GET /api/bulk-operations/{task_id}/status/`
- **Output**: Task status, progress, and results

## HTTP Method Differences

- **GET**: Retrieve multiple records by IDs or complex queries
- **POST**: Creates new records (all fields required based on your model)
- **PATCH**: Partial updates - only include fields you want to change (requires `id`)
- **PUT**: Full replacement - all required fields must be provided (requires `id`) 
- **DELETE**: Removes records (provide array of IDs)

## Usage

### Adding Bulk Operations to a ViewSet

```python
from django_bulk_drf.bulk_mixins import BulkOperationsMixin

class FinancialTransactionViewSet(BulkOperationsMixin, viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer
```

### OpenAPI/Swagger Documentation

The bulk operations include proper OpenAPI schema definitions for Swagger documentation. To enable this:

1. **Install drf-spectacular** (optional dependency):
```bash
pip install drf-spectacular
```

2. **Add to INSTALLED_APPS**:
```python
INSTALLED_APPS = [
    # ... your other apps
    'drf_spectacular',
]
```

3. **Configure DRF settings**:
```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your API',
    'DESCRIPTION': 'Your API description',
    'VERSION': '1.0.0',
}
```

4. **Add URL patterns**:
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ... your other URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

The bulk endpoints will now show proper OpenAPI documentation with:
- ✅ **Array payloads** correctly specified for all bulk operations
- ✅ **Request/response examples** for each operation type
- ✅ **Proper schema references** for your model fields
- ✅ **CSV upload support** documented for file operations

**Note**: If `drf-spectacular` is not installed, the mixins will work normally but without enhanced OpenAPI documentation.

### Example API Calls

#### Bulk Retrieve (Simple ID-based)
```bash
# Small result set - returns data directly
curl "http://localhost:8000/api/financial-transactions/bulk/?ids=1,2,3,4,5"
```

#### Bulk Retrieve (Large ID-based - Async)
```bash
# Large result set - returns task ID
curl "http://localhost:8000/api/financial-transactions/bulk/?ids=1,2,3,4,5,6,7,8,...,150"
```

#### Bulk Retrieve (Complex Query)
```bash
# Complex filtering via request body
curl -X GET http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "filters": {
      "amount": {"gte": 100, "lte": 1000},
      "datetime": {"gte": "2025-01-01"},
      "financial_account": 1
    }
  }'
```

#### Bulk Create
```bash
curl -X POST http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '[
    {
      "amount": "100.50",
      "description": "Transaction 1",
      "datetime": "2025-01-01T10:00:00Z",
      "financial_account": 1,
      "classification_status": 1
    },
    {
      "amount": "-25.75", 
      "description": "Transaction 2",
      "datetime": "2025-01-01T11:00:00Z",
      "financial_account": 1,
      "classification_status": 1
    }
  ]'
```

**Response:**
```json
{
  "message": "Bulk create task started for 2 items",
  "task_id": "abc123-def456-ghi789",
  "total_items": 2,
  "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/"
}
```

#### Bulk Update (Partial)
```bash
curl -X PATCH http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '[
    {
      "id": 1,
      "amount": "150.00",
      "description": "Updated transaction 1"
    },
    {
      "id": 2,
      "description": "Updated transaction 2"
    }
  ]'
```

#### Bulk Replace (Full Update)
```bash
curl -X PUT http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '[
    {
      "id": 1,
      "amount": "200.00",
      "description": "Completely replaced transaction 1",
      "datetime": "2025-01-01T15:00:00Z",
      "financial_account": 1,
      "classification_status": 2
    },
    {
      "id": 2,
      "amount": "75.50",
      "description": "Completely replaced transaction 2",
      "datetime": "2025-01-01T16:00:00Z",
      "financial_account": 1,
      "classification_status": 1
    }
  ]'
```

#### Bulk Delete
```bash
curl -X DELETE http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '[1, 2, 3, 4, 5]'
```

#### Check Status
```bash
curl http://localhost:8000/api/bulk-operations/abc123-def456-ghi789/status/
```

**Response:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "state": "SUCCESS",
  "result": {
    "task_id": "abc123-def456-ghi789",
    "total_items": 2,
    "operation_type": "bulk_create",
    "success_count": 2,
    "error_count": 0,
    "errors": [],
    "created_ids": [10, 11],
    "updated_ids": [],
    "deleted_ids": []
  },
  "progress": {
    "current": 2,
    "total": 2,
    "percentage": 100.0,
    "message": "Creating instances in database..."
  },
  "status": "Task completed successfully"
}
```

### CSV Upload Examples

#### CSV Bulk Create
```bash
# Upload CSV file for bulk creation
curl -X POST http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Authorization: Bearer your-token" \\
  -F "file=@transactions.csv"
```

**Sample CSV (transactions.csv):**
```csv
amount,description,datetime,financial_account,classification_status
100.50,"Transaction 1","2025-01-01T10:00:00Z",1,1
-25.75,"Transaction 2","2025-01-01T11:00:00Z",1,1
500.00,"Transaction 3","2025-01-01T12:00:00Z",2,2
```

#### CSV Bulk Update
```bash
# Upload CSV file for bulk updates
curl -X PATCH http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Authorization: Bearer your-token" \\
  -F "file=@updates.csv"
```

**Sample CSV (updates.csv):**
```csv
id,amount,description
1,150.00,"Updated Transaction 1"
2,,"Updated Transaction 2"
3,75.50,
```

#### CSV Bulk Delete
```bash
# Upload CSV file for bulk deletion
curl -X DELETE http://localhost:8000/api/financial-transactions/bulk/ \\
  -H "Authorization: Bearer your-token" \\
  -F "file=@delete_ids.csv"
```

**Sample CSV (delete_ids.csv):**
```csv
id
1
2
3
4
5
```

### CSV Format Requirements

1. **File encoding**: UTF-8 (supports BOM)
2. **File extension**: Must be `.csv`
3. **Headers**: First row must contain field names
4. **File size limit**: 10MB (configurable via `csv_max_file_size` attribute)
5. **Required fields**:
   - **Create**: All required model fields
   - **Update/Replace**: `id` column + fields to update
   - **Delete**: `id` column only

### CSV Benefits

- ✅ **Easy to create**: Use Excel, Google Sheets, or any CSV editor
- ✅ **Memory efficient**: Streamed processing for large files
- ✅ **Human readable**: Easy to review and edit data
- ✅ **Widely supported**: Standard format across platforms
- ✅ **Compact**: Smaller than equivalent JSON for large datasets

## Bulk GET Response Formats

### Small Result Sets (< 100 records)
Returns data immediately:
```json
{
  "count": 5,
  "results": [
    {"id": 1, "amount": "100.50", "description": "Transaction 1"},
    {"id": 2, "amount": "75.00", "description": "Transaction 2"}
  ],
  "is_async": false
}
```

### Large Result Sets (≥ 100 records)
Returns task ID for async processing:
```json
{
  "message": "Bulk get task started for 250 IDs",
  "task_id": "abc123-def456-ghi789",
  "total_items": 250,
  "status_url": "/api/bulk-operations/abc123-def456-ghi789/status/",
  "is_async": true
}
```

### Complex Query Filters

You can use Django ORM-style filters in the request body:

```json
{
  "filters": {
    "amount": {"gte": 100, "lte": 1000},      // amount >= 100 AND amount <= 1000
    "datetime": {"gte": "2025-01-01"},         // datetime >= 2025-01-01
    "financial_account": 1,                    // financial_account = 1
    "description": {"icontains": "payment"}    // description contains "payment" (case-insensitive)
  }
}
```

Supported lookup types: `exact`, `gte`, `lte`, `gt`, `lt`, `in`, `icontains`, `startswith`, `endswith`, etc.

## Task States

- **PENDING**: Task is waiting to be executed
- **PROGRESS**: Task is currently running (includes progress data)
- **SUCCESS**: Task completed successfully
- **FAILURE**: Task failed with an error

## Progress Tracking

Progress is tracked in Redis and updated every 10 items processed. The progress object includes:

```json
{
  "current": 50,
  "total": 100,
  "percentage": 50.0,
  "message": "Validated 50/100 items"
}
```

## Error Handling

Individual item errors are captured and included in the result:

```json
{
  "errors": [
    {
      "index": 5,
      "error": "amount: This field is required.",
      "data": {"description": "Missing amount"}
    }
  ]
}
```

## Configuration

### Redis Settings
Make sure your Django settings include Redis configuration:

```python
# Redis cache for bulk operations
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Celery Settings
Your Celery configuration should include:

```python
# Celery settings for bulk operations
CELERY_TASK_TIME_LIMIT = 5 * 60  # 5 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 60  # 1 minute
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
```

## Starting Workers

To process bulk operations, start Celery workers:

```bash
# Start Celery worker
celery -A config.celery_app worker -l info

# Start Celery beat (for periodic tasks)
celery -A config.celery_app beat -l info

# Start Flower (monitoring - optional)
celery -A config.celery_app flower
```

## Performance Considerations

1. **Batch Size**: Large arrays are processed in chunks to avoid memory issues
2. **Database Connections**: Use connection pooling for high-volume operations
3. **Redis Memory**: Monitor Redis memory usage for large result sets
4. **Worker Scaling**: Scale Celery workers based on load

## Monitoring

- Use Flower for Celery task monitoring: `http://localhost:5555`
- Monitor Redis usage with `redis-cli info memory`
- Check Django logs for task execution details
- Use the status endpoint for real-time progress tracking

## Security Considerations

1. **Authentication**: Ensure bulk endpoints require proper authentication
2. **Rate Limiting**: Implement rate limiting for bulk operations
3. **Input Validation**: All input is validated through DRF serializers
4. **Permission Checks**: Add custom permission classes as needed

## Extending the System

### Custom Bulk Operations

You can create custom bulk operations by:

1. Creating new Celery tasks in `bulk_processing.py`
2. Adding new action methods to the mixins
3. Updating the status view if needed

### Custom Progress Tracking

Override the progress tracking by extending `BulkOperationCache`:

```python
from django_bulk_drf.bulk_cache import BulkOperationCache

class CustomBulkCache(BulkOperationCache):
    @classmethod
    def set_custom_metric(cls, task_id: str, metric_data: dict):
        # Custom metric tracking
        pass
```

This bulk operations system provides a robust, scalable solution for handling large data operations asynchronously while keeping your API responsive and providing real-time feedback to users.
