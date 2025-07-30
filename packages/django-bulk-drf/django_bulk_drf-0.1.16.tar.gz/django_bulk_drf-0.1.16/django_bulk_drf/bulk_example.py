"""
Example script demonstrating how to use the bulk operations endpoints.

This script shows how to:
1. Create multiple financial transactions using bulk create
2. Update multiple financial transactions using bulk update
3. Delete multiple financial transactions using bulk delete
4. Track progress using the status endpoint

Run this script from a Django shell or as a management command.
"""
import time
import csv

import requests


class BulkOperationsExample:
    """Example class demonstrating bulk operations usage."""

    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        # Add authentication if needed
        # self.session.headers.update({'Authorization': 'Token your-token-here'})

    def bulk_create_financial_transactions(self, transactions_data: list[dict]) -> str:
        """
        Create multiple financial transactions using bulk endpoint with POST method.

        Args:
            transactions_data: List of transaction data dictionaries

        Returns:
            Task ID for tracking the operation
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        response = self.session.post(url, json=transactions_data)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk create started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            print(f"🔗 Status URL: {result['status_url']}")
            return result["task_id"]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""

    def bulk_update_financial_transactions(self, updates_data: list[dict]) -> str:
        """
        Update multiple financial transactions using bulk endpoint with PATCH method.

        Args:
            updates_data: List of update data dictionaries (must include 'id')

        Returns:
            Task ID for tracking the operation
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        response = self.session.patch(url, json=updates_data)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk update started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            return result["task_id"]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""

    def bulk_replace_financial_transactions(self, replacements_data: list[dict]) -> str:
        """
        Replace multiple financial transactions using bulk endpoint with PUT method.

        Args:
            replacements_data: List of complete replacement data dictionaries (must include 'id')

        Returns:
            Task ID for tracking the operation
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        response = self.session.put(url, json=replacements_data)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk replace started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            return result["task_id"]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""

    def bulk_delete_financial_transactions(self, ids_list: list[int]) -> str:
        """
        Delete multiple financial transactions using bulk endpoint with DELETE method.

        Args:
            ids_list: List of transaction IDs to delete

        Returns:
            Task ID for tracking the operation
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        response = self.session.delete(url, json=ids_list)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk delete started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            return result["task_id"]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""

    def bulk_get_financial_transactions(self, ids_list: list[int] = None, query_filters: dict = None) -> dict:
        """
        Retrieve multiple financial transactions using bulk endpoint with GET method.

        Args:
            ids_list: List of transaction IDs to retrieve
            query_filters: Dictionary of filters for complex queries

        Returns:
            Response data (either direct results or task info)
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        
        if ids_list:
            # Simple ID-based retrieval via query params
            ids_str = ",".join(map(str, ids_list))
            response = self.session.get(f"{url}?ids={ids_str}")
        elif query_filters:
            # Complex query via request body
            response = self.session.get(url, json=query_filters)
        else:
            print("❌ Error: Must provide either ids_list or query_filters")
            return {}
        
        if response.status_code == 200:
            result = response.json()
            if result.get("is_async", False):
                print(f"✅ Bulk get task started: {result.get('message', '')}")
                print(f"📋 Task ID: {result['task_id']}")
                return result
            else:
                print(f"✅ Retrieved {result['count']} records directly")
                return result
        elif response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk get task started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            return result
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return {}

    def bulk_upsert_financial_transactions(self, data: list[dict], unique_fields: list[str], salesforce_style: bool = True) -> str:
        """
        Upsert multiple financial transactions using PATCH bulk endpoint.
        
        Similar to Django's bulk_create with update_conflicts=True, this will create
        new records or update existing ones based on unique field constraints.

        Args:
            data: List of transaction data dictionaries (or single dict for single upsert)
            unique_fields: List of field names that form the unique constraint
            salesforce_style: If True, use query params (default). If False, use legacy body structure.

        Returns:
            Task ID for tracking the operation
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        
        if salesforce_style:
            # Salesforce-style: unique_fields in query params, data as payload
            params = {"unique_fields": ",".join(unique_fields)}
            response = self.session.patch(url, json=data, params=params)
        else:
            # Legacy style: structured body with data, unique_fields, update_fields
            payload = {
                "data": data,
                "unique_fields": unique_fields,
            }
            response = self.session.patch(url, json=payload)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk upsert started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            print(f"🔗 Status URL: {result['status_url']}")
            print(f"🔑 Unique fields: {unique_fields}")
            style = "Salesforce-style" if salesforce_style else "Legacy-style"
            print(f"🎯 Style: {style}")
            return result["task_id"]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""

    def bulk_upsert_csv_financial_transactions(self, csv_file_path: str, unique_fields: list[str], update_fields: list[str] = None) -> dict:
        """
        Upsert multiple financial transactions from CSV file using PATCH bulk endpoint.
        
        Note: CSV upsert currently uses form data approach (unique_fields in form data).
        Query param style for CSV is not yet implemented.

        Args:
            csv_file_path: Path to the CSV file
            unique_fields: List of field names that form the unique constraint
            update_fields: Optional list of field names to update on conflict (auto-inferred if not provided)

        Returns:
            Response data with task information
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        
        with open(csv_file_path, 'rb') as csv_file:
            files = {'file': csv_file}
            data = {
                'unique_fields': ','.join(unique_fields),
            }
            if update_fields:
                data['update_fields'] = ','.join(update_fields)
            
            response = self.session.patch(url, files=files, data=data)
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Bulk upsert from CSV started: {result['message']}")
            print(f"📋 Task ID: {result['task_id']}")
            print(f"📁 Source file: {result['source_file']}")
            print(f"🔑 Unique fields: {result['unique_fields']}")
            if result.get('update_fields'):
                print(f"📝 Update fields: {result['update_fields']}")
            return result
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return {}

    def check_task_status(self, task_id: str) -> dict:
        """
        Check the status of a bulk operation task.

        Args:
            task_id: The task ID to check

        Returns:
            Task status information
        """
        url = f"{self.base_url}/bulk-operations/{task_id}/status/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error checking status: {response.status_code} - {response.text}")
            return {}

    def wait_for_completion(self, task_id: str, max_wait: int = 300) -> dict:
        """
        Wait for a task to complete, showing progress updates.

        Args:
            task_id: The task ID to wait for
            max_wait: Maximum time to wait in seconds

        Returns:
            Final task result
        """
        print(f"⏳ Waiting for task {task_id} to complete...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_data = self.check_task_status(task_id)
            
            if not status_data:
                time.sleep(2)
                continue
                
            state = status_data.get("state", "UNKNOWN")
            
            if state == "PENDING":
                print("📋 Task is pending...")
            elif state == "PROGRESS":
                progress = status_data.get("progress", {})
                if progress:
                    current = progress.get("current", 0)
                    total = progress.get("total", 1)
                    percentage = progress.get("percentage", 0)
                    message = progress.get("message", "")
                    print(f"🔄 Progress: {current}/{total} ({percentage}%) - {message}")
            elif state == "SUCCESS":
                print("✅ Task completed successfully!")
                return status_data
            elif state == "FAILURE":
                print("❌ Task failed!")
                print(f"Error: {status_data.get('error', 'Unknown error')}")
                return status_data
            
            time.sleep(2)  # Check every 2 seconds
        
        print(f"⏰ Timeout waiting for task {task_id}")
        return self.check_task_status(task_id)

    def bulk_create_csv_financial_transactions(self, csv_file_path: str) -> dict:
        """
        Create multiple financial transactions using CSV file upload.

        Args:
            csv_file_path: Path to the CSV file to upload

        Returns:
            Response data with task info
        """
        url = f"{self.base_url}/financial-transactions/bulk/"
        
        try:
            with open(csv_file_path, 'rb') as csv_file:
                files = {'file': csv_file}
                response = self.session.post(url, files=files)
            
            if response.status_code == 202:
                result = response.json()
                print(f"✅ CSV bulk create started: {result['message']}")
                print(f"📋 Task ID: {result['task_id']}")
                print(f"📁 Source file: {result['source_file']}")
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return {}
                
        except FileNotFoundError:
            print(f"❌ Error: CSV file not found: {csv_file_path}")
            return {}
        except Exception as e:
            print(f"❌ Error uploading CSV: {str(e)}")
            return {}

    def create_sample_csv(self, filename: str = "sample_transactions.csv"):
        """
        Create a sample CSV file for testing bulk operations.
        
        Args:
            filename: Name of the CSV file to create
        """
        sample_data = [
            {
                "amount": "100.50",
                "description": "Sample transaction 1",
                "datetime": "2025-01-01T10:00:00Z",
                "financial_account": 1,
                "classification_status": 1
            },
            {
                "amount": "-25.75",
                "description": "Sample transaction 2", 
                "datetime": "2025-01-01T11:00:00Z",
                "financial_account": 1,
                "classification_status": 1
            },
            {
                "amount": "500.00",
                "description": "Sample transaction 3",
                "datetime": "2025-01-01T12:00:00Z",
                "financial_account": 2,
                "classification_status": 2
            }
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = sample_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sample_data)
            
            print(f"✅ Created sample CSV file: {filename}")
            print(f"📝 Contains {len(sample_data)} sample transactions")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating CSV file: {str(e)}")
            return None

def run_example():
    """Run the bulk operations example."""
    example = BulkOperationsExample()
    
    print("🚀 Starting Bulk Operations Example")
    print("=" * 50)
    
    # Example 1: Bulk Create
    print("\n📝 Example 1: Bulk Create Financial Transactions")
    
    # Sample transaction data - adjust fields according to your model
    sample_transactions = [
        {
            "amount": "100.50",
            "description": "Sample transaction 1",
            "datetime": "2025-01-01T10:00:00Z",
            "financial_account": 1,  # Adjust to valid account ID
            "classification_status": 1,  # Adjust to valid status ID
        },
        {
            "amount": "-25.75",
            "description": "Sample transaction 2", 
            "datetime": "2025-01-01T11:00:00Z",
            "financial_account": 1,  # Adjust to valid account ID
            "classification_status": 1,  # Adjust to valid status ID
        },
        {
            "amount": "500.00",
            "description": "Sample transaction 3",
            "datetime": "2025-01-01T12:00:00Z",
            "financial_account": 1,  # Adjust to valid account ID
            "classification_status": 1,  # Adjust to valid status ID
        },
    ]
    
    task_id = example.bulk_create_financial_transactions(sample_transactions)
    
    if task_id:
        # Wait for completion and get results
        result = example.wait_for_completion(task_id)
        
        if result.get("state") == "SUCCESS":
            task_result = result.get("result", {})
            print(f"📊 Results:")
            print(f"   • Created: {task_result.get('success_count', 0)}")
            print(f"   • Errors: {task_result.get('error_count', 0)}")
            print(f"   • Created IDs: {task_result.get('created_ids', [])}")
            
            created_ids = task_result.get("created_ids", [])
            
            # Example 2: Bulk Update (if we have created IDs)
            if created_ids:
                print("\n✏️ Example 2: Bulk Update Financial Transactions")
                
                updates_data = [
                    {
                        "id": created_ids[0],
                        "description": "Updated transaction 1",
                        "amount": "150.00",
                    },
                    {
                        "id": created_ids[1] if len(created_ids) > 1 else created_ids[0],
                        "description": "Updated transaction 2",
                    },
                ]
                
                update_task_id = example.bulk_update_financial_transactions(updates_data)
                
                if update_task_id:
                    update_result = example.wait_for_completion(update_task_id)
                    if update_result.get("state") == "SUCCESS":
                        update_task_result = update_result.get("result", {})
                        print(f"📊 Update Results:")
                        print(f"   • Updated: {update_task_result.get('success_count', 0)}")
                        print(f"   • Errors: {update_task_result.get('error_count', 0)}")
                
                # Example 3: Bulk Delete
                print("\n🗑️ Example 3: Bulk Delete Financial Transactions")
                
                delete_task_id = example.bulk_delete_financial_transactions(created_ids[:2])  # Delete first 2
                
                if delete_task_id:
                    delete_result = example.wait_for_completion(delete_task_id)
                    if delete_result.get("state") == "SUCCESS":
                        delete_task_result = delete_result.get("result", {})
                        print(f"📊 Delete Results:")
                        print(f"   • Deleted: {delete_task_result.get('success_count', 0)}")
                        print(f"   • Errors: {delete_task_result.get('error_count', 0)}")
    
    # Example 4: Bulk Create from CSV
    print("\n📁 Example 4: Bulk Create Financial Transactions from CSV")
    
    # Create a sample CSV file
    csv_file = example.create_sample_csv()
    
    if csv_file:
        # Perform bulk create using the CSV file
        csv_task_id = example.bulk_create_csv_financial_transactions(csv_file)
        
        if csv_task_id:
            # Wait for completion and get results
            csv_result = example.wait_for_completion(csv_task_id)
            
            if csv_result.get("state") == "SUCCESS":
                csv_task_result = csv_result.get("result", {})
                print(f"📊 CSV Upload Results:")
                print(f"   • Created: {csv_task_result.get('success_count', 0)}")
                print(f"   • Errors: {csv_task_result.get('error_count', 0)}")
                print(f"   • Created IDs: {csv_task_result.get('created_ids', [])}")
    
    # Example 5: Bulk Upsert (Salesforce-style with query params)
    print("\n🔄 Example 5: Bulk Upsert Financial Transactions (Salesforce-style)")
    
    # Sample upsert data - this will create new records or update existing ones
    # based on the unique constraint of financial_account + datetime
    upsert_data = [
        {
            "amount": "100.50",
            "description": "Upsert transaction 1",
            "datetime": "2025-01-01T10:00:00Z",
            "financial_account": 1,
            "classification_status": 1,
        },
        {
            "amount": "200.75",  # This will update the existing record if it exists
            "description": "Upsert transaction 1 (updated)",
            "datetime": "2025-01-01T10:00:00Z",  # Same datetime as above
            "financial_account": 1,  # Same account as above
            "classification_status": 2,  # Different status
        },
        {
            "amount": "300.00",
            "description": "Upsert transaction 2",
            "datetime": "2025-01-01T11:00:00Z",
            "financial_account": 1,
            "classification_status": 1,
        },
    ]
    
    # Define unique fields that form the constraint
    unique_fields = ["financial_account", "datetime"]
    
    # Salesforce-style: unique_fields in query params, update_fields auto-inferred
    upsert_task_id = example.bulk_upsert_financial_transactions(
        data=upsert_data,
        unique_fields=unique_fields,
        salesforce_style=True  # Use query params approach
    )
    
    if upsert_task_id:
        # Wait for completion and get results
        upsert_result = example.wait_for_completion(upsert_task_id)
        
        if upsert_result.get("state") == "SUCCESS":
            upsert_task_result = upsert_result.get("result", {})
            print(f"📊 Salesforce-style Upsert Results:")
            print(f"   • Created: {len(upsert_task_result.get('created_ids', []))}")
            print(f"   • Updated: {len(upsert_task_result.get('updated_ids', []))}")
            print(f"   • Errors: {upsert_task_result.get('error_count', 0)}")
            print(f"   • Created IDs: {upsert_task_result.get('created_ids', [])}")
            print(f"   • Updated IDs: {upsert_task_result.get('updated_ids', [])}")
    
    # Example 5b: Single object upsert (Salesforce-style)
    print("\n🔄 Example 5b: Single Object Upsert (Salesforce-style)")
    
    single_upsert_data = {
        "amount": "999.99",
        "description": "Single upsert transaction",
        "datetime": "2025-01-01T14:00:00Z",
        "financial_account": 1,
        "classification_status": 1,
    }
    
    single_upsert_task_id = example.bulk_upsert_financial_transactions(
        data=single_upsert_data,  # Single object, not array
        unique_fields=unique_fields,
        salesforce_style=True
    )
    
    if single_upsert_task_id:
        single_upsert_result = example.wait_for_completion(single_upsert_task_id)
        if single_upsert_result.get("state") == "SUCCESS":
            single_upsert_task_result = single_upsert_result.get("result", {})
            print(f"📊 Single Upsert Results:")
            print(f"   • Created: {len(single_upsert_task_result.get('created_ids', []))}")
            print(f"   • Updated: {len(single_upsert_task_result.get('updated_ids', []))}")
            print(f"   • Errors: {single_upsert_task_result.get('error_count', 0)}")
    
    # Example 5c: Legacy-style upsert (for backward compatibility)
    print("\n🔄 Example 5c: Legacy-style Upsert (backward compatibility)")
    
    legacy_upsert_task_id = example.bulk_upsert_financial_transactions(
        data=upsert_data,
        unique_fields=unique_fields,
        salesforce_style=False  # Use legacy body structure
    )
    
    if legacy_upsert_task_id:
        legacy_upsert_result = example.wait_for_completion(legacy_upsert_task_id)
        if legacy_upsert_result.get("state") == "SUCCESS":
            legacy_upsert_task_result = legacy_upsert_result.get("result", {})
            print(f"📊 Legacy-style Upsert Results:")
            print(f"   • Created: {len(legacy_upsert_task_result.get('created_ids', []))}")
            print(f"   • Updated: {len(legacy_upsert_task_result.get('updated_ids', []))}")
            print(f"   • Errors: {legacy_upsert_task_result.get('error_count', 0)}")
    
    # Example 6: Bulk Upsert from CSV
    print("\n📁 Example 6: Bulk Upsert Financial Transactions from CSV")
    
    # Create a sample CSV file for upsert
    upsert_csv_filename = "sample_upsert_transactions.csv"
    upsert_csv_data = [
        {
            "amount": "150.00",
            "description": "CSV Upsert 1",
            "datetime": "2025-01-01T12:00:00Z",
            "financial_account": "2",
            "classification_status": "1"
        },
        {
            "amount": "250.00",  # This will update if the record exists
            "description": "CSV Upsert 1 (updated)",
            "datetime": "2025-01-01T12:00:00Z",  # Same datetime
            "financial_account": "2",  # Same account
            "classification_status": "2"
        },
        {
            "amount": "350.00",
            "description": "CSV Upsert 2",
            "datetime": "2025-01-01T13:00:00Z",
            "financial_account": "2",
            "classification_status": "1"
        }
    ]
    
    try:
        with open(upsert_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = upsert_csv_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(upsert_csv_data)
        
        print(f"✅ Created upsert CSV file: {upsert_csv_filename}")
        
        # Perform bulk upsert using the CSV file
        csv_upsert_result = example.bulk_upsert_csv_financial_transactions(
            csv_file_path=upsert_csv_filename,
            unique_fields=["financial_account", "datetime"],
            update_fields=["amount", "description", "classification_status"]
        )
        
        if csv_upsert_result:
            # Wait for completion and get results
            csv_upsert_final_result = example.wait_for_completion(csv_upsert_result['task_id'])
            
            if csv_upsert_final_result.get("state") == "SUCCESS":
                csv_upsert_task_result = csv_upsert_final_result.get("result", {})
                print(f"📊 CSV Upsert Results:")
                print(f"   • Created: {len(csv_upsert_task_result.get('created_ids', []))}")
                print(f"   • Updated: {len(csv_upsert_task_result.get('updated_ids', []))}")
                print(f"   • Errors: {csv_upsert_task_result.get('error_count', 0)}")
                print(f"   • Created IDs: {csv_upsert_task_result.get('created_ids', [])}")
                print(f"   • Updated IDs: {csv_upsert_task_result.get('updated_ids', [])}")
                
    except Exception as e:
        print(f"❌ Error with CSV upsert example: {str(e)}")
    
    print("\n🎉 Bulk Operations Example Completed!")


if __name__ == "__main__":
    # This can be run as a Django management command
    # or from a Django shell
    run_example()
