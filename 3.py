# by GPT4
import hashlib

def hash_block(block):
    sha256 = hashlib.sha256()
    sha256.update(block)
    return sha256.digest()

def process_file(filename):
    BLOCK_SIZE = 1024
    blocks = []

    with open(filename, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if not block:
                break
            blocks.append(block)

    if len(blocks) > 1:
        for i in reversed(range(len(blocks) - 1)):
            block_hash = hash_block(blocks[i+1])
            blocks[i] += block_hash
    
    print(hash_block(blocks[0]).hex())

    # output_filename = f"{filename}_processed"
    # with open(output_filename, 'wb') as f:
    #     for block in blocks:
    #         f.write(block)

    # print(f"Processed file saved as {output_filename}")

if __name__ == "__main__":
    filename = "3.1.mp4"
    process_file(filename)
