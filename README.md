# Aave-DeFi-Wallet-Credit-Scorer
# Credit Scoring for Aave V2 Wallets

## Overview
This project assigns a credit score (0–1000) to each wallet address based on historical transaction behavior on the Aave V2 protocol. The score reflects the reliability and responsibility of each wallet, using only transaction-level data.

## Features Engineered
- **transaction_count**: Number of transactions by the wallet.
- **total_deposit**: Total amount deposited.
- **total_borrow**: Total amount borrowed.
- **total_repay**: Total amount repaid.
- **total_redeem**: Total amount redeemed.
- **total_liquidation**: Total amount liquidated (lower is better).
- **average_transaction_size**: Mean transaction size.
- **time_since_last_transaction**: Recency of activity (more recent is better).
- **time_since_first_transaction**: Longevity of wallet activity.
- **unique_actions**: Number of unique action types performed.
- **repay_borrow_ratio**: Ratio of repaid to borrowed amount.
- **deposit_borrow_ratio**: Ratio of deposited to borrowed amount.
- **repay_borrow_count_ratio**: Ratio of repay to borrow actions.

## Scoring Logic
- Each feature is normalized (min-max scaling).
- Features are combined using a weighted sum (see code for weights).
- Higher scores indicate more responsible, less risky behavior.
- Scores are clipped to the range [0, 1000].

## How to Run
1. Place `user-transactions.json` in the same directory as `credit_score.py`.
2. Run the script:
   ```
   python credit_score.py
   ```
3. The output file `wallet_scores.csv` will contain wallet addresses and their credit scores.

## Extensibility
- The scoring logic and feature weights can be easily adjusted in the script.
- Additional features can be engineered as needed.
