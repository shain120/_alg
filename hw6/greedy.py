def gradient_descent(x_data, y_data, iterations=1000, lr=0.001):
    w = 0
    b = 0
    n = len(x_data)
    
    for _ in range(iterations):
        # 計算預測值
        y_pred = [w * x + b for x in x_data]
        
        # 計算梯度 (這裡省略了係數 2，常被併入 learning rate)
        w_grad = sum((y_p - y) * x for y_p, y, x in zip(y_pred, y_data, x_data)) * (2/n)
        b_grad = sum((y_p - y) for y_p, y in zip(y_pred, y_data)) * (2/n)
        
        # 貪婪更新：往梯度反方向走
        w = w - lr * w_grad
        b = b - lr * b_grad
        
    return w, b