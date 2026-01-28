import torch
import os
import sys

# ================= 配置区域 =================
# 请在这里填入你想要检查的 .pt 文件的完整路径
# 例如: "logs/rsl_rl/BeyondMimic/2026-01-27_09-24-34/model_500.pt"
file_path = "/home/chengyuxuan/BeyondMimic/logs/rsl_rl/g1_flat/2026-01-23_15-55-27/model_29999.pt" 
# ===========================================

def inspect_checkpoint(path):
    print(f"\n🔍 正在加载文件: {path}")
    
    if not os.path.exists(path):
        print(f"❌ 错误: 找不到文件，请检查路径是否正确。\n   当前路径: {path}")
        return

    try:
        # map_location='cpu' 确保即使没有显卡也能查看，且不占用显存
        checkpoint = torch.load(path, map_location='cpu')
        
        print("\n📋 === 文件内容结构 (Top-Level Keys) ===")
        if isinstance(checkpoint, dict):
            for key, value in checkpoint.items():
                if isinstance(value, dict):
                    # 如果值是字典，打印出它包含的子键（前5个）
                    sub_keys = list(value.keys())
                    preview = str(sub_keys[:5]) + ("..." if len(sub_keys) > 5 else "")
                    print(f"  🔹 Key: '{key:<20}' | 类型: dict | 子键: {preview}")
                elif torch.is_tensor(value):
                    print(f"  🔹 Key: '{key:<20}' | 类型: Tensor | 形状: {value.shape}")
                else:
                    print(f"  🔹 Key: '{key:<20}' | 类型: {type(value).__name__} | 值: {value}")

            print("\n🩺 === 诊断结果 ===")
            if 'obs_norm_state_dict' in checkpoint:
                print("  ✅ 成功: 文件中包含 'obs_norm_state_dict'。")
            else:
                print("  ❌ 警告: 文件中缺失 'obs_norm_state_dict'！")
                print("     这证实了为什么原始的 rsl_rl 代码会报错 KeyError。")
                print("     请务必保留刚才对 rsl_rl 源码的修改 (if 'obs_norm_state_dict' in ...)。")
        
        else:
            print(f"⚠️  文件加载成功，但它不是一个字典，而是: {type(checkpoint)}")

    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")

if __name__ == "__main__":
    # 如果通过命令行传参，则使用命令行参数，否则使用上方配置的路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    inspect_checkpoint(file_path)