# OFDM 模擬圖表詳細解析

本文件旨在解釋 OFDM (Orthogonal Frequency Division Multiplexing) 模擬程式中產生的兩張核心圖表。這兩張圖分別展示了訊號在**頻域 (Frequency Domain)** 的物理特性與**複數平面 (Complex Plane)** 上的數據調變狀態。

---
<img width="1088" height="449" alt="image" src="https://github.com/user-attachments/assets/af51b723-765d-4c3d-b96f-79b87f402046" />
# OFDM 核心運算原理說明

本文件解析 `ofdm.py` 中 `L1_ofdm` 函式的三個關鍵步驟。這展示了如何利用數位訊號處理 (DSP) 將資料透過無線信道傳輸。

核心流程：**頻域符號 (Tx)** $\xrightarrow{IFFT}$ **時域波形 (Channel)** $\xrightarrow{FFT}$ **頻域符號 (Rx)**
# OFDM 發送與接收流程說明（IFFT / FFT）

本文件說明以下三個步驟在 **OFDM（Orthogonal Frequency Division Multiplexing）** 系統中的意義與數學背景：

```python
Tx (發送)：
 time_signal = np.fft.ifft(qpsk_symbols)   # 使用公式 (2)

Channel（通道）：
 received_signal = time_signal + noise

Rx (接收)：
 recovered_symbols = np.fft.fft(received_signal)  # 使用公式 (4)
```

---

## 一、Tx（發送端）：IFFT 產生時域 OFDM 訊號

### 1. 輸入：`qpsk_symbols`

* `qpsk_symbols` 為**頻域資料**
* 每一個元素代表一個 **子載波（Subcarrier）** 上的 QPSK 符號
* 形式如下：

[
X[k], \quad k = 0, 1, 2, \dots, N-1
]

其中：

* (N)：子載波數量（FFT size）
* (X[k])：第 (k) 個子載波上的複數調變符號

---

### 2. IFFT（公式 2）：頻域 → 時域

```python
time_signal = np.fft.ifft(qpsk_symbols)
```

對應的數學公式為：

[
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] e^{j2\pi kn/N}, \quad n = 0, 1, \dots, N-1
]

#### 意義說明：

* 將 **N 個子載波** 疊加成一個時域 OFDM 符號
* 每一個子載波彼此正交（Orthogonal）
* `time_signal` 是實際「送到空中 / 線路上」的訊號

📌 **重點概念**：

> IFFT = 把「很多頻率的資料」合成「一段時間的波形」

---

## 二、Channel（通道）：加入雜訊

```python
received_signal = time_signal + noise
```

### 1. 通道模型（簡化）

此處使用最基本的 **AWGN（Additive White Gaussian Noise）** 模型：

[
y[n] = x[n] + w[n]
]

其中：

* (x[n])：發送端 OFDM 時域訊號
* (w[n])：高斯白雜訊
* (y[n])：接收端接收到的時域訊號

---

### 2. 為何加雜訊？

* 模擬實際無線/有線通道
* 測試系統對雜訊的抗干擾能力
* SNR 越低，錯誤率越高

---

## 三、Rx（接收端）：FFT 還原頻域符號

### 1. FFT（公式 4）：時域 → 頻域

```python
recovered_symbols = np.fft.fft(received_signal)
```

對應的數學公式為：

[
Y[k] = \sum_{n=0}^{N-1} y[n] e^{-j2\pi kn/N}, \quad k = 0, 1, \dots, N-1
]

---

### 2. 意義說明

* 將接收到的時域 OFDM 波形拆回各個子載波
* 每一個 (Y[k]) 對應原本的 (X[k])
* 若雜訊不大：

[
Y[k] \approx X[k]
]

之後即可進行：

* QPSK 解調
* 判斷 bit 0 / 1

📌 **重點概念**：

> FFT = 把「一段時間的混合波形」拆回「各個頻率的資料」

---

## 四、整體流程總結

```text
Bits
 ↓ QPSK 調變
Frequency-domain symbols (X[k])
 ↓ IFFT
Time-domain OFDM signal (x[n])
 ↓ Channel + Noise
Received signal (y[n])
 ↓ FFT
Recovered symbols (Y[k])
 ↓ QPSK 解調
Bits
```

---

## 五、補充說明（實務系統）

實際 OFDM 系統通常還會包含：

* Cyclic Prefix (CP)
* 通道衰減與等化（Channel Estimation / Equalization）
* 多徑效應
* 同步（Timing / Frequency Offset）

本範例為 **最簡化 OFDM 架構**，用於理解 FFT / IFFT 的核心角色。

---

📘 **一句話總結**：

> OFDM 的精髓在於：
> **Tx 用 IFFT 合成多子載波，Rx 用 FFT 再把它們分離回來。**

---

## 1. 發送端 (Tx): 調變
**程式碼：**
```python
time_signal = np.fft.ifft(qpsk_symbols)
## 圖表一：OFDM Orthogonal Subcarriers (正交子載波)

這張圖（左側圖表）展示了 OFDM 訊號在**頻率域**上的樣子。這是理解 OFDM 如何節省頻寬並避免干擾的關鍵。

### 1. 視覺特徵
* **多色波形**：每一種顏色的波形代表一個獨立的**子載波 (Subcarrier)**。
* **波形形狀**：這些是 **Sinc 函數** ($sinc(x) = \frac{\sin(x)}{x}$)。
    * **原理**：在數位通訊中，時域上的訊號通常是矩形脈衝 (Rectangular Window)。根據傅立葉變換原理，時域的矩形對應到頻域就是 Sinc 波形。

### 2. 核心概念：正交性 (Orthogonality)
這張圖最重要的地方在於它展示了「正交」的數學定義。請觀察圖中的波峰與零點：

* **峰值對齊零點**：
    * 當**藍色波形**達到最高能量點（Peak，也就是我們讀取該載波數據的時刻）時...
    * **所有其他顏色的波形**（橘色、綠色、紅色...）剛好都穿越 **0 (Zero Crossing)**。
* **物理意義**：
    * 這意味著在採樣點上，各個子載波之間**完全沒有互相干擾 (No Inter-Carrier Interference, ICI)**。
    * 即使這些波形在頻譜上看起來緊密重疊，我們仍然可以完美地將它們分離出來。

### 3. 優勢
* **頻譜效率極高**：傳統通訊需要在頻道之間留「保護帶 (Guard Band)」來防止重疊，但 OFDM 允許波形重疊（只要保持正交），因此能在有限的頻寬內塞入更多數據。

---

## 圖表二：QPSK Constellation (星座圖)

這張圖（右側圖表）展示了數據在**複數平面 (Complex Plane)** 上的狀態。它告訴我們「傳送了什麼資訊」以及「訊號品質如何」。

### 1. 座標軸意義
* **X 軸 (Real / In-Phase)**：實部，也稱為 I 路。
* **Y 軸 (Imaginary / Quadrature)**：虛部，也稱為 Q 路。
* 每一個點都代表一個複數符號 $S = I + jQ$。

### 2. 調變模式：QPSK (Quadrature Phase Shift Keying)
圖中有 4 個聚落，代表使用 QPSK 調變：
* **4 個相位點**：系統將數據映射到四個象限中 (例如：$45^\circ, 135^\circ, 225^\circ, 315^\circ$)。
* **攜帶資訊**：每個符號攜帶 **2 bits** 資訊。
    * 例如（依據映射表）：
        * `00` $\rightarrow$ 第一象限 $(1, 1)$
        * `01` $\rightarrow$ 第二象限 $(-1, 1)$
        * `10` $\rightarrow$ 第三象限 $(-1, -1)$
        * `11` $\rightarrow$ 第四象限 $(1, -1)$

### 3. 紅色 X vs. 藍色圓點
* **紅色 X (Reference/Tx)**：
    * 這是**發送端**原本想要傳送的理想位置（標準答案）。
* **藍色圓點 (Received/Rx)**：
    * 這是**接收端**實際解調出來的訊號點。
    * 藍點沒有完全重疊在紅叉上，而是散落在周圍，這是因為經過了**雜訊 (Noise)** 的干擾。

### 4. 訊號品質解讀
* **集中**：如果藍點緊緊包圍紅叉，代表雜訊低 (高信噪比 SNR)，通訊品質好。
* **發散**：如果藍點散得很開，甚至跨越了座標軸跑到別的象限，就會發生**位元錯誤 (Bit Error)**。
* **本圖結論**：圖中的藍點非常集中，代表模擬環境中的雜訊極低，解碼準確率應為 100%。

---

## 總結：兩圖的關係

| 特性 | 左圖 (Subcarriers) | 右圖 (Constellation) |
| :--- | :--- | :--- |
| **領域** | **頻率域 (Frequency Domain)** | **複數/調變域 (Modulation Domain)** |
| **關注點** | 訊號如何**傳輸**與物理排列 | 數據如何**編碼**與解碼 |
| **關鍵字** | Sinc 波形、正交性、IFFT | QPSK、I/Q 通道、雜訊 (Noise) |
| **對應程式碼** | `draw()` 中的 `np.sinc()` 繪圖 | `L1_ofdm` 中的 `mapping` 與 `noise` |
