"""
xterm util
"""
import os
import pty
import select
import termios
import struct
import fcntl
import asyncio
from typing import Optional

from hero.util import log

class Terminal:
    """
    terminal
    """
    def __init__(self):
        self.pid: Optional[int] = None
        self.fd: Optional[int] = None
        self.current_dir = os.getcwd()
        # 设置更美观的提示符样式，只显示最后一级目录
        self.prompt = f"\033[1;32m{os.path.basename(self.current_dir)}\033[0m \033[1;34m$\033[0m "
        self.old_settings = None

    async def start(self, working_dir: Optional[str] = None):
        """启动伪终端"""
        # 如果已经存在终端，先清理
        self.cleanup()
        
        if working_dir:
            self.current_dir = working_dir
        
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.environ["TERM"] = "xterm-256color"
            os.environ["PS1"] = "\\[\\033[1;32m\\]\\W\\[\\033[0m\\] $ "
            os.environ["CLICOLOR"] = "1"
            os.environ["LSCOLORS"] = "ExFxBxDxCxegedabagacad"
            os.environ["BASH_SILENCE_DEPRECATION_WARNING"] = "1"
            os.chdir(self.current_dir)
            os.execv("/bin/bash", ["bash", "--noprofile", "--norc", "-i"])

        else:
            self.old_settings = termios.tcgetattr(self.fd)
            # 启用回显
            new_settings = termios.tcgetattr(self.fd)
            new_settings[3] = new_settings[3] | termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSADRAIN, new_settings)
            # 立即触发提示符显示
            self.update_prompt()
            
    def update_prompt(self):
        """更新提示符"""
        if self.fd is None:
            return
        # 直接发送提示符，不需要换行符
        self.write_input(b"")
            
    def handle_resize(self, rows: int, cols: int):
        """处理终端大小调整"""
        if self.fd is None:
            return
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)
            
    async def read_output(self):
        """读取终端输出"""
        if self.fd is None:
            return
        timeout = 10.0
        try:
            flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            start_time = asyncio.get_event_loop().time()
            while True:
                # 使用异步方式读取
                try:
                    # 使用 run_in_executor 异步读取
                    output = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            None, os.read, self.fd, 1024
                        ),
                        timeout=0.01
                    )
                    
                    if output:
                        print(f"output: {output}")
                        output = output.decode()
                        yield output
                        # 重置开始时间，因为收到了输出
                        start_time = asyncio.get_event_loop().time()
                except asyncio.TimeoutError:
                    pass
                except BlockingIOError:
                    pass
                
                # 如果超过10秒没有新输出，则退出循环
                if asyncio.get_event_loop().time() - start_time > timeout:
                    break

                # 短暂让出控制权，避免CPU占用过高
                await asyncio.sleep(0.001)

        except (OSError, select.error) as e:
            log.error(f"Terminal read error: {str(e)}")
            self.cleanup()
                    
    def write_input(self, data: bytes):
        """写入输入到终端"""
        if self.fd is None:
            return
        try:
            os.write(self.fd, data)
        except (OSError, select.error) as e:
            log.error(f"Terminal write error: {str(e)}")
            self.cleanup()
            
    def cleanup(self):
        """清理资源"""
        if self.fd is not None and self.old_settings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self.old_settings = None
            
        if self.pid:
            try:
                os.kill(self.pid, 9)
                os.waitpid(self.pid, 0)
            except (OSError, ProcessLookupError):
                pass
            self.pid = None
            
        if self.fd:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None

terminal = Terminal()

class ShellQueue:
    """
    shell queue
    """
    def __init__(self):
        self.queue = []
        self.is_running = False
        
    async def add_shell(self, dir: str, shell: str):
        """
        add shell to queue
        """
        self.queue.append((dir, shell))
        if not self.is_running:
            self.is_running = True
            try:
                while self.queue:
                    dir, shell = self.queue.pop(0)
                    async for output in self.execute_shell(dir, shell):
                        yield output
            finally:
                self.is_running = False
            
    async def execute_shell(self, dir: str, shell: str):
        """
        execute shell
        """
        try:
            # 获取对应连接的终端实例
            instance = terminal
            
            # 如果终端未启动，启动终端
            if not instance.fd:
                await instance.start(dir)

            log.info(f"current_dir: {instance.current_dir}, working_dir: {dir}")
            if instance.current_dir != dir:
                instance.write_input(f"cd {dir}\n".encode())
                async for output in instance.read_output():
                    yield output
            
            # 写入命令到终端
            instance.write_input(f"{shell}\n".encode())
            
            # 读取输出
            async for output in instance.read_output():
                yield output
            
        except Exception as e:
            yield e

shell_queue = ShellQueue()