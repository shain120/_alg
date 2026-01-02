import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ofdm import OSIStack, MAPPING_TABLE


class Demo:
    def __init__(self, root):
        self.root = root
        self.root.title("OSI 7-Layer Secure Transmission (Correct Model)")
        self.root.geometry("1300x750")

        shared = OSIStack()
        self.alice = shared
        self.bob = OSIStack(shared.key)

        # ============ OSI LABELS ============
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
                relief="ridge", bg="lightgray"
            )
            lbl.grid(row=0, column=i, padx=3)
            self.osi_labels.append(lbl)

        # ============ PAYLOAD VIEW ============
        payload_frame = ttk.Frame(root, padding=10)
        payload_frame.pack(fill="x")

        ttk.Label(payload_frame, text="Payload at each layer").pack(anchor="w")

        self.payload_box = tk.Text(payload_frame, height=6)
        self.payload_box.pack(fill="x")

        # ============ INPUT ============
        io = ttk.Frame(root, padding=10)
        io.pack(fill="x")

        self.in_box = tk.Text(io, height=3, width=40)
        self.in_box.insert("end", "Hello Bob!")
        self.in_box.grid(row=0, column=0)

        ttk.Button(io, text="Send", command=self.start).grid(row=0, column=1, padx=10)

        self.out_box = tk.Text(io, height=3, width=40)
        self.out_box.grid(row=0, column=2)

        # ============ FIGURE ============
        fig_frame = ttk.Frame(root)
        fig_frame.pack(fill="both", expand=True)

        self.fig, (self.ax_f, self.ax_c) = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, fig_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ================= Helpers =================
    def highlight(self, idx, color):
        for l in self.osi_labels:
            l.config(bg="lightgray")
        self.osi_labels[idx].config(bg=color)

    def show_payload(self, label, data):
        self.payload_box.insert("end", f"{label}: {data[:80]}\n")
        self.payload_box.see("end")

    # ================= Flow =================
    def start(self):
        self.payload_box.delete("1.0", "end")
        self.out_box.delete("1.0", "end")
        self.msg = self.in_box.get("1.0", "end").strip()
        self.step = 0
        self.root.after(500, self.send_step)

    def send_step(self):
        if self.step == 0:
            self.highlight(0, "lightgreen")
            self.data = self.alice.L7(self.msg)
            self.show_payload("L7", self.data)

        elif self.step == 1:
            self.highlight(1, "lightgreen")
            self.data = self.alice.L6_encrypt(self.data)
            self.show_payload("L6 (Encrypted)", self.data)

        elif self.step == 2:
            self.highlight(2, "lightgreen")
            self.data = self.alice.L5(self.data)
            self.show_payload("L5", self.data)

        elif self.step == 3:
            self.highlight(3, "lightgreen")
            self.data = self.alice.L4(self.data)
            self.show_payload("L4", self.data)

        elif self.step == 4:
            self.highlight(4, "lightgreen")
            self.data = self.alice.L3(self.data)
            self.show_payload("L3", self.data)

        elif self.step == 5:
            self.highlight(5, "lightgreen")
            self.data = self.alice.L2(self.data)
            self.show_payload("L2", self.data)

        elif self.step == 6:
            self.highlight(6, "lightgreen")
            self.phy = self.alice.L1_ofdm(self.data)
            self.draw(self.phy["constellation"])

        self.step += 1
        if self.step <= 6:
            self.root.after(500, self.send_step)
        else:
            self.step = 6
            self.root.after(500, self.recv_step)

    def recv_step(self):
        if self.step == 6:
            self.highlight(6, "lightblue")

        elif self.step == 5:
            self.highlight(5, "lightblue")
            self.data = self.bob.L2_remove(self.data)

        elif self.step == 4:
            self.highlight(4, "lightblue")
            self.data = self.bob.L3_remove(self.data)

        elif self.step == 3:
            self.highlight(3, "lightblue")
            self.data = self.bob.L4_remove(self.data)

        elif self.step == 2:
            self.highlight(2, "lightblue")
            self.data = self.bob.L5_remove(self.data)

        elif self.step == 1:
            self.highlight(1, "lightblue")
            self.data = self.bob.L6_decrypt(self.data)

        elif self.step == 0:
            self.highlight(0, "lightblue")
            self.out_box.insert("end", self.data.decode())
            return

        self.step -= 1
        self.root.after(500, self.recv_step)

    # ================= Drawing =================
    def draw(self, constellation):
        self.ax_f.clear()
        f = np.linspace(-10, 10, 4000)
        for k in range(-3, 4):
            self.ax_f.plot(f, np.sinc(f - k))
        self.ax_f.set_title("OFDM Orthogonal Subcarriers")
        self.ax_f.grid(True)

        self.ax_c.clear()
        self.ax_c.scatter(np.real(constellation), np.imag(constellation), alpha=0.5)
        ideal = list(MAPPING_TABLE.values())
        self.ax_c.scatter(np.real(ideal), np.imag(ideal), color="red", marker="x")
        self.ax_c.set_title("QPSK Constellation")
        self.ax_c.set_aspect("equal")
        self.ax_c.grid(True)

        self.canvas.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    Demo(root)
    root.mainloop()
