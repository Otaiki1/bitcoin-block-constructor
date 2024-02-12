import csv

# Function to read mempool CSV file and parse transactions
def read_mempool_csv(file_path):
    mempool = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            txid, fee, weight, parent_txids = row
            fee = int(fee)
            weight = int(weight)
            parents = parent_txids.split(";") if parent_txids else []  # Split parent txids if available
            mempool[txid] = {'fee': fee, 'weight': weight, 'parents': parents}
    return mempool

# Function to construct blocks
def construct_block(mempool):
    block_weight_limit = 4000000  # Block weight limit
    block_weight = 0  # Current block weight
    block_transactions = []  # List to store transactions in current block
    blocks = []  # List to store all blocks

    # Function to check if a transaction can be included in the block
    def can_include(txid):
        if txid in block_transactions:  # Check if transaction is already included in current block
            return False
        for parent_txid in mempool[txid]['parents']:  # Check if all parent transactions are included
            if parent_txid not in block_transactions:
                return False
        return True

    sorted_txids = sorted(mempool.keys(), key=lambda x: mempool[x]['fee'], reverse=True)  # Sort transactions by fee
    current_block_transactions = []  # Transactions in current block
    current_block_weight = 0  # Current block weight

    # Iterate through sorted transactions
    for txid in sorted_txids:
        # Check if adding the transaction exceeds block weight limit and if it can be included
        if block_weight + mempool[txid]['weight'] <= block_weight_limit and can_include(txid):
            current_block_transactions.append(txid)  # Add transaction to current block
            current_block_weight += mempool[txid]['weight']  # Update current block weight
            block_weight += mempool[txid]['weight']  # Update block weight
        else:
            blocks.append(current_block_transactions)  # Add current block to blocks list
            current_block_transactions = [txid]  # Start a new block with this transaction
            current_block_weight = mempool[txid]['weight']  # Update current block weight
            block_weight = mempool[txid]['weight']  # Update block weight

    # Add the last block if it's not empty
    if current_block_transactions:
        blocks.append(current_block_transactions)

    return blocks  # Return list of blocks

# Function to write blocks to text files
def write_blocks_to_files(blocks):
    for i, block_transactions in enumerate(blocks):
        output_file_path = f"./block_sample_{i+1}.txt"  # Output file path for each block
        with open(output_file_path, 'w') as file:
            for txid in block_transactions:
                file.write(txid + '\n')  # Write transaction txid to file

# Main function
def main():
    mempool_file_path = "./mempool.csv"
    mempool = read_mempool_csv(mempool_file_path)  # Read mempool CSV file
    blocks = construct_block(mempool)  # Construct blocks
    write_blocks_to_files(blocks)  # Write blocks to text files

if __name__ == "__main__":
    main()
