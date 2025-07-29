import os
from multiprocessing import cpu_count, Pool
from tqdm import tqdm
from functools import partial

def _count_files_in_dir(ends, args):
    root, files = args
    return sum(1 for file in files if file.lower().endswith(ends))

def count_files_by_end(directory, ends=".png", workers=None):
    """
    统计目录下所有文件的数量，支持多进程并行处理。
    该函数会遍历指定目录及其子目录，统计所有文件的数量。
    Args:
        directory: 要扫描的目录路径
        workers: 并行工作进程数(默认使用CPU核心数)
    """

    # 设置默认worker数为CPU核心数
    if workers is None:
        workers = max(cpu_count() - 1, 1)  # 保留一个核心用于其他任务
    
    # 收集所有目录和文件
    walk_results = []
    for root, _, files in os.walk(directory):
        walk_results.append((root, files))
    
    # 创建进程池并处理
    with Pool(workers) as pool:
        func = partial(_count_files_in_dir, ends)
        results = list(tqdm(
            pool.imap(func, walk_results),
            total=len(walk_results),
            desc="Scanning Dirs",
            unit="dir",
            mininterval=1  # 更新进度条的最小间隔(秒)
        ))
    
    return sum(results)

if __name__ == '__main__':
    import argparse
    
    # 设置命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("-j", "--workers", type=int, default=None,
                       help="Number of worker processes")
    parser.add_argument("-e", "--ends", type=str, default=".png",
                       help="File extension to count (default: .png)")
    args = parser.parse_args()
    
    # 执行统计
    files_count = count_files_by_end(args.directory, ends=args.ends, workers=args.workers)
    print(f"Total files: {files_count}")

