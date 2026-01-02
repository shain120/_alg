import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 引入剛剛修改過、具有真實運算能力的 ofdm 模組
from ofdm import OSIStack, MAPPING_TABLE

class Demo:
    def __init__(self, root):
        self.root = root
        self.root.title("OSI 7-Layer + OFDM Physical Layer Simulation")
        self.root.geometry("1300x750")

        # 初始化 Alice 和 Bob
        # Alice 產生一個 key，Bob 使用相同的 key (模擬已交換密鑰)
        shared_stack = OSIStack()
        self.alice = shared_stack
        self.bob = OSIStack(shared_stack.key)

        # ============ OSI LABELS (最上方的分層標籤) ============
        osi_frame = ttk.Frame(root, padding=10)
        osi_frame.pack(fill="x")

        self.layers = [
            "L7 Application",
            "L6 Presentation",
            "L5 Session",
            "L4 Transport",
            "L3 Network",
            "L2 Data Link",
            "L1 Physical"
        ]

        self.osi_labels = []
        for i, l in enumerate(self.layers):
            lbl = tk.Label(
                osi_frame, text=l, width=18,
                relief="ridge", bg="lightgray", font=("Arial", 10, "bold")
            )
            lbl.grid(row=0, column=i, padx=3)
            self.osi_labels.append(lbl)

        # ============ PAYLOAD VIEW (顯示每一層的數據變化) ============
        payload_frame = ttk.Frame(root, padding=10)
        payload_frame.pack(fill="x")

        ttk.Label(payload_frame, text="Data Packet / Payload Inspection:").pack(anchor="w")

        self.payload_box = tk.Text(payload_frame, height=8, font=("Consolas", 10))
        self.payload_box.pack(fill="x")

        # ============ INPUT/OUTPUT (輸入訊息與接收結果) ============
        io = ttk.Frame(root, padding=10)
        io.pack(fill="x")

        # 輸入框
        tk.Label(io, text="Alice Sends:").grid(row=0, column=0)
        self.in_box = tk.Text(io, height=3, width=40)
        self.in_box.insert("end", "Hello Bob! OFDM is cool.")
        self.in_box.grid(row=0, column=1, padx=5)

        # 發送按鈕
        ttk.Button(io, text="Transmit ➡️", command=self.start).grid(row=0, column=2, padx=10)

        # 輸出框
        tk.Label(io, text="Bob Receives:").grid(row=0, column=3)
        self.out_box = tk.Text(io, height=3, width=40)
        self.out_box.grid(row=0, column=4, padx=5)

        # ============ FIGURE (圖表區域) ============
        fig_frame = ttk.Frame(root)
        fig_frame.pack(fill="both", expand=True, pady=10)

        # 建立兩個子圖：左邊畫 Sinc 波形，右邊畫星座圖
        self.fig, (self.ax_f, self.ax_c) = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, fig_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # 先畫一次空的背景格線
        self.init_plots()

    def init_plots(self):
        # 左圖：OFDM Sinc 示意
        self.ax_f.set_title("OFDM Orthogonal Subcarriers (Freq Domain)")
        self.ax_f.set_xlabel("Frequency")
        self.ax_f.grid(True)
        
        # 右圖：星座圖
        self.ax_c.set_title("QPSK Constellation (Rx Symbols)")
        self.ax_c.set_xlabel("In-Phase (I)")
        self.ax_c.set_ylabel("Quadrature (Q)")
        self.ax_c.grid(True)
        self.canvas.draw()

    # ================= Helpers =================
    def highlight(self, idx, color):
        """改變上方 OSI 標籤的顏色"""
        for l in self.osi_labels:
            l.config(bg="lightgray")
        self.osi_labels[idx].config(bg=color)

    def show_payload(self, label, data):
        """將每一層的數據顯示在中間的文字框"""
        # 如果是 bytes，顯示其 hex 或長度；如果是 str 直接顯示
        display_text = str(data)
        if isinstance(data, bytes):
            # 為了版面整潔，太長只顯示一部分
            if len(data) > 60:
                display_text = f"{data[:60]}... (len={len(data)})"
        
        self.payload_box.insert("end", f"[{label}] -> {display_text}\n")
        self.payload_box.see("end")

    # ================= Flow Logic =================
    def start(self):
        """開始傳輸流程"""
        self.payload_box.delete("1.0", "end")
        self.out_box.delete("1.0", "end")
        
        # 取得使用者輸入
        self.msg = self.in_box.get("1.0", "end").strip()
        if not self.msg: return

        self.step = 0
        self.root.after(500, self.send_step)

    def send_step(self):
        """Alice 的發送過程 (L7 -> L1)"""
        
        if self.step == 0:
            self.highlight(0, "lightgreen") # L7
            self.data = self.alice.L7(self.msg)
            self.show_payload("L7 (App)", self.data)

        elif self.step == 1:
            self.highlight(1, "lightgreen") # L6
            self.data = self.alice.L6_encrypt(self.data)
            self.show_payload("L6 (Encrypt)", self.data)

        elif self.step == 2:
            self.highlight(2, "lightgreen") # L5
            self.data = self.alice.L5(self.data)
            self.show_payload("L5 (Session)", self.data)

        elif self.step == 3:
            self.highlight(3, "lightgreen") # L4
            self.data = self.alice.L4(self.data)
            self.show_payload("L4 (TCP Header)", self.data)

        elif self.step == 4:
            self.highlight(4, "lightgreen") # L3
            self.data = self.alice.L3(self.data)
            self.show_payload("L3 (IP Header)", self.data)

        elif self.step == 5:
            self.highlight(5, "lightgreen") # L2
            self.data = self.alice.L2(self.data)
            self.show_payload("L2 (MAC Header)", self.data)

        elif self.step == 6:
            self.highlight(6, "lightgreen") # L1
            
            # === 關鍵修改：呼叫真實運算的 OFDM 模組 ===
            # result 包含 {"constellation": 複數陣列, "data": 解調後的 bytes}
            result = self.alice.L1_ofdm(self.data)
            
            # 1. 畫圖 (顯示接收到的含噪訊號)
            self.draw(result["constellation"])
            
            # 2. 傳遞數據 (模擬從物理層解出來的 Bits 轉回 Bytes)
            # 這一步確保 Bob 收到的是經過 IFFT/Channel/FFT 過程的資料
            self.data = result["data"]
            
            self.show_payload("L1 (OFDM Tx->Rx)", "Signal Transmitted & Demodulated")

        self.step += 1
        if self.step <= 6:
            self.root.after(600, self.send_step)
        else:
            # 傳送完畢，轉入接收階段
            self.step = 6
            self.root.after(600, self.recv_step)

    def recv_step(self):
        """Bob 的接收過程 (L1 -> L7)"""
        
        # 注意：如果雜訊太大導致資料損毀，split() 可能會報錯
        # 這裡加個簡單的 try-except 來處理傳輸失敗的情況
        try:
            if self.step == 6:
                self.highlight(6, "lightblue")
                # L1 已經在 send_step 的最後做完解調了，這裡只是視覺上的切換

            elif self.step == 5:
                self.highlight(5, "lightblue")
                self.data = self.bob.L2_remove(self.data)
                self.show_payload("L2 (Strip MAC)", self.data)

            elif self.step == 4:
                self.highlight(4, "lightblue")
                self.data = self.bob.L3_remove(self.data)
                self.show_payload("L3 (Strip IP)", self.data)

            elif self.step == 3:
                self.highlight(3, "lightblue")
                self.data = self.bob.L4_remove(self.data)
                self.show_payload("L4 (Strip TCP)", self.data)

            elif self.step == 2:
                self.highlight(2, "lightblue")
                self.data = self.bob.L5_remove(self.data)
                self.show_payload("L5 (Strip Session)", self.data)

            elif self.step == 1:
                self.highlight(1, "lightblue")
                self.data = self.bob.L6_decrypt(self.data)
                self.show_payload("L6 (Decrypt)", self.data)

            elif self.step == 0:
                self.highlight(0, "lightblue")
                final_msg = self.data.decode("utf-8", errors="ignore")
                self.out_box.insert("end", final_msg)
                self.show_payload("L7 (Received)", final_msg)
                return

            self.step -= 1
            self.root.after(600, self.recv_step)

        except Exception as e:
            self.payload_box.insert("end", f"\n[ERROR] Data Corrupted during transmission!\n{e}\n")
            print(f"Error at step {self.step}: {e}")

    # ================= Drawing Logic =================
    def draw(self, constellation):
        # 1. 繪製左圖 (Sinc 波形示意)
        self.ax_f.clear()
        f = np.linspace(-6, 6, 1000)
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
        for k in range(-2, 3):
            # 畫出互相正交的 Sinc 波
            y = np.sinc(f - k)
            self.ax_f.plot(f, y, color=colors[(k+2)%5], linewidth=1.5)
        
        self.ax_f.set_title("OFDM Orthogonal Subcarriers")
        self.ax_f.grid(True, alpha=0.5)

        # 2. 繪製右圖 (星座圖)
        self.ax_c.clear()
        
        # 畫出實際接收點 (藍色圓點，半透明)
        self.ax_c.scatter(np.real(constellation), np.imag(constellation), 
                          alpha=0.6, label="Rx Symbols")
        
        # 畫出理想標準點 (紅色 X)
        ideal_points = list(MAPPING_TABLE.values())
        self.ax_c.scatter(np.real(ideal_points), np.imag(ideal_points), 
                          color="red", marker="x", s=100, linewidth=2, label="Ideal QPSK")
        
        self.ax_c.set_title("QPSK Constellation")
        self.ax_c.set_xlim(-2, 2)
        self.ax_c.set_ylim(-2, 2)
        self.ax_c.axhline(0, color='black', linewidth=0.5)
        self.ax_c.axvline(0, color='black', linewidth=0.5)
        self.ax_c.set_aspect("equal")
        self.ax_c.grid(True)
        self.ax_c.legend(loc="upper right", fontsize="small")

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = Demo(root)
    root.mainloop()
