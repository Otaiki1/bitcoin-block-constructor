import csv

def read_mempool_csv(file_path):
    mempool = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            txid, fee, weight, parent_txids = row
            fee = int(fee)
            weight = int(weight)
            parents = parent_txids.split(";") if parent_txids else []
            mempool[txid] = {'fee': fee, 'weight': weight, 'parents': parents}
    return mempool

def construct_block(mempool):
    block_weight_limit = 4000000
    block_weight = 0
    block_transactions = []

    def can_include(txid):
        if txid in block_transactions:
            return False
        for parent_txid in mempool[txid]['parents']:
            if parent_txid not in block_transactions:
                return False
        return True

    sorted_txids = sorted(mempool.keys(), key=lambda x: mempool[x]['fee'], reverse=True)
    for txid in sorted_txids:
        if block_weight + mempool[txid]['weight'] <= block_weight_limit and can_include(txid):
            block_transactions.append(txid)
            block_weight += mempool[txid]['weight']

    return block_transactions

def write_block_transactions_to_file(block_transactions, file_path):
    with open(file_path, 'w') as file:
        for txid in block_transactions:
            file.write(txid + '\n')

def main():
    mempool_file_path = "./mempool.csv"
    mempool = read_mempool_csv(mempool_file_path)
    block_transactions = construct_block(mempool)
    output_file_path = "./block_sample.txt"
    write_block_transactions_to_file(block_transactions, output_file_path)

if __name__ == "__main__":
    main()
