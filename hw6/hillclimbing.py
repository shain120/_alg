import random
def calculate_loss(w, b, x_data, y_data):
    """
    計算均方誤差 (MSE)
    Loss = (1/n) * Σ(y_true - y_pred)^2
    """
    total_error = 0
    n = len(x_data)
    
    for x, y in zip(x_data, y_data):
        prediction = w * x + b
        total_error += (y - prediction) ** 2
        
def hill_climbing(x_data, y_data, iterations=1000):
    # 1. 隨機初始化
    w = random.uniform(-10, 10)
    b = random.uniform(-10, 10)
    current_loss = calculate_loss(w, b, x_data, y_data)
    step_size = 0.01

    for _ in range(iterations):
        # 2. 生成鄰居 (嘗試上下左右移動)
        candidates = [
            (w + step_size, b), (w - step_size, b),
            (w, b + step_size), (w, b - step_size)
        ]
        
        best_neighbor = None
        best_neighbor_loss = current_loss

        # 3. 找最好的鄰居
        for (nw, nb) in candidates:
            loss = calculate_loss(nw, nb, x_data, y_data)
            if loss < best_neighbor_loss:
                best_neighbor_loss = loss
                best_neighbor = (nw, nb)

        # 4. 如果鄰居更好，就移動；否則停止 (或繼續嘗試)
        if best_neighbor:
            w, b = best_neighbor
            current_loss = best_neighbor_loss
        else:
            # 在純爬山法中，找不到更好的就代表到了局部最佳解
            break 
            
    return w, b