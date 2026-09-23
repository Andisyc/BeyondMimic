#!/bin/bash

# 1. 自动获取当前脚本所在的绝对路径，作为要匹配的仓库目录
# 这样即使你不在该目录下，直接输入路径运行此脚本也能精准匹配
TARGET_DIR=$(cd "$(dirname "$0")" && pwd)
USER_NAME="${USER:-chengyuxuan}"

echo "🔍 正在扫描属于 [$USER_NAME] 且包含路径 [$TARGET_DIR] 的进程..."

# 2. 查找 PID：-u 限定用户，-f 匹配完整路径
# 排除当前脚本自身的 PID（$$ 是当前 shell 的 PID）
PIDS=$(pgrep -u "$USER_NAME" -f "$TARGET_DIR" | grep -v "^$$\$")

# 如果没找到进程，直接退出
if [ -z "$PIDS" ]; then
    echo "✅ 在 [$TARGET_DIR] 下没有发现需要清理的进程。"
    exit 0
fi

echo -e "\n⚠️ 发现以下疑似有问题的训练进程："
echo "-------------------------------------------------------------------"
# 3. 打印出这些 PID 的详细信息供你审查
ps -f -p $PIDS
echo "-------------------------------------------------------------------"

# 4. 安全确认
read -p "❓ 是否确认使用 kill -9 强制终止上述所有进程？(y/n): " confirm

if [[ "$confirm" =~ ^[yY]([eE][sS])?$ ]]; then
    echo "💥 正在清理进程..."
    # 强制结束列出的所有进程
    kill -9 $PIDS 2>/dev/null
    echo "✅ 进程清理完毕！"
else
    echo "🛑 操作已取消，进程仍在运行。"
fi
