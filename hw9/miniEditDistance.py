def min_edit_distance(word1, word2):
    """
    計算兩個字串之間的最小編輯距離 (Levenshtein Distance)。
    操作包括：插入 (Insert)、刪除 (Delete)、替換 (Replace)。
    """
    m = len(word1)
    n = len(word2)

    # 建立一個 (m+1) x (n+1) 的二維表格
    # dp[i][j] 代表 word1 的前 i 個字元轉換成 word2 的前 j 個字元所需的最少步數
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 1. 初始化邊界條件 (Base Cases)
    # 如果 word2 為空，word1 需要刪除 i 個字元才能變成 word2
    for i in range(m + 1):
        dp[i][0] = i
    
    # 如果 word1 為空，word1 需要插入 j 個字元才能變成 word2
    for j in range(n + 1):
        dp[0][j] = j

    # 2. 填滿 DP 表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 情況 A: 字元相同，不需要操作
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            # 情況 B: 字元不同，取三種操作中的最小值 + 1
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # 刪除 (Delete)
                    dp[i][j - 1],    # 插入 (Insert)
                    dp[i - 1][j - 1] # 替換 (Replace)
                )

    # 回傳表格右下角的值，即為最終答案
    return dp[m][n]

# --- 測試範例 ---
if __name__ == "__main__":
    s1 = "horse"
    s2 = "ros"
    
    dist = min_edit_distance(s1, s2)
    print(f"'{s1}' 轉換成 '{s2}' 的最小編輯距離為: {dist}")
    
    # 經典範例 2
    print(f"'intention' -> 'execution': {min_edit_distance('intention', 'execution')}")