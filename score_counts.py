import pandas as pd

scores = pd.read_csv('wallet_scores.csv')
bins = list(range(0, 1100, 100))
labels = [f"{bins[i]}–{bins[i+1]}" for i in range(len(bins)-1)]
scores['score_range'] = pd.cut(scores['credit_score'], bins=bins, labels=labels, right=False, include_lowest=True)
counts = scores['score_range'].value_counts().sort_index()

# Prepare lines for markdown
lines = [f"- {label}: {count} wallets" for label, count in zip(labels, counts)]

# Read analysis.md
with open('analysis.md', 'r', encoding='utf-8') as f:
    analysis = f.readlines()

# Find the index to insert counts (after the image)
for i, line in enumerate(analysis):
    if '![Score Distribution]' in line:
        insert_idx = i + 1
        break
else:
    insert_idx = len(analysis)

# Remove old count lines
while insert_idx < len(analysis) and analysis[insert_idx].strip().startswith('-'):
    del analysis[insert_idx]

# Insert new counts
for line in reversed(lines):
    analysis.insert(insert_idx, line + '\n')

# Write back to analysis.md
with open('analysis.md', 'w', encoding='utf-8') as f:
    f.writelines(analysis)

# Also print to console
for line in lines:
    print(line)
