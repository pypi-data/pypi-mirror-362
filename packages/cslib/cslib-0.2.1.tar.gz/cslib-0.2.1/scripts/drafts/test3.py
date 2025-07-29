import torch

# 假设我们有两个二维矩阵 A 和 B
# A 的维度是 [m, n]
# B 的维度是 [n, p]
# m, n, p 分别是矩阵的行数和列数

# 创建两个二维张量
A = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
B = torch.tensor([[2, 0], [1, 3]], dtype=torch.float32)

# 方法1: 使用 torch.mm() 函数进行矩阵乘法
C_mm = torch.mm(A, B)

# 方法2: 使用 @ 操作符进行矩阵乘法
C_at = A @ B

# 输出结果
print("使用 torch.mm() 函数的结果:")
print(C_mm)
print("使用 @ 操作符的结果:")
print(C_at)
