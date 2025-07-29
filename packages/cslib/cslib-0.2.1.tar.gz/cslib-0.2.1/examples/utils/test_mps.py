import torch
import time

# 配置参数
matrix_size = 4096  # 增大矩阵尺寸以体现性能差异
num_iter = 100      # 迭代次数（预热+正式测试）
warmup = 10         # 预热次数（避免冷启动误差）

# 生成测试数据（统一在CPU生成，后续复制到不同设备）
x_cpu = torch.randn(matrix_size, matrix_size, dtype=torch.float32)
y_cpu = torch.randn(matrix_size, matrix_size, dtype=torch.float32)

# 定义计算任务（模拟神经网络中的常见操作）
def complex_operation(x, y):
    z = torch.mm(x, y)        # 矩阵乘法
    z = torch.relu(z)         # ReLU激活
    z = torch.sin(z)          # 正弦变换
    return z

# 测试CPU性能
def run_cpu():
    x = x_cpu.clone()
    y = y_cpu.clone()
    start_time = time.time()
    for _ in range(num_iter):
        _ = complex_operation(x, y)
    return (time.time() - start_time) / num_iter  # 单次迭代平均时间

# 测试MPS性能
def run_mps():
    device = torch.device("mps")
    x = x_cpu.clone().to(device)
    y = y_cpu.clone().to(device)
    
    # 预热（确保MPS设备初始化完成）
    for _ in range(warmup):
        _ = complex_operation(x, y)
    torch.mps.synchronize()  # 确保MPS操作完成
    
    # 正式测试
    start_time = time.time()
    for _ in range(num_iter):
        _ = complex_operation(x, y)
    torch.mps.synchronize()  # 同步计时
    return (time.time() - start_time) / num_iter

if __name__ == "__main__":
    if not torch.backends.mps.is_available():
        print("MPS不可用，请检查环境配置")
        exit()
        
    # 运行测试
    cpu_time = run_cpu()
    mps_time = run_mps()
    
    # 打印结果
    print(f"CPU 单次计算平均时间: {cpu_time:.6f} 秒")
    print(f"MPS 单次计算平均时间: {mps_time:.6f} 秒")
    print(f"加速比: {cpu_time/mps_time:.2f}x")
