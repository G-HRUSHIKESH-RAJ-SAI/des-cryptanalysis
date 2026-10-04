import sys, ast
from tabulate import tabulate

# Prints the DDT data in aligned table
def print_concise_ddt(ddt_list_of_dicts):

    if not ddt_list_of_dicts:
        print("DDT data is empty.")
        return

    # Get all unique Delta Y values (column headers)
    all_delta_y = sorted(set(key for d in ddt_list_of_dicts for key in d.keys()))
    
    # Define the header row (including ΔX column)
    headers = ["\u2193 ΔX"] + [f"ΔY={dy}" for dy in all_delta_y]

    # Create the rows for tabulate
    table_data = []
    
    for dx, d_row in enumerate(ddt_list_of_dicts):
        # Start the row with the ΔX value
        row = [dx]
        
        # Add the count for each ΔY, using 0 if the key is missing
        for dy in all_delta_y:
            row.append(d_row.get(dy, 0))
            
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

def main():
    if len(sys.argv) != 2:
        print("Usage: python sbox_analysis.py <S-boxes_file>")
        sys.exit(0)
    file_path = sys.argv[1]

    with open(file_path, 'r') as f:
        content = f.read().split('=')[-1].strip()
    s_boxes = ast.literal_eval(content) # to read from files as string and to convert to list of list of lists 

    s = 1
    high_prob_diff =[]

    for s_box in s_boxes:
        diff_dist = [{i:0 for i in range(16)} for _ in range(64)]
        for i in range(64):
            for j in range(64):
                diff = i ^ j    # ΔX
                binary_i = bin(i)[2:].zfill(6)
                r_i, c_i = int(binary_i[0]+binary_i[-1], base=2), int(binary_i[1:-1], base=2)   #r_i: row of sbox, c_i: col of sbox
                y_i = s_box[r_i][c_i]

                binary_j = bin(j)[2:].zfill(6)
                r_j, c_j = int(binary_j[0]+binary_j[-1], base=2), int(binary_j[1:-1], base=2)
                y_j = s_box[r_j][c_j]

                y_diff = y_i ^ y_j  # ΔY
                diff_dist[diff][y_diff] += 1

        diff_dist_prob = [{i:0 for i in range(16)} for _ in range(64)]
        for d in range(64):
            for i in range(16):
                diff_dist_prob[d][i] = diff_dist[d][i] / 64
            diff_dist_prob[d] = dict(sorted(diff_dist_prob[d].items(), key=lambda item: item[1], reverse=True))

        new_diff_dist = [{} for _ in range(64)]
        for i in range(64):
            for j in range(16):
                if diff_dist[i][j] >= 24:
                    new_diff_dist[i][j] = diff_dist_prob[i][j]
        high_prob_diff.append(new_diff_dist)

        print(f"\n=============\n S-box {s} DDT\n=============")
        print_concise_ddt(diff_dist)

        s += 1

    print("\nHigh Probability Differentials...\n")
    for s in range(1,9):
        print(f"============\nFor S-box {s} :")
        for i in range(64):
            if high_prob_diff[s-1][i] != {}:
                print(f"  ΔX:{i} ==> ΔY:  {high_prob_diff[s-1][i]}")
    print()

if __name__ == '__main__':
    main()