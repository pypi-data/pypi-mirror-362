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
    
    print("\n🎉 Bulk Operations Example Completed!")


if __name__ == "__main__":
    # This can be run as a Django management command
    # or from a Django shell
    run_example()
