[ai chat](https://gemini.google.com/share/d5188a4f14d0)
# 習題 9：最小編輯距離 (Minimum Edit Distance) 與 動態規劃

![img](https://github.com/shain120/_alg/blob/main/hw9/Screenshot_3.png)

---

## 1. 問題定義

**最小編輯距離**是指將一個字串 (`word1`) 轉換成另一個字串 (`word2`) 所需的最少操作次數。允許的操作有三種：
1.  **插入 (Insert)**
2.  **刪除 (Delete)**
3.  **替換 (Replace)**

### 範例
* `horse` -> `ros`
* 距離為 **3**：
    1.  `h` -> `r` (替換)
    2.  `o` -> `o` (不變)
    3.  `r` -> `s` (替換)
    4.  `s` -> (刪除)
    5.  `e` -> (刪除)
    *(註：實際路徑可能不同，但最少步數皆為 3)*

---

## 2. 解題邏輯：動態規劃 (Dynamic Programming)

此問題符合 DP 的兩個特性：**最佳子結構**與**重疊子問題**。我們使用一個二維表格 `dp` 來記錄運算結果。

### 2.1 狀態定義 (State)
定義 `dp[i][j]` 為：
> 將 `word1` 的前 `i` 個字元，轉換成 `word2` 的前 `j` 個字元，所需的**最小編輯距離**。

### 2.2 狀態轉移方程式 (Transition Equation)

對於 `word1[i]` 和 `word2[j]`：

1.  **若字元相同 (`word1[i-1] == word2[j-1]`)**：
    不需要額外操作，距離等於左上角的值。
    $$dp[i][j] = dp[i-1][j-1]$$

2.  **若字元不同**：
    取三種操作中代價最小者，並加 1 (本次操作成本)。
    $$dp[i][j] = 1 + \min \begin{cases} dp[i-1][j] & \text{(刪除操作)} \\ dp[i][j-1] & \text{(插入操作)} \\ dp[i-1][j-1] & \text{(替換操作)} \end{cases}$$

### 2.3 邊界條件 (Base Case)
* 若 `word2` 為空字串，`word1` 需刪除所有字元：`dp[i][0] = i`
* 若 `word1` 為空字串，`word1` 需插入所有字元：`dp[0][j] = j`

---

## 3. Python 程式碼實作

```python
def min_edit_distance(word1, word2):
    """
    計算兩個字串之間的 Levenshtein Distance。
    使用 Bottom-Up 動態規劃方法。
    """
    m = len(word1)
    n = len(word2)

    # 1. 建立 DP 表格，大小為 (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 2. 初始化邊界條件
    # word1 變為空字串 (刪除)
    for i in range(m + 1):
        dp[i][0] = i
    
    # 空字串變為 word2 (插入)
    for j in range(n + 1):
        dp[0][j] = j

    # 3. 填滿表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 情況 A: 字元相同
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            # 情況 B: 字元不同
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # 刪除 (Delete)
                    dp[i][j - 1],    # 插入 (Insert)
                    dp[i - 1][j - 1] # 替換 (Replace)
                )

    # 回傳右下角的值 (最終答案)
    return dp[m][n]

# --- 測試區塊 ---
if __name__ == "__main__":
    s1 = "intention"
    s2 = "execution"
    dist = min_edit_distance(s1, s2)
    print(f"'{s1}' -> '{s2}' 的最小編輯距離: {dist}")
