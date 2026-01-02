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

    # ---------- L7 Application ----------
    def L7(self, msg: str):
        return msg.encode()

    # ---------- L6 Presentation ----------
    def L6_encrypt(self, data: bytes):
        return self.cipher.encrypt(data)

    def L6_decrypt(self, data: bytes):
        
        try:
            return self.cipher.decrypt(data)
        except:
            return b"[Decryption Failed] " + data

    # ---------- L5 Session ----------
    def L5(self, data: bytes):
        return b"SESSION|" + data

    def L5_remove(self, data: bytes):
        # 安全移除 Header，找不到則回傳原始(損壞)資料
        parts = data.split(b"|", 1)
        return parts[1] if len(parts) > 1 else data

    # ---------- L4 Transport ----------
    def L4(self, data: bytes):
        return b"TCP|" + data

    def L4_remove(self, data: bytes):
        parts = data.split(b"|", 1)
        return parts[1] if len(parts) > 1 else data

    # ---------- L3 Network ----------
    def L3(self, data: bytes):
        return b"IP|" + data

    def L3_remove(self, data: bytes):
        parts = data.split(b"|", 1)
        return parts[1] if len(parts) > 1 else data

    # ---------- L2 Data Link ----------
    def L2(self, data: bytes):
        return b"MAC|" + data

    def L2_remove(self, data: bytes):
        parts = data.split(b"|", 1)
        return parts[1] if len(parts) > 1 else data

    # ---------- L1 Physical Layer (OFDM) ----------
    def L1_ofdm(self, data: bytes):
        # 1. Bytes -> Bits
        bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
        original_bit_len = len(bits)

        if len(bits) % 2 != 0:
            bits = np.append(bits, 0)

        # 2. Mapping
        tx_symbols = []
        for i in range(0, len(bits), 2):
            b0, b1 = bits[i], bits[i+1]
            tx_symbols.append(MAPPING_TABLE[(b0, b1)])
        tx_symbols = np.array(tx_symbols)

        # 3. IFFT
        tx_signal = np.fft.ifft(tx_symbols)

        # 4. Channel (Add Noise)
        noise_level = 0.01 
        noise = np.random.normal(0, noise_level, tx_signal.shape) + \
                1j * np.random.normal(0, noise_level, tx_signal.shape)
        rx_signal = tx_signal + noise

        # 5. FFT
        rx_symbols = np.fft.fft(rx_signal)

        # 6. Demapping
        rx_bits = []
        possible_symbols = list(MAPPING_TABLE.values())
        possible_bits = list(MAPPING_TABLE.keys())

        for sym in rx_symbols:
            distances = [abs(sym - ref) for ref in possible_symbols]
            min_idx = np.argmin(distances)
            b_tuple = possible_bits[min_idx]
            rx_bits.extend(b_tuple)

        rx_bits = np.array(rx_bits, dtype=np.uint8)
        rx_bits = rx_bits[:original_bit_len]

        rx_bytes = np.packbits(rx_bits).tobytes()

        return {
            "constellation": rx_symbols,
            "data": rx_bytes
        }
