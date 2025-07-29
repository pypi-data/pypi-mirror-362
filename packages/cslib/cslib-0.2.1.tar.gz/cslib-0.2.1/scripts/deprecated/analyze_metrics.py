import sqlite3
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import os

def plot_metrics(result_matrix, algorithms, metrics, output_dir="plots"):
    """
    为每个指标绘制不同算法的曲线图。
    :param result_matrix: 二维矩阵，每行代表一个算法，每列代表一个指标的平均值。
    :param algorithms: 算法名称列表。
    :param metrics: 指标名称列表。
    :param output_dir: 保存图像的目录。
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历每个指标
    for j, metric in enumerate(metrics):
        # 获取当前指标的所有算法的值
        values = result_matrix[:, j]

        # 绘图
        plt.figure(figsize=(10, 6))
        plt.plot(algorithms, values, marker='o', linestyle='-', linewidth=2, markersize=8)
        plt.title(f"Comparison of Algorithms for Metric: {metric}")
        plt.xlabel("Algorithms")
        plt.ylabel(metric)
        plt.xticks(rotation=45)  # 旋转 x 轴标签以便更好地显示
        plt.grid(True, linestyle='--', alpha=0.7)

        # 保存图像
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{metric}.png"))
        plt.close()

    print(f"All plots have been saved to {output_dir}")

def analyze_metrics(db_path):
    """
    从数据库中读取融合算法的指标，并计算每种算法在每个指标上的平均值。
    :param db_path: 数据库文件的路径
    :return: 二维矩阵，其中每一行代表一个算法，每一列代表一个指标的平均值。
    """
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询所有算法和指标
    cursor.execute("SELECT DISTINCT method FROM fusion_metrics")
    algorithms = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM fusion_metrics")
    metrics = [row[0] for row in cursor.fetchall()]

    # 初始化结果矩阵
    result_matrix = np.zeros((len(algorithms), len(metrics)))

    # 遍历每种算法和每个指标，计算平均值
    for i, algorithm in enumerate(algorithms):
        for j, metric in enumerate(metrics):
            cursor.execute('''
            SELECT AVG(value) FROM fusion_metrics WHERE method=? AND name=?
            ''', (algorithm, metric))
            avg_value = cursor.fetchone()[0]
            result_matrix[i, j] = avg_value if avg_value is not None else 0  # 如果没有数据，则用 0 填充

    conn.close()

    return result_matrix, algorithms, metrics

# 示例用法
if __name__ == "__main__":
    root_dir = "/Volumes/Charles/data/vision/torchvision/tno/tno/fused"  # 替换为你的数据集根目录
    db_name = "metrics.db"  # 数据库文件名
    db_path = Path(root_dir, db_name)

    # 分析指标
    result_matrix, algorithms, metrics = analyze_metrics(db_path)

    # 打印结果
    print("Algorithms:", algorithms)
    print("Metrics:", metrics)
    print("Result Matrix:\n", result_matrix)

    # 画图
    plot_metrics(result_matrix, algorithms, metrics, output_dir="/Volumes/Charles/data/vision/torchvision/tno/tno/fused")