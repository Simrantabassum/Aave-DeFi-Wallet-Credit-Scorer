import pandas as pd
import matplotlib.pyplot as plt

scores = pd.read_csv('wallet_scores.csv')
plt.figure(figsize=(10,6))
plt.hist(scores['credit_score'], bins=range(0, 1100, 100), edgecolor='black')
plt.title('Wallet Credit Score Distribution')
plt.xlabel('Credit Score Range')
plt.ylabel('Number of Wallets')
plt.xticks(range(0, 1100, 100))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('score_distribution.png')
plt.show()
