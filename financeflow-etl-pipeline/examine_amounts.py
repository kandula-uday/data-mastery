import pandas as pd

df = pd.read_csv('/Users/udayshankar/Documents/JOB/FinanceFlow/data/raw/budgetwise_finance_dataset.csv')
amounts = df['amount'].dropna().head(100).tolist()

print('Amount samples from CSV:')
print('=' * 50)
for i, amt in enumerate(amounts, 1):
    print(f"{i}. {amt}")
