import pandas as pd
import json

# Load the JSON data
with open('user-transactions.json') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.json_normalize(data)

# Step 3: Feature Engineering
def feature_engineering(df):
    features = {}
    for wallet in df['userWallet'].unique():
        wallet_data = df[df['userWallet'] == wallet]
        deposit = wallet_data[wallet_data['action'] == 'deposit']['actionData.amount'].astype(float).sum()
        borrow = wallet_data[wallet_data['action'] == 'borrow']['actionData.amount'].astype(float).sum()
        repay = wallet_data[wallet_data['action'] == 'repay']['actionData.amount'].astype(float).sum()
        redeem = wallet_data[wallet_data['action'] == 'redeemunderlying']['actionData.amount'].astype(float).sum()
        liquidation = wallet_data[wallet_data['action'] == 'liquidationcall']['actionData.amount'].astype(float).sum() if 'liquidationcall' in wallet_data['action'].values else 0
        tx_count = len(wallet_data)
        avg_tx_size = wallet_data['actionData.amount'].astype(float).mean()
        time_since_last = (pd.to_datetime('now') - pd.to_datetime(wallet_data['timestamp'])).dt.total_seconds().max()
        time_since_first = (pd.to_datetime('now') - pd.to_datetime(wallet_data['timestamp'])).dt.total_seconds().min()
        unique_actions = wallet_data['action'].nunique()
        repay_borrow_ratio = repay / borrow if borrow > 0 else 0
        deposit_borrow_ratio = deposit / borrow if borrow > 0 else 0
        repay_count = len(wallet_data[wallet_data['action'] == 'repay'])
        borrow_count = len(wallet_data[wallet_data['action'] == 'borrow'])
        repay_borrow_count_ratio = repay_count / borrow_count if borrow_count > 0 else 0
        features[wallet] = {
            'transaction_count': tx_count,
            'total_deposit': deposit,
            'total_borrow': borrow,
            'total_repay': repay,
            'total_redeem': redeem,
            'total_liquidation': liquidation,
            'average_transaction_size': avg_tx_size,
            'time_since_last_transaction': time_since_last,
            'time_since_first_transaction': time_since_first,
            'unique_actions': unique_actions,
            'repay_borrow_ratio': repay_borrow_ratio,
            'deposit_borrow_ratio': deposit_borrow_ratio,
            'repay_borrow_count_ratio': repay_borrow_count_ratio
        }
    return pd.DataFrame.from_dict(features, orient='index')

def score_wallets(features_df):
    # Normalize features (min-max scaling)
    norm = lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else x
    features_norm = features_df.copy()
    for col in ['transaction_count', 'total_deposit', 'total_borrow', 'total_repay', 'total_redeem',
                'average_transaction_size', 'unique_actions', 'repay_borrow_ratio', 'deposit_borrow_ratio', 'repay_borrow_count_ratio']:
        features_norm[col] = norm(features_df[col].fillna(0))
    # Lower is better for time_since_last_transaction and liquidation
    features_norm['time_since_last_transaction'] = 1 - norm(features_df['time_since_last_transaction'].fillna(0))
    features_norm['total_liquidation'] = 1 - norm(features_df['total_liquidation'].fillna(0))
    # Weighted sum (weights can be tuned)
    score = (
        0.15 * features_norm['transaction_count'] +
        0.15 * features_norm['total_deposit'] +
        0.10 * features_norm['total_repay'] +
        0.10 * features_norm['repay_borrow_ratio'] +
        0.10 * features_norm['deposit_borrow_ratio'] +
        0.10 * features_norm['repay_borrow_count_ratio'] +
        0.10 * features_norm['unique_actions'] +
        0.05 * features_norm['average_transaction_size'] +
        0.10 * features_norm['time_since_last_transaction'] +
        0.05 * features_norm['total_liquidation']
    )
    features_df['credit_score'] = (score * 1000).clip(0, 1000).round(0).astype(int)
    return features_df

if __name__ == "__main__":
    features_df = feature_engineering(df)  # Call the feature engineering function
    features_df = score_wallets(features_df)  # Score wallets
    print(features_df[['credit_score']].head())  # Display first few scores
    features_df[['credit_score']].to_csv('wallet_scores.csv')  # Save scores to CSV
