import numpy as np
from cryptography.fernet import Fernet

# QPSK mapping
MAPPING_TABLE = {
    (0, 0): 1 + 1j,
    (0, 1): -1 + 1j,
    (1, 1): -1 - 1j,
    (1, 0): 1 - 1j
}

class OSIStack:
    def __init__(self, key=None):
        self.key = key if key else Fernet.generate_key()
        self.cipher = Fernet(self.key)

    # ---------- L7 ----------
    def L7(self, msg: str):
        return msg.encode()

    # ---------- L6 ----------
    def L6_encrypt(self, data: bytes):
        return self.cipher.encrypt(data)

    def L6_decrypt(self, data: bytes):
        return self.cipher.decrypt(data)

    # ---------- L5 ----------
    def L5(self, data: bytes):
        return b"SESSION|" + data

    def L5_remove(self, data: bytes):
        return data.split(b"|", 1)[1]

    # ---------- L4 ----------
    def L4(self, data: bytes):
        return b"TCP|" + data

    def L4_remove(self, data: bytes):
        return data.split(b"|", 1)[1]

    # ---------- L3 ----------
    def L3(self, data: bytes):
        return b"IP|" + data

    def L3_remove(self, data: bytes):
        return data.split(b"|", 1)[1]

    # ---------- L2 ----------
    def L2(self, data: bytes):
        return b"MAC|" + data

    def L2_remove(self, data: bytes):
        return data.split(b"|", 1)[1]

    # ---------- L1 ----------
    def L1_ofdm(self, data: bytes):
        bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
        if len(bits) % 2:
            bits = np.append(bits, 0)

        symbols = []
        for i in range(0, len(bits), 2):
            symbols.append(MAPPING_TABLE[(bits[i], bits[i+1])])
        symbols = np.array(symbols)

        N = 64
        blocks = []
        for i in range(0, len(symbols), N):
            blk = symbols[i:i+N]
            if len(blk) < N:
                blk = np.pad(blk, (0, N-len(blk)))
            blocks.append(np.fft.ifft(blk))

        return {
            "bits": bits,
            "constellation": symbols,
            "tx": np.concatenate(blocks)
        }
