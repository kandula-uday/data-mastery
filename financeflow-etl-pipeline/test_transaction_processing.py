"""
Test Transaction Processing Service with actual CSV data
"""

import sys
sys.path.append('/Users/udayshankar/Documents/JOB/FinanceFlow')

from app.services.transaction_processing_service import process_transaction_file

# Path to the raw CSV file
input_file = '/Users/udayshankar/Documents/JOB/FinanceFlow/data/raw/budgetwise_finance_dataset.csv'

print("="*80)
print("TESTING TRANSACTION PROCESSING SERVICE")
print("="*80)
print()
print(f"Input file: {input_file}")
print()

# Process the transaction file
result = process_transaction_file(input_file)

print()
print("="*80)
print("FINAL RESULT")
print("="*80)
print(f"Status: {result['status']}")
print(f"Timestamp: {result['timestamp']}")
print(f"Total Records: {result['total_records']}")
print(f"Valid Records: {result['valid_records']}")
print(f"Invalid Records: {result['invalid_records']}")
print(f"Duplicate Records: {result['duplicate_records']}")
print(f"Success Rate: {result['success_rate']}%")
print()

# Show where files were saved
print("="*80)
print("OUTPUT FILES")
print("="*80)
print("✅ Valid records saved to: data/processed/processed_transactions_<timestamp>.csv")
print("❌ Invalid records saved to: data/invalid/invalid_transactions_<timestamp>.csv")
print()
