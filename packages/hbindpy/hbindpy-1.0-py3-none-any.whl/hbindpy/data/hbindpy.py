import argparse
import sys
import os
import logging
from .setup_engine import setup, build
from .utils import setup_logging, ensure_dirs
from .print import CombinePrint
from .version import __version__, version_info

def main():
    import warnings
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(prog="hbindpy")
    parser.add_argument("--compile", action="store_true", help="编译项目")
    parser.add_argument("-V", "--version", action="store_true", help="显示版本信息")
    parser.add_argument("-std", help="设置C++标准 (例如: c++17)")
    parser.add_argument("-d", "--detailed", action="store_true", help="输出详细信息")
    parser.add_argument("-e", "--exe", action="store_true", help="生成可执行文件(EXE)")
    # 新增参数
    parser.add_argument("-p", action="append", default=[], help="额外编译器参数")
    parser.add_argument("--debug", action="store_true", help="包含调试信息")
    parser.add_argument("--optimize", choices=["O0", "O1", "O2", "O3", "Os"], help="优化级别")
    parser.add_argument("--no-warnings", action="store_true", help="禁用警告")
    parser.add_argument("--static", action="store_true", help="静态链接")
    parser.add_argument("--no-threading", action="store_true", help="禁用多线程支持")
    parser.add_argument("--no-exceptions", action="store_true", help="禁用异常")
    parser.add_argument("--no-rtti", action="store_true", help="禁用RTTI")
    parser.add_argument("--no-pic", action="store_true", help="禁用位置无关代码")
    parser.add_argument("--verbose", action="store_true", help="详细编译输出")

    args = parser.parse_args()
    
    # 版本信息
    if args.version:
        CombinePrint.print(f"[bold,t,b]hbindpy - {__version__}")
        return
    
    # 编译模式
    if not args.compile:
        parser.print_help()
        return
    
    # 设置日志
    logger = setup_logging(args.detailed)
    ensure_dirs()
    
    try:
        # 动态导入用户setup配置
        sys.path.insert(0, os.getcwd())
        from setup import config as user_config
        
        # 应用命令行参数覆盖
        if args.std:
            user_config.std = args.std
        if args.debug:
            user_config.debug = True
        if args.optimize:
            user_config.optimize = args.optimize
        if args.no_warnings:
            user_config.warnings = False
        if args.static:
            user_config.static = True
        if args.no_threading:
            user_config.threading = False
        if args.no_exceptions:
            user_config.exceptions = False
        if args.no_rtti:
            user_config.rtti = False
        if args.no_pic:
            user_config.pic = False
        if args.verbose:
            user_config.verbose = True
        
        # 添加-p参数
        user_config.compiler_args.extend(args.p)
        
        # 执行编译
        return_code = build(
            user_config,
            detailed=args.detailed,
            exe_mode=args.exe
        )
        
        sys.exit(return_code)
        
    except ImportError:
        logging.error("当前目录未找到setup.py配置文件!")
        sys.exit(1)
    except Exception as e:
        logging.error(f"构建失败: {str(e)}")
        sys.exit(2)

if __name__ == "__main__":
    CombinePrint.print("[bold,green,blink,italic,typewriter]--------------------hbindpy--------------------",0.01)
    main()