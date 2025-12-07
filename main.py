import random
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# 1. 核心规则与单场比赛模拟
# --------------------------
def simulate_single_match(win_prob_a, win_prob_b):
    """
    模拟一场乒乓球比赛（11分制，需领先2分获胜）
    :param win_prob_a: 选手A每分获胜概率（0-1）
    :param win_prob_b: 选手B每分获胜概率（0-1）
    :return: (winner: str, score_a: int, score_b: int) 获胜者及最终比分
    """
    score_a, score_b = 0, 0
    
    while True:
        # 随机生成每分获胜者（基于概率）
        if random.random() < win_prob_a:
            score_a += 1
        else:
            score_b += 1
        
        # 结束条件：一方≥11分且领先≥2分
        if (score_a >= 11 or score_b >= 11) and abs(score_a - score_b) >= 2:
            break
    
    winner = "A" if score_a > score_b else "B"
    return winner, score_a, score_b

# --------------------------
# 2. 多场模拟与统计
# --------------------------
def simulate_multiple_matches(n_matches, win_prob_a, win_prob_b):
    """
    模拟多场比赛并统计结果
    :param n_matches: 模拟场次
    :param win_prob_a: 选手A每分获胜概率
    :param win_prob_b: 选手B每分获胜概率
    :return: 统计结果字典
    """
    results = {
        "A_wins": 0,  # A获胜场次
        "B_wins": 0,  # B获胜场次
        "all_scores": [],  # 所有场次比分 [(a1,b1), (a2,b2), ...]
        "a_scores": [],    # A所有场次得分
        "b_scores": []     # B所有场次得分
    }
    
    for _ in range(n_matches):
        winner, sa, sb = simulate_single_match(win_prob_a, win_prob_b)
        results["all_scores"].append((sa, sb))
        results["a_scores"].append(sa)
        results["b_scores"].append(sb)
        
        if winner == "A":
            results["A_wins"] += 1
        else:
            results["B_wins"] += 1
    
    # 计算胜率
    results["A_win_rate"] = results["A_wins"] / n_matches
    results["B_win_rate"] = results["B_wins"] / n_matches
    return results

# --------------------------
# 3. 结果可视化分析
# --------------------------
def plot_analysis(results, win_prob_a, win_prob_b):
    """
    可视化统计结果（胜率饼图 + 得分分布直方图）
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 子图1：胜率饼图
    win_rates = [results["A_win_rate"], results["B_win_rate"]]
    labels = [f"选手A\n胜率: {win_rates[0]:.2%}", f"选手B\n胜率: {win_rates[1]:.2%}"]
    colors = ["#FF6B6B", "#4ECDC4"]
    ax1.pie(win_rates, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax1.set_title(f"乒乓球比赛胜率分布\n（A每分胜率: {win_prob_a}, B每分胜率: {win_prob_b}）")
    
    # 子图2：得分分布直方图
    ax2.hist(results["a_scores"], alpha=0.6, label="选手A得分", color="#FF6B6B", bins=15)
    ax2.hist(results["b_scores"], alpha=0.6, label="选手B得分", color="#4ECDC4", bins=15)
    ax2.set_xlabel("单场得分")
    ax2.set_ylabel("场次")
    ax2.set_title("单场得分分布")
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# --------------------------
# 4. 主函数（运行模拟与分析）
# --------------------------
if __name__ == "__main__":
    # 模拟参数设置
    N_MATCHES = 1000  # 模拟总场次
    WIN_PROB_A = 0.55  # 选手A每分获胜概率（略强于B）
    WIN_PROB_B = 0.45  # 选手B每分获胜概率
    
    # 执行多场模拟
    print(f"开始模拟 {N_MATCHES} 场乒乓球比赛...")
    stats = simulate_multiple_matches(N_MATCHES, WIN_PROB_A, WIN_PROB_B)
    
    # 打印核心统计结果
    print("\n=== 模拟结果统计 ===")
    print(f"选手A获胜场次：{stats['A_wins']} 场，胜率：{stats['A_win_rate']:.2%}")
    print(f"选手B获胜场次：{stats['B_wins']} 场，胜率：{stats['B_win_rate']:.2%}")
    print(f"选手A平均得分：{np.mean(stats['a_scores']):.2f} 分")
    print(f"选手B平均得分：{np.mean(stats['b_scores']):.2f} 分")
    print(f"前10场比分示例：{stats['all_scores'][:10]}")
    
    # 可视化分析
    plot_analysis(stats, WIN_PROB_A, WIN_PROB_B)
