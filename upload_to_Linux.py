#!/usr/bin/env python3
"""将当前目录下除自身外的所有文件上传到 yw:/home/jupyter/"""

import os
import subprocess
import sys


def main():
    script_name = os.path.basename(__file__)  # 本脚本文件名
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录

    # 收集当前目录下的文件（排除自身）
    files = []
    for name in os.listdir(script_dir):
        full = os.path.join(script_dir, name)
        if os.path.isfile(full) and name != script_name:
            files.append(name)
        # 忽略目录，不做处理

    if not files:
        print("没有需要上传的文件。")
        return

    print(f"共发现 {len(files)} 个文件待上传:")
    for f in files:
        print(f"  - {f}")
    print()

    failed = []
    for f in files:
        src = os.path.join(script_dir, f)
        print(f"正在上传: {f}  ->  yw:/home/jupyter/")
        result = subprocess.run(
            ["scp", src, "yw:/home/jupyter/"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  ✓ 完成")
        else:
            print(f"  ✗ 失败: {result.stderr.strip()}")
            failed.append(f)

    print()
    if failed:
        print(f"以下 {len(failed)} 个文件上传失败: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"全部 {len(files)} 个文件上传成功。")


if __name__ == "__main__":
    main()
