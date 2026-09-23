#!/bin/bash

# 通过进程的工作目录（cwd）匹配，而不是命令行参数
# 这样可以找到所有从该目录启动的进程，无论它们用什么命令

TARGET_DIR=$(cd "$(dirname "$0")" && pwd)
USER_NAME="${USER:-chengyuxuan}"

echo "🔍 正在扫描工作目录在 [$TARGET_DIR] 下的进程..."

# 遍历所有属于该用户的进程，检查它们的 cwd
PIDS=""
for pid in $(pgrep -u "$USER_NAME"); do
    # 跳过当前脚本自己
    if [ "$pid" = "$$" ]; then
        continue
    fi
    
    # 读取进程的 cwd
    cwd=$(readlink "/proc/$pid/cwd" 2>/dev/null)
    
    # 如果 cwd 在 TARGET_DIR 下，加入列表
    if [[ "$cwd" == "$TARGET_DIR"* ]]; then
        PIDS="$PIDS $pid"
    fi
done

# 去掉首尾空格
PIDS=$(echo $PIDS | xargs)

# 如果没找到进程，直接退出
if [ -z "$PIDS" ]; then
    echo "✅ 在 [$TARGET_DIR] 下没有发现需要清理的进程。"
    exit 0
fi

echo -e "\n⚠️ 发现以下进程："
echo "-------------------------------------------------------------------"
ps -f -p $PIDS
echo "-------------------------------------------------------------------"
echo "进程数: $(echo $PIDS | wc -w)"

# 安全确认
read -p "❓ 是否确认终止这些进程？(y/n): " confirm

if [[ "$confirm" =~ ^[yY]([eE][sS])?$ ]]; then
    echo "💥 正在清理进程..."
    
    # 先尝试优雅终止
    kill $PIDS 2>/dev/null
    sleep 2
    
    # 检查是否还有残留
    REMAINING=""
    for pid in $PIDS; do
        if kill -0 $pid 2>/dev/null; then
            REMAINING="$REMAINING $pid"
        fi
    done
    
    if [ -n "$REMAINING" ]; then
        echo "⚠️ 部分进程未响应，强制终止..."
        kill -9 $REMAINING 2>/dev/null
    fi
    
    echo "✅ 进程清理完毕！"
else
    echo "🛑 操作已取消。"
fi
