import os, sys
from pathlib import Path

# 关键：在导入 csv_to_npz 前，动态添加 --headless 参数
# 先备份原始参数
original_argv = sys.argv.copy()

try:
    # 创建模拟的命令行参数（必须包含模块名作为第一个参数）
    # 假设 csv_to_npz.py 需要的所有参数都已通过其他方式传入
    sys.argv = [
        "csv_to_npz.py",  # 模拟脚本名
        "--headless",     # 强制无头模式
    ]
    
    # 现在导入模块（它会读取我们伪造的 sys.argv）
    import csv_to_npz
    
finally:
    # 无论是否出错，都要恢复原始参数
    sys.argv = original_argv

def process_folder(input_folder, output_folder, file_extension=None):

    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # 验证输入文件夹
    if not input_path.is_dir():
        raise ValueError(f"[✗] input file not exist: {input_path}")
    
    # 创建输出文件夹
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 遍历所有文件
    for file_path in input_path.rglob("*"):
        print(f"file_path: {file_path}")
        if file_path.is_file():
            # 文件过滤
            if file_extension and file_path.suffix != file_extension:
                continue
            
            # 构建输出路径（保持原有子目录结构）
            relative_path = file_path.relative_to(input_path)
            output_file_path = output_path / relative_path
            
            # 确保输出子目录存在
            output_file_path.parent.mkdir(parents=True, exist_ok=True)

            # 修改output_file_path文件后缀
            output_file_path = str(output_file_path)[:-3] + 'npz'
            print(f"output_file_path: {output_file_path}")
            
            try:
                # 调用处理函数
                csv_to_npz.main_control(str(file_path), output_file_path)
                print(f"[✓] process successed: {file_path} -> {output_file_path}")
            except Exception as e:
                print(f"[✗] process failed: {file_path} - error: {e}")

# 处理所有文件
process_folder("/home/chengyuxuan/BeyondMimic/LaFan1_csv", "/home/chengyuxuan/BeyondMimic/LaFan1_npz")

# # 仅处理 .zip 文件
# process_folder("/path/to/input", "/path/to/output", file_extension=".zip")