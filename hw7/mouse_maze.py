import numpy as np

def dfs(maze_list):
    maze = np.array(maze_list)
    visit_maze = np.zeros_like(maze,dtype=bool)
    visit_maze[start_pos[0],start_pos[1]] = True
    
    row, col = maze.shape
    move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    
    def solve(current_pos, path):
        r, c = current_pos
        visit_maze[r,c] = True
        
        if current_pos == end_pos:
            return path
        
        for x, y in move:
            n_r, n_c = r+x,c+y
            
            if 0 <=n_r < row and 0 <= n_c and \
            maze[n_r,n_c] == 0 and not visit_maze[n_r,n_c]:
                new_path = path + [(n_r,n_c)]
                result = solve((n_r,n_c),new_path)
                
                if result is not None:
                    return result
        return None
    return solve(start_pos,[start_pos])    

#---print---
def print_maze_solution(maze_list, path):
    """
    視覺化顯示迷宮和找到的路徑。
    """

    maze_viz = np.array(maze_list, dtype='<U1')
    
    # 轉換 1 為牆壁, 0 為空白
    maze_viz[maze_viz == '1'] = '█'
    maze_viz[maze_viz == '0'] = ' '
    
    # 標記路徑
    if path:
        for r, c in path:
            maze_viz[r, c] = '.' # 路徑
            
        # 標記起點和終點
        start_r, start_c = path[0]
        end_r, end_c = path[-1]
        maze_viz[start_r, start_c] = 'S' # 起點
        maze_viz[end_r, end_c] = 'E' # 終點


    for row in maze_viz:
        print(" ".join(row))
        
# ---maze---
maze_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
start_pos = (1, 1)
end_pos = (8, 8)

found_path = dfs(maze_data)
if found_path:
    print("成功找到路徑！\n")
    print_maze_solution(maze_data, found_path)
    print("\n路徑座標：")
    print(found_path)
else:
    print("找不到路徑。")
    print_maze_solution(maze_data, None)