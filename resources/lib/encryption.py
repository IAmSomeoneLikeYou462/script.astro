# ----------------------------------------------------------------------
# Copyright (c) 2010-2022 Marti Raudsepp <marti@juffo.org> & Someone Like You
#
# This file is part of Astro.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------


from array import array

MODE_ECB = 1
MODE_CBC = 2


class AES(object):
    def __init__(self, key, mode, IV=None):
        self.aes_sbox = array('B', [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
                                    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
                                    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
                                    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
                                    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
                                    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
                                    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
                                    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
                                    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
                                    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
                                    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
                                    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
                                    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
                                    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
                                    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
                                    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22])

        self.aes_inv_sbox = array('B', [82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251,
                                        124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203,
                                        84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78,
                                        8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37,
                                        114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146,
                                        108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132,
                                        144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6,
                                        208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107,
                                        58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115,
                                        150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110,
                                        71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27,
                                        252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244,
                                        31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95,
                                        96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239,
                                        160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97,
                                        23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125])

        self.aes_Rcon = array('B', [141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154,
                                    47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57,
                                    114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58,
                                    116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216,
                                    171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239,
                                    197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204,
                                    131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27,
                                    54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179,
                                    125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148,
                                    51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32,
                                    64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53,
                                    106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159,
                                    37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4,
                                    8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99,
                                    198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189,
                                    97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203])
        self.modeEnc = mode
        if mode != MODE_ECB and mode != MODE_CBC:
            raise NotImplementedError

        if mode == MODE_CBC:
            if IV is None:
                raise ValueError("CBC mode needs an IV value!")
            else:
                self.IV = array('B', IV)
        self.block_size = 16
        self.setkey(key)

        self.gf_mul_by_2 = array(
            'B', [self.galois_multiply(x, 2) for x in range(256)])
        self.gf_mul_by_3 = array(
            'B', [self.galois_multiply(x, 3) for x in range(256)])
        # ... for decryption
        self.gf_mul_by_9 = array(
            'B', [self.galois_multiply(x, 9) for x in range(256)])
        self.gf_mul_by_11 = array(
            'B', [self.galois_multiply(x, 11) for x in range(256)])
        self.gf_mul_by_13 = array(
            'B', [self.galois_multiply(x, 13) for x in range(256)])
        self.gf_mul_by_14 = array(
            'B', [self.galois_multiply(x, 14) for x in range(256)])

    def setkey(self, key):
        """Sets the key and performs key expansion."""

        self.key = key
        self.key_size = len(key)

        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError("Key length must be 16, 24 or 32 bytes")

        self.expand_key()

    def expand_key(self):
        """Performs AES key expansion on self.key and stores in self.exkey"""

        # The key schedule specifies how parts of the key are fed into the
        # cipher's round functions. "Key expansion" means performing this
        # schedule in advance. Almost all implementations do this.
        #
        # Here's a description of AES key schedule:
        # http://en.wikipedia.org/wiki/Rijndael_key_schedule

        # The expanded key starts with the actual key itself
        exkey = array('B', self.key)

        # extra key expansion steps
        if self.key_size == 16:
            extra_cnt = 0
        elif self.key_size == 24:
            extra_cnt = 2
        else:
            extra_cnt = 3

        # 4-byte temporary variable for key expansion
        word = exkey[-4:]
        # Each expansion cycle uses 'i' once for Rcon table lookup
        for i in range(1, 11):

            # key schedule core:
            # left-rotate by 1 byte
            word = word[1:4] + word[0:1]

            # apply S-box to all bytes
            for j in range(4):
                word[j] = self.aes_sbox[word[j]]

            # apply the Rcon table to the leftmost byte
            word[0] = word[0] ^ self.aes_Rcon[i]
            # end key schedule core

            for z in range(4):
                for j in range(4):
                    # mix in bytes from the last subkey
                    word[j] ^= exkey[-self.key_size + j]
                exkey.extend(word)

            # Last key expansion cycle always finishes here
            if len(exkey) >= (self.rounds + 1) * self.block_size:
                break

            # Special substitution step for 256-bit key
            if self.key_size == 32:
                for j in range(4):
                    # mix in bytes from the last subkey XORed with S-box of
                    # current word bytes
                    word[j] = self.aes_sbox[word[j]
                                            ] ^ exkey[-self.key_size + j]
                exkey.extend(word)

            # Twice for 192-bit key, thrice for 256-bit key
            for z in range(extra_cnt):
                for j in range(4):
                    # mix in bytes from the last subkey
                    word[j] ^= exkey[-self.key_size + j]
                exkey.extend(word)

        self.exkey = exkey

    def add_round_key(self, block, round):
        """AddRoundKey step in AES. This is where the key is mixed into plaintext"""

        offset = round * 16
        exkey = self.exkey

        for i in range(16):
            block[i] ^= exkey[offset + i]

        # print 'AddRoundKey:', block

    def sub_bytes(self, block, sbox):
        """SubBytes step, apply S-box to all bytes

        Depending on whether encrypting or decrypting, a different sbox array
        is passed in.
        """

        for i in range(16):
            block[i] = sbox[block[i]]

        # print 'SubBytes   :', block

    def shift_rows(self, b):
        """ShiftRows step. Shifts 2nd row to left by 1, 3rd row by 2, 4th row by 3

        Since we're performing this on a transposed matrix, cells are numbered
        from top to bottom::

          0  4  8 12   ->    0  4  8 12    -- 1st row doesn't change
          1  5  9 13   ->    5  9 13  1    -- row shifted to left by 1 (wraps around)
          2  6 10 14   ->   10 14  2  6    -- shifted by 2
          3  7 11 15   ->   15  3  7 11    -- shifted by 3
        """

        b[1], b[5], b[9], b[13] = b[5], b[9], b[13], b[1]
        b[2], b[6], b[10], b[14] = b[10], b[14], b[2], b[6]
        b[3], b[7], b[11], b[15] = b[15], b[3], b[7], b[11]

        # print 'ShiftRows  :', b

    def shift_rows_inv(self, b):
        """Similar to shift_rows above, but performed in inverse for decryption."""

        b[5], b[9], b[13], b[1] = b[1], b[5], b[9], b[13]
        b[10], b[14], b[2], b[6] = b[2], b[6], b[10], b[14]
        b[15], b[3], b[7], b[11] = b[3], b[7], b[11], b[15]

        # print 'ShiftRows  :', b

    def mix_columns(self, block):
        """MixColumns step. Mixes the values in each column"""

        # Cache global multiplication tables (see below)
        mul_by_2 = self.gf_mul_by_2
        mul_by_3 = self.gf_mul_by_3

        # Since we're dealing with a transposed matrix, columns are already
        # sequential
        for i in range(4):
            col = i * 4

            # v0, v1, v2, v3 = block[col : col+4]
            v0, v1, v2, v3 = (block[col], block[col + 1], block[col + 2],
                              block[col + 3])

            block[col] = mul_by_2[v0] ^ v3 ^ v2 ^ mul_by_3[v1]
            block[col + 1] = mul_by_2[v1] ^ v0 ^ v3 ^ mul_by_3[v2]
            block[col + 2] = mul_by_2[v2] ^ v1 ^ v0 ^ mul_by_3[v3]
            block[col + 3] = mul_by_2[v3] ^ v2 ^ v1 ^ mul_by_3[v0]

        # print 'MixColumns :', block

    def mix_columns_inv(self, block):
        """Similar to mix_columns above, but performed in inverse for decryption."""

        # Cache global multiplication tables (see below)
        mul_9 = self.gf_mul_by_9
        mul_11 = self.gf_mul_by_11
        mul_13 = self.gf_mul_by_13
        mul_14 = self.gf_mul_by_14

        # Since we're dealing with a transposed matrix, columns are already
        # sequential
        for i in range(4):
            col = i * 4

            v0, v1, v2, v3 = (block[col], block[col + 1], block[col + 2],
                              block[col + 3])
            # v0, v1, v2, v3 = block[col:col+4]

            block[col] = mul_14[v0] ^ mul_9[v3] ^ mul_13[v2] ^ mul_11[v1]
            block[col + 1] = mul_14[v1] ^ mul_9[v0] ^ mul_13[v3] ^ mul_11[v2]
            block[col + 2] = mul_14[v2] ^ mul_9[v1] ^ mul_13[v0] ^ mul_11[v3]
            block[col + 3] = mul_14[v3] ^ mul_9[v2] ^ mul_13[v1] ^ mul_11[v0]

        # print 'MixColumns :', block

    def encrypt_block(self, block):
        """Encrypts a single block. This is the main AES function"""

        # For efficiency reasons, the state between steps is transmitted via a
        # mutable array, not returned.
        self.add_round_key(block, 0)

        for round in range(1, self.rounds):
            self.sub_bytes(block, self.aes_sbox)
            self.shift_rows(block)
            self.mix_columns(block)
            self.add_round_key(block, round)

        self.sub_bytes(block, self.aes_sbox)
        self.shift_rows(block)
        # no mix_columns step in the last round
        self.add_round_key(block, self.rounds)

    def decrypt_block(self, block):
        """Decrypts a single block. This is the main AES decryption function"""

        # For efficiency reasons, the state between steps is transmitted via a
        # mutable array, not returned.
        self.add_round_key(block, self.rounds)

        # count rounds down from 15 ... 1
        for round in range(self.rounds - 1, 0, -1):
            self.shift_rows_inv(block)
            self.sub_bytes(block, self.aes_inv_sbox)
            self.add_round_key(block, round)
            self.mix_columns_inv(block)

        self.shift_rows_inv(block)
        self.sub_bytes(block, self.aes_inv_sbox)
        self.add_round_key(block, 0)
        # no mix_columns step in the last round

    def galois_multiply(self, a, b):
        """Galois Field multiplicaiton for AES"""
        p = 0
        while b:
            if b & 1:
                p ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x1b
            b >>= 1

        return p & 0xff

    def ecb(self, data, block_func):
        """Perform ECB mode with the given function"""

        if len(data) % self.block_size != 0:
            raise ValueError("Plaintext length must be multiple of 16")

        block_size = self.block_size
        data = array('B', data)

        for offset in range(0, len(data), block_size):
            block = data[offset: offset + block_size]
            block_func(block)
            data[offset: offset + block_size] = block

        return data.tostring()

    def cbcEncrypt(self, data):
        """Encrypt data in CBC mode"""

        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError("Plaintext length must be multiple of 16")

        data = array('B', data)
        IV = self.IV

        for offset in range(0, len(data), block_size):
            block = data[offset: offset + block_size]

            # Perform CBC chaining
            for i in range(block_size):
                block[i] ^= IV[i]

            self.encrypt_block(block)
            data[offset: offset + block_size] = block
            IV = block

        self.IV = IV
        return data.tostring()

    def cbcDecrypt(self, data):
        """Decrypt data in CBC mode"""

        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError("Ciphertext length must be multiple of 16")

        data = array('B', data)
        IV = self.IV

        for offset in range(0, len(data), block_size):
            ctext = data[offset: offset + block_size]
            block = ctext[:]
            self.decrypt_block(block)

            # Perform CBC chaining
            # for i in range(block_size):
            #    data[offset + i] ^= IV[i]
            for i in range(block_size):
                block[i] ^= IV[i]
            data[offset: offset + block_size] = block

            IV = ctext
            # data[offset : offset+block_size] = block

        self.IV = IV
        return data.tostring()

    def encrypt(self, data):
        """Encrypt data"""
        if self.modeEnc == MODE_ECB:
            return self.ecb(data, self.encrypt_block)
        elif self.modeEnc == MODE_CBC:
            return self.cbcEncrypt(data)

    def decrypt(self, data):
        """Decrypt data"""
        if self.modeEnc == MODE_ECB:
            return self.ecb(data, self.decrypt_block)
        elif self.modeEnc == MODE_CBC:
            return self.cbcDecrypt(data)


def pad(data_to_pad, block_size, style='pkcs7'):
    """Apply standard padding.

    Args:
      data_to_pad (byte string):
        The data that needs to be padded.
      block_size (integer):
        The block boundary to use for padding. The output length is guaranteed
        to be a multiple of :data:`block_size`.
      style (string):
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.

    Return:
      byte string : the original data with the appropriate padding added at the end.
    """
    def bchr(s):
        return bytes([s])

    padding_len = block_size - len(data_to_pad) % block_size
    if style == 'pkcs7':
        padding = bchr(padding_len) * padding_len
    elif style == 'x923':
        padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0) * (padding_len - 1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding


def unpad(padded_data, block_size, style='pkcs7'):
    """Remove standard padding.

    Args:
      padded_data (byte string):
        A piece of data with padding that needs to be stripped.
      block_size (integer):
        The block boundary to use for padding. The input length
        must be a multiple of :data:`block_size`.
      style (string):
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    Return:
        byte string : data without padding.
    Raises:
      ValueError: if the padding is incorrect.
    """
    def bchr(s):
        return bytes([s])

    pdata_len = len(padded_data)
    if pdata_len == 0:
        raise ValueError("Zero-length input cannot be unpadded")
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = padded_data[-1]
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1] != bchr(0) * (padding_len - 1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bchr(128))
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len > 1 and padded_data[1 - padding_len:] != bchr(0) * (padding_len - 1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]


class AES_CBC_Cipher:
    def __init__(self, key):
        password = key.encode('utf-8')
        self.key = password

    def encrypt(self, data):
        import os
        vector = os.urandom(16)
        encryption_cipher = AES(self.key, MODE_CBC, vector)
        return vector + encryption_cipher.encrypt(pad(data, 16))

    def decrypt(self, data):
        file_vector = data[:16]
        decryption_cipher = AES(self.key, MODE_CBC, file_vector)
        return unpad(decryption_cipher.decrypt(data[16:]), 16)
