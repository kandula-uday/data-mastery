import pandas as pd

df = pd.read_csv('/Users/udayshankar/Documents/JOB/FinanceFlow/data/raw/budgetwise_finance_dataset.csv')
dates = df['date'].dropna().head(100).tolist()

print('Date samples from CSV:')
print('=' * 50)
for i, d in enumerate(dates, 1):
    print(f"{i}. {d}")
