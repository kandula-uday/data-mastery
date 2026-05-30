"""
Verify notes field cleaning
"""
import pandas as pd

# Read the processed file
df = pd.read_csv('data/processed/processed_transactions_20260530_090313.csv')

print('='*60)
print('NOTES FIELD VERIFICATION - WITH NaN VALUES')
print('='*60)

print('\n1. SAMPLE RECORDS (first 20 rows):')
print(df[['transaction_id', 'category', 'amount', 'payment_mode', 'location', 'notes']].head(20).to_string())

print('\n2. NOTES VALUE COUNTS (showing top 20 unique values):')
print(df['notes'].value_counts().head(20))

print(f'\n3. STATISTICS:')
print(f'   - Total records: {len(df)}')
print(f'   - Records with "NaN" in notes: {len(df[df["notes"] == "NaN"])}')
print(f'   - Records with valid notes: {len(df[df["notes"] != "NaN"])}')
print(f'   - Percentage with NaN: {(len(df[df["notes"] == "NaN"]) / len(df) * 100):.2f}%')

print('\n4. CHECKING FOR OLD INVALID PATTERNS:')
print(f'   - Records with "..." in notes: {len(df[df["notes"] == "..."])}')
print(f'   - Records with "!!!" in notes: {len(df[df["notes"] == "!!!"])}')
print(f'   - Records with "test" in notes: {len(df[df["notes"] == "test"])}')
print(f'   - Records with "xyz123" in notes: {len(df[df["notes"] == "xyz123"])}')

print('\n5. CHECKING ALL CLEANING RESULTS:')
print(f'   ✓ Location "Unknown": {len(df[df["location"] == "Unknown"])}')
print(f'   ✓ Payment mode "unknown": {len(df[df["payment_mode"] == "unknown"])}')
print(f'   ✓ Notes "NaN": {len(df[df["notes"] == "NaN"])}')
print(f'   ✓ No "BAN" in location: {len(df[df["location"] == "BAN"]) == 0}')
print(f'   ✓ No "csh" in payment_mode: {len(df[df["payment_mode"] == "csh"]) == 0}')
print(f'   ✓ No "..." in notes: {len(df[df["notes"] == "..."]) == 0}')
