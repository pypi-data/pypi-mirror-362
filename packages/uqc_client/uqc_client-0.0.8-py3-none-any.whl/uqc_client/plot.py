import numpy as np
import matplotlib.pyplot as plt


def plot_hist(data):
    """
    输入两列数据，绘制量子态概率分布直方图
    - x轴标签自动转换为二进制字符串（位数由最大索引决定）
    - 示例：索引3 → 二进制"11"（2量子比特系统）

    Parameters
    ----------
    data : 二维数组或列表，格式为 [[索引1, 值1], [索引2, 值2], ...]

    Returns
    -------
    None

    """
    # 转换为 numpy 数组并提取列
    data = np.array(data)
    indices = data[:, 0].astype(int)  # 确保索引为整数
    values = data[:, 1]

    # 计算量子比特数（根据最大索引确定二进制位数）
    max_index = np.max(indices)
    n_qubits = int(np.ceil(np.log2(max_index + 1))) if max_index > 0 else 1

    # 生成二进制标签 (如 0 → "00", 3 → "11")
    bin_labels = [format(i, "0{}b".format(n_qubits)) for i in indices]

    # 创建图形
    plt.figure(figsize=(8, 4))
    bars = plt.bar(indices, values, color="#4C72B0", edgecolor="black", width=0.6)

    # 添加数值标签
    max_value = np.max(values)
    is_probability = np.all(values <= 1.0)  # 判断是否为概率值

    for bar in bars:
        height = bar.get_height()
        # 动态确定标签位置
        if height > 0.7 * max_value:  # 大数值标签放在柱内
            va = "top"
            y = height - 0.02 * max_value
            color = "white"
        else:  # 小数值标签放在柱外
            va = "bottom"
            y = height + 0.02 * max_value
            color = "black"

        # 动态格式化文本
        if is_probability:
            text = f"{height:.2f}".rstrip("0").rstrip(".")  # 去除多余零
        else:
            text = f"{int(height)}" if height.is_integer() else f"{height:.1f}"

        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            y,
            text,
            ha="center",
            va=va,
            color=color,
            fontsize=8,
        )

    # 设置x轴为二进制标签
    plt.xticks(indices, bin_labels, rotation=45 if n_qubits >= 4 else 0)  # 比特数多时倾斜标签

    # 添加标签和标题
    plt.title(f"Quantum State Distribution ({n_qubits}-qubit)", fontsize=12)
    plt.xlabel("Computational Basis State", fontsize=10)
    plt.ylabel("Probability" if np.all(values <= 1) else "Count", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # 显示图形
    plt.tight_layout()
    plt.show()


def plot_counts_by_theta(x, y):
    plt.figure(figsize=(8, 4))
    plt.rcParams["font.family"] = "DejaVu Sans Mono"
    plt.rcParams["figure.dpi"] = 100
    plt.grid(True, linestyle="--", alpha=0.5)

    # plt.xlim(0.1, 2 * np.pi + 0.1)
    # plt.ylim(0, 100)
    plt.plot(x, y, "o-")
    plt.xlabel("RPhi gate parameter θ")
    plt.ylabel("State 1 counts")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
