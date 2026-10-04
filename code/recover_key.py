import random, requests, sys

# Weakened S-boxes
WEAK_S_BOXES = [
    # S1
    [[14, 1, 6, 3, 8, 5, 7, 10, 13, 9, 15, 12, 2, 4, 11, 0], 
     [15, 14, 2, 3, 4, 5, 7, 8, 6, 9, 0, 11, 12, 13, 1, 10], 
     [15, 1, 5, 3, 7, 2, 8, 13, 4, 9, 6, 11, 14, 10, 12, 0], 
     [4, 1, 5, 3, 8, 2, 6, 7, 10, 9, 15, 11, 12, 13, 14, 0]],

    # S2
    [[4, 12, 10, 3, 5, 1, 6, 2, 8, 9, 14, 11, 0, 13, 7, 15], 
     [12, 11, 9, 3, 14, 13, 6, 7, 8, 2, 10, 4, 0, 5, 1, 15], 
     [5, 14, 2, 13, 6, 4, 11, 15, 12, 9, 3, 0, 1, 10, 8, 7], 
     [1, 14, 2, 10, 7, 5, 6, 0, 8, 9, 12, 11, 4, 13, 3, 15]],

    # S3
    [[14, 12, 6, 3, 4, 5, 2, 7, 8, 9, 15, 11, 0, 13, 1, 10], 
     [0, 1, 2, 8, 13, 9, 10, 7, 3, 6, 12, 11, 4, 5, 14, 15], 
     [4, 1, 5, 3, 13, 2, 11, 7, 15, 9, 12, 0, 6, 8, 14, 10], 
     [0, 6, 2, 3, 7, 15, 10, 4, 13, 9, 1, 11, 14, 8, 12, 5]],

    # S4 
    [[12, 1, 0, 14, 4, 5, 6, 3, 10, 9, 2, 13, 8, 11, 7, 15], 
     [0, 1, 2, 15, 4, 5, 8, 7, 9, 12, 10, 11, 3, 13, 14, 6], 
     [3, 1, 2, 0, 9, 5, 11, 7, 6, 4, 13, 15, 14, 10, 12, 8], 
     [0, 1, 9, 3, 4, 5, 2, 7, 11, 15, 10, 8, 13, 12, 6, 14]],

    # S5
    [[14, 1, 7, 3, 8, 5, 6, 2, 4, 9, 10, 11, 0, 13, 12, 15], 
     [2, 5, 14, 3, 9, 4, 11, 7, 8, 1, 13, 6, 15, 10, 0, 12], 
     [0, 1, 5, 13, 7, 12, 10, 4, 3, 9, 2, 11, 14, 6, 8, 15], 
     [12, 1, 6, 9, 2, 5, 3, 8, 13, 7, 14, 0, 4, 11, 10, 15]],

    # S6
    [[0, 5, 2, 3, 8, 1, 6, 7, 4, 9, 15, 11, 12, 13, 14, 10], 
     [0, 1, 14, 3, 4, 5, 11, 10, 12, 9, 7, 6, 8, 13, 2, 15], 
     [12, 1, 2, 3, 4, 0, 11, 7, 6, 9, 15, 8, 5, 13, 14, 10], 
     [6, 3, 2, 1, 4, 5, 10, 7, 8, 9, 14, 11, 15, 13, 0, 12]],

    # S7
    [[2, 3, 1, 6, 5, 7, 4, 6, 9, 8, 11, 10, 13, 15, 14, 12], 
     [1, 0, 2, 3, 5, 4, 7, 6, 10, 11, 8, 9, 15, 12, 13, 14], 
     [1, 2, 3, 0, 4, 7, 5, 6, 8, 10, 9, 11, 12, 14, 15, 13], 
     [2, 1, 0, 3, 5, 7, 6, 4, 8, 10, 13, 9, 13, 14, 12, 15]],

    # S8
    [[12, 14, 7, 3, 9, 5, 6, 2, 10, 4, 8, 11, 1, 13, 0, 15], 
     [0, 11, 7, 3, 15, 5, 6, 2, 8, 9, 10, 1, 12, 13, 14, 4], 
     [0, 1, 9, 14, 4, 2, 10, 5, 13, 7, 15, 11, 12, 8, 3, 6], 
     [0, 1, 2, 3, 7, 5, 6, 4, 14, 11, 13, 9, 8, 10, 12, 15]]  

]

# Expansion Permutation (E) table
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation (P) table
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9, 
    19, 13, 30, 6, 
    22, 11, 4, 25
]

# Key Permutation (PC1) table
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Key Permutation (PC2) table
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_SCHEDULE = [1, 1, 2, 2]

# To convert from decimal to binary
def to_bin(n, length):
    return bin(n)[2:].zfill(length)

# To convert from hex to binary
def hex_to_bin(n, length):
    return bin(int(n, 16))[2:].zfill(length)

# To convert from binary to hex
def bin_to_hex(n, length):
    return hex(int(n, 2))[2:].zfill(length).upper()

def permute(input_bits, table):
    return [input_bits[i - 1] for i in table]

# To invert the mixing permutation
def reverse_permute(input_bits, table):
    return [input_bits[table.index(i+1)] for i in range(32)]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor_bits(a, b):
    return ''.join(str(int(a[i]) ^ int(b[i])) for i in range(len(a)))

def generate_subkeys(key):
    key_bits = permute(key, PC1)
    left = key_bits[:28]
    right = key_bits[28:]
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        left = left_shift(left, shift)
        right = left_shift(right, shift)
        combined = left + right
        subkey = permute(combined, PC2)
        subkeys.append(subkey)
    return subkeys

def s_box_substitution(bits):
    result = []
    for i in range(8):
        chunk = bits[i * 6:(i + 1) * 6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(''.join(chunk[1:5]), 2)
        sbox_val = WEAK_S_BOXES[i][row][col]
        result.extend(list(to_bin(sbox_val, 4)))
    return result

# Perform the Feistel function
def feistel(right, subkey):
    # Expand the right half
    expanded = permute(right, E)
    # XOR with the subkey
    xor_result = [str(int(expanded[i]) ^ int(subkey[i])) for i in range(48)]

    substituted = s_box_substitution(xor_result)
    
    permuted = permute(substituted, P)
    return permuted

# generate random pt pairs (in binary) satisfying the given input differential
def get_plaintext_pairs(count, differential):
    pt_pairs = []
    diff_int = int(differential, 16)
    for _ in range(count):

        p1 = bin(random.getrandbits(64))[2:].zfill(64)  #generate random P1
        p2 = bin(int(p1, 2) ^ diff_int)[2:].zfill(64)
        if (p1,p2) not in pt_pairs:
            pt_pairs.append((p1,p2))
    return pt_pairs


CLIENT_ID = "062c7fa0df0fa12c6370071efdc9fcd6.access"
CLIENT_SECRET = "<client_secret_string"
URL = "https://des-oracle.bombaykettle.org/<roll_number>/api/encrypt"

HEADERS = {
    "CF-Access-Client-Id": CLIENT_ID,
    "CF-Access-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json"
}

#function to get ciphertext from oracle
def get_cipher(pt):
    response = requests.post(
        URL,
        headers=HEADERS,
        json={"plaintext": pt}
    )
    output = response.json()
    return output['ciphertext']

#function to generate asked no. of ptctpairs for random pt satisfying the given differential
def generate_pt_ct_pairs(pc, differential, pairs_file="queried_pairs.txt"):
    pt_pairs = get_plaintext_pairs(pc, differential)

    pt_ct_pairs = []
    for p1, p2 in pt_pairs:
        p1, p2 = hex(int(p1, 2))[2:].upper().zfill(16), hex(int(p2, 2))[2:].upper().zfill(16)
        c1, c2 = get_cipher(p1), get_cipher(p2)
        pair = f"[({p1}, {p2}), ({c1}, {c2})]"
        print(pair + f"  ΔX = {differential}")
        with open(pairs_file, 'a') as f:    # save the pair to file
            f.write(pair + "\n")
        pt_ct_pairs.append([(hex_to_bin(p1, 64), hex_to_bin(p2, 64)), (hex_to_bin(c1, 64), hex_to_bin(c2, 64))])

    return pt_ct_pairs

def des_decrypt(block, key):
    subkeys = generate_subkeys(key)[::-1]
    
    left = block[:32]
    right = block[32:]
    
    for i in range(4):
        new_left = right
        new_right = [str(int(left[j]) ^ int(feistel(right, subkeys[i])[j])) for j in range(32)]
        left, right = new_left, new_right

    # Combine without final permutation
    combined = right + left
    return ''.join(combined)


CUM_SHIFT = sum(SHIFT_SCHEDULE) 

# produce 56-length key list, filled with '0'/'1' or None
def invert_pc2(k48_bits):
    combined56 = [None]*56

    for i, pc2_pos in enumerate(PC2):   # pc2_pos is 1..56
        if k48_bits[i] != '_':
            combined56[pc2_pos - 1] = k48_bits[i]
    return combined56

# reverse the left shift
def rotate_right(bits56, r):
    r = r % 56
    left, right = bits56[:28], bits56[28:]
    return left[-r:] + left[:-r] + right[-r:] + right[:-r]

# produce 64-length key list, filled with '0'/'1' or None
def invert_pc1(combined56):

    key64 = [None]*64
    for i, pc1_pos in enumerate(PC1):  # PC1 maps masterkey positions -> 56 bits
        key64[pc1_pos - 1] = combined56[i]
    return key64

#get 48 bits of master key using 48 bits of k4
def design_masterkey(k4_bits):
    # k4_bits: string of '0'/'1/_' length 48
    combined56_after_shift = invert_pc2(k4_bits)
    combined56_before_shift = rotate_right(combined56_after_shift, CUM_SHIFT)
    key64_partial = invert_pc1(combined56_before_shift)  # length 64 with Nones

    return key64_partial


def main():

    if len(sys.argv) !=2:
        print("Usage: python recover_key.py <file_to_save_key>")
        sys.exit(0)
    key_file = sys.argv[1]
    pairs_file = "pt_ct_pairs.txt"
    try:
        with open(pairs_file, 'w') as f:
            pass
    except:
        pass

    pt_ct_pairs = []

    differ_at = 4
    done = False
    num_pt_ct_pairs = 0

    # Differentials to activate only 5th sbox
    choices = ['0000400000000000', '0000200000000000', '0000600000000000']
    choice = 0

    print("===========================")
    print("  DES Key Recovery Attack  ")
    print("===========================\n")
    print(f"The differentials used are {choices}\n")
    print("The (PT, CT) pairs used are ...\n[(P1, P2), (C1, C2)]")
    

    while not done :
        count_k = [{} for s in range(8)]

        pt_ct_pairs_new = generate_pt_ct_pairs(1, choices[choice], pairs_file)
        pt_ct_pairs.extend(pt_ct_pairs_new)

        num_pt_ct_pairs = len(pt_ct_pairs)
        
        for i in range(num_pt_ct_pairs):
            p1, p2 = pt_ct_pairs[i][0][0], pt_ct_pairs[i][0][1]
            c1, c2 = pt_ct_pairs[i][1][0], pt_ct_pairs[i][1][1]

            for s in range(8):
                # Logic to select expanded inputs from r of ciphertext (l||r)
                if s==differ_at:
                    continue
                elif s==0:
                    e1 = c1[-1] + c1[32+s*4 : 32+(s+1)*4+1]
                    e2 = c2[-1] + c2[32+s*4 : 32+(s+1)*4+1]
                elif s==7:
                    e1 = c1[32+s*4-1 : 32+(s+1)*4] + c1[32]
                    e2 = c2[32+s*4-1 : 32+(s+1)*4] + c2[32]
                else:
                    e1 = c1[32+s*4-1 : 32+(s+1)*4+1]
                    e2 = c2[32+s*4-1 : 32+(s+1)*4+1]

                # original D' difference
                d1 = c1[:32]
                d2 = c2[:32]

                # invert the mixing permutation
                d_1 = ''.join(reverse_permute(d1, P))
                d_2 = ''.join(reverse_permute(d2, P))

                y_1 = int(d_1[s*4: (s+1)*4], 2)
                y_2 = int(d_2[s*4: (s+1)*4], 2)

                y_diff_original = y_1^y_2   # original difference of s-box

                # try for all possible 2**6 subkey bits for each particular s-box
                for k in range(64):
                    i1 = bin(int(e1, 2) ^ k)[2:].zfill(6)
                    i2 = bin(int(e2, 2) ^ k)[2:].zfill(6)

                    # S-box subsitutions
                    r_i, c_i = int(i1[0]+i1[-1], base=2), int(i1[1:-1], base=2)   #r_i: row of sbox, c_i: col of sbox
                    y_i = WEAK_S_BOXES[s][r_i][c_i]

                    r_j, c_j = int(i2[0]+i2[-1], base=2), int(i2[1:-1], base=2)
                    y_j = WEAK_S_BOXES[s][r_j][c_j]

                    y_diff = y_i ^ y_j  

                    if y_diff == y_diff_original:   #check if output differences match
                        count_k[s][k] = count_k[s].get(k,0) + 1

        for s in range(8):
            if s!=differ_at:
                max_val = max(count_k[s].values())
                keys = [k for k,v in count_k[s].items() if v==max_val]

                if len(keys)>1:     # if more than one possible (6-bits) part of k4, increase (PT,CT) pairs
                    break_out = True
                    choice = (choice+1)%3
                    break
                else:
                    count_k[s] = dict(sorted(count_k[s].items(), key=lambda item: item[1], reverse=True))
                    break_out = False
            
        if break_out:
            done = False
        else:   
            done = True     # obtained unique 42 bits of k4 with enough no. of (PT, CT) pairs

    k4 = ''

    for s in range(8):
        count_k[s] = dict(sorted(count_k[s].items(), key= lambda item: item[1], reverse=True))
    
        if s!=differ_at:
            max_val = max(count_k[s].values())
            keys = [k for k,v in count_k[s].items() if v==max_val]

            k4 += bin(keys[0])[2:].zfill(6)
        else:
            k4 += '_'*6
    print(f"\nRecovered bits of k4: {k4}")

    # get partial master key from k4 
    partial_key_ls = design_masterkey(k4)

    partial_key = ''

    for i in range(64):
        if partial_key_ls[i] is not None:
            partial_key += partial_key_ls[i]
        else:
            if i%8==7:
                partial_key += '0'    # padding : to match given implementation
            else:
                partial_key += '_'

    print(f"\nPartial master key(64 bits) constructed from k4: {partial_key}\n")

    # count satisfied pairs for each possible key
    prob_key_dict = {}
    underscore_positions = [i for i, c in enumerate(partial_key) if c == '_']

    for bbits in range(16384):  # 2**14
        bin_bbits = bin(bbits)[2:].zfill(14)

        # Construct test_key as list
        test_key = list(partial_key)
        for idx, pos in enumerate(underscore_positions):
            test_key[pos] = bin_bbits[idx]
        test_key_str = ''.join(test_key)

        match_count = 0
        success = True
        
        # Test against queried pt-ct pairs
        for j in range(num_pt_ct_pairs):
            p1, p2 = pt_ct_pairs[j][0]
            c1, c2 = pt_ct_pairs[j][1]

            p1_dec = des_decrypt(list(c1), list(test_key_str))
            if p1_dec != p1:
                success = False
                break
            
            p2_dec = des_decrypt(list(c2), list(test_key_str))
            if p2_dec != p2:
                success = False
                break
            
            match_count += 1

        if success:
            prob_key_dict[test_key_str] = match_count

    final_key = None
    for key, v in prob_key_dict.items():
        
        if v == num_pt_ct_pairs:    # the key is satisfied by all pairs
            keyls = list(key)
            key_56 = ''.join([keyls[k] for k in range(64) if k%8 != 7])
            final_key = bin_to_hex(key_56, 14)
            print(f"{final_key} : Recovered Key(Hex)")
            try:
                with open(key_file, 'w') as f:
                    f.write(final_key)
            except Exception as e:
                print(f"Exception occurred: {e}")
            
        else:
            print(f"{key} satisfying {v} no. of pairs. Total no. of pairs={num_pt_ct_pairs}")
    print(f"\nThe (PT, CT) pairs are saved to {pairs_file}")
    print(f"The Recovered Key is saved to {key_file}")
    

if __name__ == "__main__":
    main()
