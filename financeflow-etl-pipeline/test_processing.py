"""
Test script for transaction processing service
"""

from app.services.transaction_processing_service import process_transaction_file
import os

if __name__ == "__main__":
    # Path to raw data file
    input_file = "/Users/udayshankar/Documents/JOB/FinanceFlow/data/raw/budgetwise_finance_dataset.csv"
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File not found - {input_file}")
        exit(1)
    
    # Process the transaction file
    print("Starting transaction processing...\n")
    summary = process_transaction_file(input_file)
    
    # Display results
    print("\nProcessing Complete!")
    print(f"Status: {summary.get('status', 'unknown')}")
    
    if summary.get('status') == 'success':
        print(f"\nResults:")
        print(f"  Total Records: {summary['total_records']}")
        print(f"  Valid Records: {summary['valid_records']}")
        print(f"  Invalid Records: {summary['invalid_records']}")
        print(f"  Duplicates: {summary['duplicate_records']}")
        print(f"  Success Rate: {summary['success_rate']}%")
