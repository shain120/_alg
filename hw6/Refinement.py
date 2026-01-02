import math
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
        
def simulated_annealing(x_data, y_data, iterations=1000):
    w = random.uniform(-10, 10)
    b = random.uniform(-10, 10)
    current_loss = calculate_loss(w, b, x_data, y_data)
    
    temperature = 1000
    cooling_rate = 0.95  # 降溫係數
    
    for _ in range(iterations):
        # 隨機選一個鄰居
        next_w = w + random.uniform(-0.5, 0.5)
        next_b = b + random.uniform(-0.5, 0.5)
        next_loss = calculate_loss(next_w, next_b, x_data, y_data)
        
        delta_E = next_loss - current_loss
        
        # 決定是否接受
        accept = False
        if delta_E < 0:
            accept = True # 更好，一定接受
        else:
            # 更差，看運氣 (溫度越高，越容易接受壞結果)
            prob = math.exp(-delta_E / temperature)
            if random.random() < prob:
                accept = True
        
        if accept:
            w, b = next_w, next_b
            current_loss = next_loss
            
        # 降溫
        temperature *= cooling_rate
        
    return w, b