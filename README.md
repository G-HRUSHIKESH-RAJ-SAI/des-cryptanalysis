# 4-Round Custom-DES Differential Cryptanalysis

## Overview

Implementation of a differential cryptanalysis attack on a custom 4-round DES variant with weakened S-boxes. Recovers the 56-bit secret key using very few plaintext-ciphertext pairs.

## Files

| File | Description |
|------|-------------|
| `recover_key.py` | Main attack implementation; queries oracle, derives K4, brute-forces remaining bits |
| `verify_recovered_key.py` | Validates recovered key against oracle ciphertexts |
| `sbox_analysis.py` | Generates DDTs for S-boxes and identifies high-probability differentials |
| `S_BOXES.txt` | Weakened S-box definitions |
| `pt_ct_pairs.txt` | Generated plaintext-ciphertext pairs from oracle queries |
| `key.txt` | Output: recovered 56-bit key |

Place the following files in the same folder:
`sbox_analysis.py` ; 
`S_BOXES.txt` ; 
`recover_key.py` ; 
`verify_recovered_key.py`

## Setup

#### Install these packages if not already present
```bash
pip install tabulate requests
```

## Usage

### Analyze S-Boxes
```bash
python sbox_analysis.py S_BOXES.txt
```

**Output:** Differential Distribution Tables for all 8 S-boxes with high-probability differentials identified.

### Recover the Key

```bash
python recover_key.py key.txt
```

**Output:**
```
===========================
 DES Key Recovery Attack 
===========================

[Attack progress...]

64F55CD5C9B7D7 : Recovered Key(Hex)
The (PT, CT) pairs are saved to pt_ct_pairs.txt
The Recovered Key is saved to key.txt
```

### Verify the Key

```bash
python verify_recovered_key.py
```

**Interactive menu:**
```
1. Check for the (PT,CT) pairs from the file
2. Check for a new input
Please select your choice: 
```

**Output:**
```
Based on selected choice
```