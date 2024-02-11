import csv

class Pool:
    def __init__(self, tx_id, fee, weight, parent_txids=None):
        self.tx_id = tx_id
        self.fee = fee
        self.weight = weight
        self.parent_txids = parent_txids

def main():
    MEMPOOL_FILE_PATH = "./mempool.csv"
    BLOCK_SAMPLE_PATH = "./block_sample.txt"

    pool_transactions = []

    with open(MEMPOOL_FILE_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) > 3:
                parent_ids = [p for p in row[3].split(";") if p]
                structured = Pool(row[0], int(row[1]), int(row[2]), parent_ids)
                pool_transactions.append(structured)
            else:
                structured = Pool(row[0], int(row[1]), int(row[2]))
                pool_transactions.append(structured)

    arranged_transactions = arrange_transactions(pool_transactions)
    remove_duplicate_transactions(arranged_transactions)

    with open(BLOCK_SAMPLE_PATH, 'a') as block_sample:
        for transaction in arranged_transactions:
            block_sample.write(f"{transaction.tx_id}\n")

def arrange_transactions(transactions):
    arranged_transactions = []
    for transaction in transactions:
        if transaction.parent_txids:
            for parent_tx in transaction.parent_txids:
                find_parent = next((pred for pred in transactions if pred.tx_id == parent_tx), None)
                if find_parent:
                    arranged_transactions.append(find_parent)
        else:
            arranged_transactions.append(transaction)
    return arranged_transactions

def remove_duplicate_transactions(transactions):
    transactions[:] = [t for i, t in enumerate(transactions) if t not in transactions[:i]]

if __name__ == "__main__":
    main()
