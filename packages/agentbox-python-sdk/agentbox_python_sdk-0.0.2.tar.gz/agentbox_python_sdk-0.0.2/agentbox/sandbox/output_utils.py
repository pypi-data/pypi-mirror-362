# agentbox/utils/output_utils.py

import time

class OutputUtils:
    @staticmethod
    def strip_echo_and_prompt(full_output: str) -> str:
        """
        简单去掉回显：找到第一行命令本身，然后把它以及之前的 prompt 去掉。
        """
        lines = full_output.splitlines()
        new_lines = []
        started = False
        for line in lines:
            if not started and "__CMD_DONE__" in line:
                continue
            # 找到命令行本身，之后开始收集
            if not started and "__CMD_DONE__" not in line and line.strip() != "":
                started = True
                new_lines.append(line)
                continue  # 跳过回显行
            if started:
                if "__CMD_DONE__" in line:
                    break
            new_lines.append(line)

        if new_lines and new_lines[0].strip() == "":
            new_lines = new_lines[1:]
            
        return '\n'.join(new_lines)
    
    @staticmethod
    def read_until_prompt(shell, prompt_markers=('$', '#'), timeout=5):
        """
        从 paramiko.Channel (shell) 读取，直到出现提示符。
        
        :param shell: paramiko.Channel 对象 (通过 invoke_shell() 得到)
        :param prompt_markers: 一组字符串，检测行尾是否是这些提示符
        :param timeout: 最大等待时间（秒）
        :return: 接收到的所有文本
        """
        buf = ""
        start_time = time.time()
        
        while True:
            if shell.recv_ready():
                data = shell.recv(4096).decode("utf-8", errors="ignore")
                buf += data
                # 检测 buf 是否以提示符结尾
                lines = buf.strip().splitlines()
                if lines:
                    last_line = lines[-1].strip()
                    if any(last_line.endswith(marker) for marker in prompt_markers):
                        break
            else:
                # 没有数据就 sleep 一会，避免空转
                time.sleep(0.05)

            # 超时检测
            if time.time() - start_time > timeout:
                break
        return buf
