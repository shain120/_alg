import numpy as np
import matplotlib.pyplot as plt

def softmax(z):
    e_z = np.exp(z - np.max(z)) # 減去 max 防止溢位
    return e_z / np.sum(e_z)

def cross_entropy(p, q):
    # 加入極小值 eps 防止 log(0)
    return -np.sum(p * np.log(q + 1e-12))

def entropy(p):
    return -np.sum(p * np.log(p + 1e-12))

# 1. 設定目標分佈 p (固定)
p = np.array([0.5, 0.25, 0.25])

# 2. 設定初始猜測 q 的 logits (變數)
# 初始 q 為 [1/3, 1/3, 1/3]，對應的 logits 可以是 [0, 0, 0]
z = np.array([0.0, 0.0, 0.0]) 

# 參數設定
learning_rate = 0.1
iterations = 200
history = []

print(f"Target p: {p}")
print(f"Target Entropy (Min Possbile Loss): {entropy(p):.6f}")
print("-" * 30)

# 3. 梯度下降迴圈
for i in range(iterations):
    # Forward: 計算當前的 q
    q = softmax(z)
    
    # Calculate Loss (Cross Entropy)
    loss = cross_entropy(p, q)
    history.append(loss)
    
    # Backward: 計算梯度
    # d(CrossEntropy) / d(z) = q - p  <-- 這是關鍵公式
    gradient = q - p
    
    # Update: 更新 logits
    z = z - learning_rate * gradient
    
    if i % 20 == 0:
        print(f"Iter {i:3d} | Loss: {loss:.6f} | q: {np.round(q, 4)}")

print("-" * 30)
final_q = softmax(z)
print(f"Final q : {np.round(final_q, 4)}")
print(f"Target p: {p}")

# 驗證結果
error = np.sum((final_q - p)**2)
if error < 1e-5:
    print("\n✅ 驗證成功！Cross Entropy 最低點發生在 q = p")
else:
    print("\n❌ 尚未收斂")