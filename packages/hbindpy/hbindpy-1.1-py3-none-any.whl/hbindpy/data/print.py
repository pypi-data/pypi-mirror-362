import sys
import time
import re

class TypeWriter:
    @staticmethod
    def print(text: str, wait: float = 0.05, end: str = '\n'):
        """打字机效果打印文本
        
        :param text: 要打印的文本（可包含多行）
        :param wait: 每个字符打印间隔（秒），默认0.05
        :param end: 结尾字符，默认换行
        """
        for char in text:
            # 立即打印当前字符（无换行）
            sys.stdout.write(char)
            sys.stdout.flush()
            
            # 根据字符类型调整延迟
            delay = wait
            if char in '\n':
                delay *= 6  # 换行时增加延迟模拟自然停顿
            elif char in ',;:':
                delay *= 4  # 标点符号稍作停顿
            
            time.sleep(delay)
        
        # 添加结尾字符
        sys.stdout.write(end)
        sys.stdout.flush()


class BaseColorPrint:
    """基类，定义颜色代码和基础打印方法"""
    
    # ANSI 颜色代码
    COLORS = {
        'black': '\033[30m',     # 黑色
        'red': '\033[31m',       # 红色
        'green': '\033[32m',     # 绿色
        'yellow': '\033[33m',    # 黄色
        'blue': '\033[34m',      # 蓝色
        'magenta': '\033[35m',   # 品红
        'cyan': '\033[36m',      # 青色
        'white': '\033[37m',     # 白色
        'reset': '\033[0m'       # 重置所有样式
    }
    
    # 文本样式代码
    STYLES = {
        'bold': '\033[1m',          # 加粗
        'italic': '\033[3m',        # 斜体
        'underline': '\033[4m',     # 下划线
        'blink': '\033[5m',         # 闪烁
        'reverse': '\033[7m',       # 反显
        'strikethrough': '\033[9m', # 删除线
    }
    
    # 亮色（高强度颜色）
    BRIGHT_COLORS = {
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m'
    }
    
    # 特殊效果
    EFFECTS = {
        'typewriter': TypeWriter.print
    }
    
    # 合并所有代码和效果
    ALL_CODES = {**COLORS, **STYLES, **BRIGHT_COLORS}
    
    # 重置代码
    RESET_CODE = '\033[0m'


class CombinePrint(BaseColorPrint):
    """组合打印类，支持颜色、样式和特殊效果组合"""
    
    # 标签映射（支持别名）
    TAG_MAP = {
        # 样式别名
        'b': 'bold', 'bold': 'bold',
        'i': 'italic', 'italic': 'italic',
        'u': 'underline', 'underline': 'underline',
        's': 'strikethrough', 'strike': 'strikethrough', 
        'r': 'reverse', 'reverse': 'reverse',
        'blink': 'blink',
        
        # 颜色别名
        'r': 'red', 'red': 'red',
        'g': 'green', 'green': 'green',
        'y': 'yellow', 'yellow': 'yellow',
        'b': 'blue', 'blue': 'blue',
        'm': 'magenta', 'magenta': 'magenta',
        'c': 'cyan', 'cyan': 'cyan',
        'w': 'white', 'white': 'white',
        
        # 特殊效果
        't': 'typewriter', 'type': 'typewriter', 'tw': 'typewriter'
    }
    
    @classmethod
    def print(cls, formatted_text: str, default_wait: float = 0.05, end: str = '\n'):
        """
        解析并打印带组合效果的文本
        
        格式: [效果1,效果2,...]文本内容
        示例: "[bold,typewriter,yellow]打字机加粗黄色文本"
        
        :param formatted_text: 格式化的文本
        :param default_wait: 打字机效果的默认延迟
        :param end: 结尾字符，默认换行
        """
        # 分离标签和内容
        match = re.match(r'^\[([^\]]+)\](.*)', formatted_text)
        if not match:
            print(formatted_text, end=end)
            return
        
        tags_str, content = match.groups()
        tags = [tag.strip().lower() for tag in tags_str.split(',')]
        
        # 解析标签
        style_seq = cls.RESET_CODE  # 初始化为重置
        effects = []
        
        for tag in tags:
            # 查找实际标签名（支持别名）
            actual_tag = cls.TAG_MAP.get(tag, tag)
            
            # 分类处理
            if actual_tag in cls.ALL_CODES:
                style_seq += cls.ALL_CODES[actual_tag]
            elif actual_tag in cls.EFFECTS:
                effects.append(actual_tag)
        
        # 构建带样式的文本
        styled_content = f"{style_seq}{content}{cls.RESET_CODE}"
        
        # 应用特殊效果
        if 'typewriter' in effects:
            # 打字机效果
            cls.EFFECTS['typewriter'](styled_content, wait=default_wait, end=end)
        else:
            # 直接打印
            print(styled_content, end=end)
    
    @classmethod
    def demo(cls):
        """演示组合打印效果"""
        print("\n=== 组合打印演示 ===")
        
        # 单效果演示
        cls.print("[bold]这是加粗文本")
        cls.print("[typewriter]这是打字机效果文本")
        cls.print("[red]这是红色文本")
        
        # 组合效果演示
        cls.print("[bold,red]这是加粗红色文本")
        cls.print("[bold,typewriter]打字机加粗效果")
        cls.print("[typewriter,underline,yellow]打字机下划线黄色文本")
        cls.print("[bold,italic,typewriter,cyan]打字机加粗斜体青色文本")
        
        # 使用别名
        cls.print("[b,t]加粗+打字机 (使用别名)")
        cls.print("[u,tw,green]下划线+打字机+绿色 (别名组合)")

# 使用示例
if __name__ == "__main__":
    CombinePrint.print("[bold,typewriter,yellow]打字机加粗黄色文本")
    CombinePrint.print("[underline,red]这是红色下划线文本")
    CombinePrint.print("[b,i,t]加粗斜体打字机效果")
    
    # 演示所有效果
    CombinePrint.demo()