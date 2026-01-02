import numpy as np
import matplotlib.pyplot as plt

def generate_newton_fractal(res=800, max_iter=50, tolerance=1e-4, x_range=(-1.5, 1.5), y_range=(-1.5, 1.5)):
    """
    生成 z^3 - 1 = 0 的牛頓碎形圖像。

    參數:
    res (int): 圖像解析度 (res x res)。越高越清晰但計算越久。
    max_iter (int): 最大迭代次數。
    tolerance (float): 收斂容忍度，當變化小於此值視為收斂。
    x_range, y_range (tuple): 複數平面的觀察範圍。
    """
    
    # --- 1. 建立複數平面網格 ---
    # 在指定範圍內生成均勻分布的點
    x = np.linspace(x_range[0], x_range[1], res)
    y = np.linspace(y_range[0], y_range[1], res)
    # 建立網格座標
    X, Y = np.meshgrid(x, y)
    # 將 X 和 Y 結合成複數平面 Z (這些是我們的初始猜測值 z0)
    Z = X + 1j * Y

    # 用來記錄每個點「是否尚未收斂」的遮罩 (True 代表還在跑)
    not_converged_mask = np.full(Z.shape, True, dtype=bool)
    # 用來記錄每個點花了幾次迭代才收斂的陣列
    iterations_count = np.zeros(Z.shape, dtype=int)

    # --- 2. 定義方程及其導數 ---
    # f(z) = z^3 - 1
    # f'(z) = 3*z^2
    
    print(f"開始計算 {res}x{res} 的網格，最大迭代 {max_iter} 次...")

    # --- 3. 開始迭代循環 ---
    for i in range(max_iter):
        # 為了避免除以零的錯誤，我們先把目前為 0 的點稍微移開一點點 (極罕見情況)
        Z[Z == 0] = 1e-8 + 1e-8j

        # --- 核心：牛頓迭代公式 ---
        # z_new = z - f(z) / f'(z)
        # 我們只對「尚未收斂」的點進行更新，節省計算資源
        Z_prev = Z[not_converged_mask] # 記錄舊值以便比較
        Z[not_converged_mask] = Z[not_converged_mask] - (Z[not_converged_mask]**3 - 1) / (3 * Z[not_converged_mask]**2)
        
        # --- 4. 檢查收斂 ---
        # 計算新舊值之間的距離 (變化量)
        diff = np.abs(Z[not_converged_mask] - Z_prev)
        
        # 找出這一輪中，哪些點的變化量已經小於容忍度了
        just_converged = diff < tolerance
        
        # 更新迭代計數：
        # 對於那些「在這一輪剛收斂」的點，記錄下當前的迭代次數 i
        # 我們需要透過遮罩映射回去，這步稍微複雜一點
        current_indices = np.where(not_converged_mask) # 找出目前還在跑的點的索引
        # 在這些點中，找出剛收斂的
        converged_indices = (current_indices[0][just_converged], current_indices[1][just_converged])
        iterations_count[converged_indices] = i
        
        # 更新遮罩：將這一輪剛收斂的點標記為 False (之後不再計算)
        not_converged_mask[converged_indices] = False
        
        # 如果所有點都收斂了，提早結束
        if not np.any(not_converged_mask):
            print(f"所有點在第 {i} 次迭代前收斂完畢。")
            break

    print("計算完成，開始著色...")

    # --- 5. 著色策略 ---
    # 我們需要根據最終 Z 收斂到哪一個根來決定顏色。
    # z^3 - 1 的三個根大約是：
    roots = np.array([1, -0.5 + 0.866j, -0.5 - 0.866j])
    
    # 建立一個用來存放顏色索引的陣列
    colors = np.zeros(Z.shape, dtype=int)

    # 對每個根，找出最終 Z 值離它最近的點
    for r_idx, root in enumerate(roots):
        # 計算最終 Z 平面與這個根的距離
        dist = np.abs(Z - root)
        # 如果距離很小（例如小於 0.1），我們就認為它收斂到了這個根
        # 將這些位置標記為該根的索引 (0, 1, 或 2)
        colors[dist < 0.1] = r_idx

    # --- 6. 視覺化 ---
    plt.figure(figsize=(10, 10))
    
    # 這裡我們使用一個小技巧來結合「收斂根」與「迭代次數」：
    # 利用 HSV 色彩空間的概念。
    # 基底顏色由 `colors` (收斂到哪個根) 決定。
    # 亮度/對比度由 `iterations_count` (收斂速度) 決定。
    
    # 將迭代次數標準化到 0~1 之間，並反轉 (迭代越少越亮/平坦，越多越暗/邊界)
    shade = 1 - (iterations_count / max_iter)
    # 增加一點對比度
    shade = shade**4 

    # 這裡使用 matplotlib 的 'hsv' colormap 是一個簡化的方式。
    # 我們將根的索引 (0,1,2) 除以 3，映射到色彩環上，再乘上亮度陰影。
    # 這是一個快速產生藝術效果的方法，你可以嘗試不同的組合。
    final_img_data = (colors / 3.0) * shade
    
    plt.imshow(final_img_data, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], cmap='twilight_shifted', origin='lower')
    
    plt.title(f"Newton Fractal for $z^3 - 1 = 0$")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.colorbar(label="Root Convergence & Iteration Speed Mix")
    plt.show()

# 執行函數
# 建議解析度設為 800 或 1000 以獲得較好的細節
generate_newton_fractal(res=800, max_iter=40)