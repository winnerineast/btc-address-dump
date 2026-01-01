import struct


def ROL(s, x):
    return ((x << s) & 0xFFFFFFFF) | (x >> (32 - s))


# Boolean functions used in RIPEMD-160
def F0(x, y, z): return x ^ y ^ z


def F1(x, y, z): return (x & y) | (~x & z)


def F2(x, y, z): return (x | ~y) ^ z


def F3(x, y, z): return (x & z) | (y & ~z)


def F4(x, y, z): return x ^ (y | ~z)


def ripemd160_compress(input_bytes):
    # Initial State
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # Unpack 64 bytes into 16 32-bit words
    # Note: Ensure input_bytes is exactly 64 bytes
    x = struct.unpack('<16L', bytes(input_bytes))

    # --- Configuration for Rounds ---
    # Left Branch: Word Selection, Rotation, and Constant
    l_idx = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Round 1
        [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8],  # Round 2
        [3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12],  # Round 3
        [1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2],  # Round 4
        [4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]  # Round 5
    ]
    l_rot = [
        [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
        [7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12],
        [11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5],
        [11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12],
        [9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    ]

    # Right Branch: Word Selection, Rotation, and Constant
    r_idx = [
        [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12],
        [6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2],
        [15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13],
        [8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14],
        [12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    ]
    r_rot = [
        [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6],
        [9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11],
        [9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5],
        [15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8],
        [8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    ]

    l_constants = [0, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    r_constants = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0]
    funcs = [F0, F1, F2, F3, F4]

    # Initialize Left and Right working variables
    al, bl, cl, dl, el = h
    ar, br, cr, dr, er = h

    # Execute 5 Rounds
    for round_i in range(5):
        f = funcs[round_i]
        rf = funcs[4 - round_i]  # Right branch uses functions in reverse order

        kl = l_constants[round_i]
        kr = r_constants[round_i]

        for i in range(16):
            # Left Branch Step
            # Only add kl if it's non-zero to satisfy your simplification request
            val_l = (al + f(bl, cl, dl) + x[l_idx[round_i][i]] + kl) & 0xFFFFFFFF
            al = (ROL(l_rot[round_i][i], val_l) + el) & 0xFFFFFFFF
            cl = ROL(10, cl)
            # Register shift: a, b, c, d, e -> e, a, b, c, d (implicitly handled by assignments)
            al, bl, cl, dl, el = el, al, bl, cl, dl

            # Right Branch Step
            val_r = (ar + rf(br, cr, dr) + x[r_idx[round_i][i]] + kr) & 0xFFFFFFFF
            ar = (ROL(r_rot[round_i][i], val_r) + er) & 0xFFFFFFFF
            cr = ROL(10, cr)
            ar, br, cr, dr, er = er, ar, br, cr, dr

    # Final State Update
    temp = (h[1] + cl + dr) & 0xFFFFFFFF
    h[1] = (h[2] + dl + er) & 0xFFFFFFFF
    h[2] = (h[3] + el + ar) & 0xFFFFFFFF
    h[3] = (h[4] + al + br) & 0xFFFFFFFF
    h[4] = (h[0] + bl + cr) & 0xFFFFFFFF
    h[0] = temp

    return h


out1 = b'C\xbe\x0fx\xd3=\xe6e\xa1\xf0H\x98W\xd6\x1a\xbc\xd5R\xa3\xea\x1aC\x8d\xb3J\xedRX\x1f\x91F?'
state = ripemd160_compress(out1+ bytes([128] + [0] * 23) + b'\x00\x01\x00\x00\x00\x00\x00\x00')
if state == [2465451037, 1654346665, 1913825899, 1308931813, 2220548396]:
    print("success")