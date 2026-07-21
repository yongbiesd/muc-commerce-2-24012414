from pathlib import Path
import pandas as pd

def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    # 读取三张数据表
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    # 原有：总用户数问答
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # ====================== TODO 4-1 四类问答 ======================
    # 1. 流失率相关问答
    if any(word in normalized for word in ["流失率", "流失人数", "流失用户"]):
        return f"平台总流失用户{int(metrics['流失人数']):,}人，整体流失率为{metrics['流失率']:.1%}。"

    # 2. 平均订单相关问答
    if any(word in normalized for word in ["订单", "平均订单", "下单次数"]):
        return f"平台用户平均订单数为{metrics['平均订单数']:.2f}单/人。"

    # 3. 偏好品类相关问答
    if any(word in normalized for word in ["品类", "偏好品类", "哪个品类用户最多"]):
        top_category = category_df.loc[category_df["用户数"].idxmax()]
        return f"用户最多的偏好品类是{top_category['PreferedOrderCat']}，共有{int(top_category['用户数']):,}位用户。"

    # 4. 生命周期风险问答（CSV阶段列名TenureGroup）
    if any(word in normalized for word in ["生命周期", "流失最高", "哪个阶段流失风险高"]):
        max_loss_segment = segment_df.loc[segment_df["流失率"].idxmax()]
        return f"流失风险最高的用户阶段是{max_loss_segment['TenureGroup']}，流失率达到{max_loss_segment['流失率']:.1%}。"

    # 兜底提示
    return "暂时无法识别该问题，你可以询问：总用户数、流失率、平均订单、热门品类、流失最高用户阶段。"