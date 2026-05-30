import pandas as pd
import os
from datetime import datetime

# Import validators
from app.validations.amount_validator import validate_amount
from app.validations.category_validator import validate_category
from app.validations.date_validator import validate_date
from app.validations.location_validator import validate_location
from app.validations.notes_validator import validate_notes
from app.validations.payment_mode_validator import validate_payment_mode

# Import cleaners
from app.utils.amount_cleaner import clean_amount
from app.utils.category_cleaner import clean_category
from app.utils.date_cleaner import clean_date
from app.utils.location_cleaner import clean_location
from app.utils.notes_cleaner import clean_notes
from app.utils.payment_mode_cleaner import clean_payment_mode


# Track processed transaction IDs to detect duplicates
processed_transaction_ids = set()


def process_transaction_file(input_file_path):
    """
    Main orchestration function.

    Responsibilities:
    - Load raw CSV data
    - Process each record
    - Separate valid and invalid records
    - Save processed output
    - Save invalid output
    - Return processing summary
    """
    print(f"Starting transaction processing for: {input_file_path}")
    
    # Load raw data
    raw_data = load_raw_data(input_file_path)
    
    if raw_data is None or raw_data.empty:
        print("No data to process")
        return {
            'status': 'error',
            'message': 'No data found in input file'
        }
    
    # Process each record
    processed_results = []
    for idx, row in raw_data.iterrows():
        result = process_single_record(row)
        result['original_index'] = idx
        processed_results.append(result)
    
    # Separate valid and invalid records
    valid_records, invalid_records = separate_valid_invalid_records(processed_results)
    
    # Create output directory structure
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(input_file_path)))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    invalid_dir = os.path.join(base_dir, 'data', 'invalid')
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(invalid_dir, exist_ok=True)
    
    # Generate timestamped filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    processed_file = os.path.join(processed_dir, f'processed_transactions_{timestamp}.csv')
    invalid_file = os.path.join(invalid_dir, f'invalid_transactions_{timestamp}.csv')
    
    # Save processed data
    save_processed_data(valid_records, processed_file)
    save_invalid_data(invalid_records, invalid_file)
    
    # Generate processing summary
    summary = generate_processing_summary(valid_records, invalid_records)
    
    # Log processing details
    log_processing_details(summary)
    
    # Clear duplicate tracker
    processed_transaction_ids.clear()
    
    return summary


def load_raw_data(file_path):
    """
    Load raw CSV file into memory/dataframe.

    Args:
        file_path: Path to raw CSV file

    Returns:
        Raw dataset
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return None


def process_single_record(record):
    """
    Process one transaction record.

    Responsibilities:
    - Validate record
    - Clean/normalize fields
    - Return processed record or failure reason

    Args:
        record: Single transaction row

    Returns:
        Processed record result
    """
    # Validate record
    is_valid, validation_errors = validate_record(record)
    
    if not is_valid:
        return {
            'status': 'invalid',
            'record': record.to_dict(),
            'errors': validation_errors
        }
    
    # Clean record
    cleaned_record = clean_record(record)
    
    return {
        'status': 'valid',
        'record': cleaned_record,
        'errors': None
    }


def validate_record(record):
    """
    Validate transaction record.

    Checks:
    - Missing fields
    - Invalid dates
    - Invalid amount
    - Invalid category (after cleaning)
    - Duplicate transaction

    Args:
        record: Single transaction row

    Returns:
        Validation result (is_valid: bool, errors: list)
    """
    errors = []
    
    # Check for missing required fields
    required_fields = ['transaction_id', 'date', 'amount', 'category']
    for field in required_fields:
        if field not in record or pd.isna(record[field]) or record[field] == '':
            errors.append(f"Missing required field: {field}")
    
    # If critical fields are missing, return early
    if errors:
        return False, errors
    
    # Check for duplicate transaction
    transaction_id = record['transaction_id']
    if transaction_id in processed_transaction_ids:
        errors.append(f"Duplicate transaction_id: {transaction_id}")
    else:
        processed_transaction_ids.add(transaction_id)
    
    # Validate date (handles multiple formats: YYYY-MM-DD, MM/DD/YYYY, DD-MM-YY, DD-MM-YYYY, etc.)
    date_valid, date_error = validate_date(record['date'])
    if not date_valid:
        errors.append(f"Date validation failed: {date_error}")
    
    # Validate amount (handles currency symbols: Rs., ₹, $, and INR suffix)
    amount_valid, amount_error = validate_amount(record['amount'])
    if not amount_valid:
        errors.append(f"Amount validation failed: {amount_error}")
    
    # Clean category first (to handle typos and variations), then validate
    cleaned_category = clean_category(record['category'])
    category_valid, category_error = validate_category(cleaned_category)
    if not category_valid:
        errors.append(f"Category validation failed: {category_error} (original: {record['category']})")
    
    # Validate location (optional field, cleaned version handles null/N/A)
    if 'location' in record:
        cleaned_location = clean_location(record['location'])
        location_valid, location_error = validate_location(cleaned_location)
        if not location_valid:
            errors.append(f"Location validation failed: {location_error}")
    
    # Validate notes (optional field, cleaned version handles special characters)
    if 'notes' in record:
        cleaned_notes = clean_notes(record['notes'])
        notes_valid, notes_error = validate_notes(cleaned_notes)
        if not notes_valid:
            errors.append(f"Notes validation failed: {notes_error}")
    
    # Validate payment_mode (optional field, cleaned version standardizes values)
    if 'payment_mode' in record:
        cleaned_payment_mode = clean_payment_mode(record['payment_mode'])
        payment_mode_valid, payment_mode_error = validate_payment_mode(cleaned_payment_mode)
        if not payment_mode_valid:
            errors.append(f"Payment mode validation failed: {payment_mode_error}")
    
    if errors:
        return False, errors
    
    return True, None


def clean_record(record):
    """
    Normalize and clean transaction fields.

    Responsibilities:
    - Standardize dates to YYYY-MM-DD format (handles multiple input formats)
    - Clean amount format (removes currency symbols: Rs., ₹, $, INR)
    - Normalize category names (fixes typos and standardizes variations)
    - Clean location (null/N/A → "Unknown", standardize city codes)
    - Clean notes (remove special characters, null invalid values)
    - Clean payment_mode (standardize variations: csh→cash, Bank Transfer→bank_transfer)
    - Trim unwanted spaces/symbols

    Args:
        record: Single transaction row

    Returns:
        Cleaned record dictionary
    """
    cleaned = record.copy()
    
    # Clean date - converts all formats to YYYY-MM-DD
    # Handles: YYYY-MM-DD, MM/DD/YYYY, DD-MM-YY, DD-MM-YYYY
    if 'date' in cleaned:
        cleaned['date'] = clean_date(cleaned['date'])
    
    # Clean amount - removes currency symbols and standardizes
    # Handles: plain numbers, Rs.XXX, ₹XXX, $XXX, XXX INR
    if 'amount' in cleaned:
        cleaned['amount'] = clean_amount(cleaned['amount'])
    
    # Clean category - fixes typos and standardizes names
    # Examples: Fod→Food, Educaton→Education, Utilties→Utilities
    if 'category' in cleaned:
        cleaned['category'] = clean_category(cleaned['category'])
    
    # Clean location - standardizes city codes and handles null/N/A
    # Examples: BAN→Bangalore, N/A→Unknown, null→Unknown
    if 'location' in cleaned:
        cleaned['location'] = clean_location(cleaned['location'])
    
    # Clean notes - removes special characters and invalid placeholders
    # Examples: "..."→null, "test"→null, "asdfgh"→null
    if 'notes' in cleaned:
        cleaned['notes'] = clean_notes(cleaned['notes'])
    
    # Clean payment_mode - standardizes variations
    # Examples: csh→cash, Bank Transfer→bank_transfer, null→unknown
    if 'payment_mode' in cleaned:
        cleaned['payment_mode'] = clean_payment_mode(cleaned['payment_mode'])
    
    # Clean remaining string fields (trim whitespace)
    string_fields = ['transaction_type']
    for field in string_fields:
        if field in cleaned and pd.notna(cleaned[field]):
            cleaned[field] = str(cleaned[field]).strip()
    
    return cleaned


def separate_valid_invalid_records(processed_results):
    """
    Separate successful and failed records.

    Args:
        processed_results: List of processed record results

    Returns:
        valid_records
        invalid_records
    """
    valid_records = []
    invalid_records = []
    
    for result in processed_results:
        if result['status'] == 'valid':
            valid_records.append(result['record'])
        else:
            # Add error information to the invalid record
            invalid_record = result['record'].copy()
            invalid_record['failure_reasons'] = '; '.join(result['errors'])
            invalid_records.append(invalid_record)
    
    return valid_records, invalid_records


def save_processed_data(valid_records, output_file_path):
    """
    Save cleaned valid records to processed folder.

    Args:
        valid_records: Clean dataset
        output_file_path: Destination path

    Returns:
        None
    """
    if not valid_records:
        print("No valid records to save")
        return
    
    try:
        df = pd.DataFrame(valid_records)
        # Save to CSV - notes field now uses "NaN" string for empty values
        df.to_csv(output_file_path, index=False)
        print(f"Saved {len(valid_records)} valid records to {output_file_path}")
    except Exception as e:
        print(f"Error saving processed data: {str(e)}")


def save_invalid_data(invalid_records, output_file_path):
    """
    Save invalid records with failure reasons.

    Args:
        invalid_records: Failed dataset
        output_file_path: Destination path

    Returns:
        None
    """
    if not invalid_records:
        print("No invalid records to save")
        return
    
    try:
        df = pd.DataFrame(invalid_records)
        # Save to CSV
        df.to_csv(output_file_path, index=False)
        print(f"Saved {len(invalid_records)} invalid records to {output_file_path}")
    except Exception as e:
        print(f"Error saving invalid data: {str(e)}")


def generate_processing_summary(valid_records, invalid_records):
    """
    Generate processing statistics.

    Example:
    - total records
    - valid count
    - invalid count
    - duplicate count

    Args:
        valid_records: Clean records
        invalid_records: Failed records

    Returns:
        Summary dictionary
    """
    total_count = len(valid_records) + len(invalid_records)
    valid_count = len(valid_records)
    invalid_count = len(invalid_records)
    
    # Count duplicates
    duplicate_count = 0
    for record in invalid_records:
        if 'failure_reasons' in record and 'Duplicate' in str(record['failure_reasons']):
            duplicate_count += 1
    
    summary = {
        'status': 'success',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_records': total_count,
        'valid_records': valid_count,
        'invalid_records': invalid_count,
        'duplicate_records': duplicate_count,
        'success_rate': round((valid_count / total_count * 100), 2) if total_count > 0 else 0
    }
    
    return summary


def log_processing_details(summary):
    """
    Log processing execution details.

    Args:
        summary: Processing statistics

    Returns:
        None
    """
    print("\n" + "="*60)
    print("TRANSACTION PROCESSING SUMMARY")
    print("="*60)
    print(f"Timestamp:        {summary['timestamp']}")
    print(f"Total Records:    {summary['total_records']}")
    print(f"Valid Records:    {summary['valid_records']}")
    print(f"Invalid Records:  {summary['invalid_records']}")
    print(f"Duplicate Records: {summary['duplicate_records']}")
    print(f"Success Rate:     {summary['success_rate']}%")
    print("="*60 + "\n")
