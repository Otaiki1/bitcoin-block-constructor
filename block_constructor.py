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
    blocks = []
    current_block_transactions = []
    current_block_weight = 0

    for txid in sorted_txids:
        if block_weight + mempool[txid]['weight'] <= block_weight_limit and can_include(txid):
            current_block_transactions.append(txid)
            current_block_weight += mempool[txid]['weight']
            block_weight += mempool[txid]['weight']
        else:
            blocks.append(current_block_transactions)
            current_block_transactions = [txid]
            current_block_weight = mempool[txid]['weight']
            block_weight = mempool[txid]['weight']

    # Add the last block if it's not empty
    if current_block_transactions:
        blocks.append(current_block_transactions)

    return blocks

def write_blocks_to_files(blocks):
    for i, block_transactions in enumerate(blocks):
        output_file_path = f"./block_sample_{i}.txt"
        with open(output_file_path, 'w') as file:
            for txid in block_transactions:
                file.write(txid + '\n')

def main():
    mempool_file_path = "./mempool.csv"
    mempool = read_mempool_csv(mempool_file_path)
    blocks = construct_block(mempool)
    write_blocks_to_files(blocks)

if __name__ == "__main__":
    main()
