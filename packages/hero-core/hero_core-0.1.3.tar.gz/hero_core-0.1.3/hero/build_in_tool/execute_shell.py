from typing import List
import traceback
from hero.context import Context
from hero.util import log, function
from hero.util.shell import shell_util
import re
from hero.tool import Tool

tool = Tool()

@tool.init("execute_shell")
async def execute_shell(command_list: List[str], ctx: Context):
    """
    <desc>Execute shell commands to complete tasks.</desc>
    <params>
        <command_list type="list">The shell command list to execute.</command_list>
    </params>
    <example>
        {
            "tool": "execute_shell",
            "params": {
                "command_list": ["python main.py", "python test.py"]
            }
        }
    </example>
    """
    if not command_list:
        return {"status": "error", "message": "No command list provided."}

    message_list = []

    for command in command_list:
        try:
            # 执行命令
            command = re.sub(r"#.*\n?", "", command).strip()
            if not command:
                continue

            stdout, stderr = await shell_util(command, ctx)

            message = f'<shell command="{command}">\n\n'
            message += f"## Stdout:\n\n"
            message += f"{function.get_head_and_tail_n_chars(stdout)}\n\n"
            message += f"## Stderr:\n\n"
            message += f"{function.get_head_and_tail_n_chars(stderr)}\n\n"
            message += f"</shell>\n\n"

            message_list.append(message)

            if stderr:
                return {
                    "status": "error",
                    "message": "\n\n".join(message_list),
                }

        except Exception as e:
            log.error(f"Error: {str(e)}")
            log.error(traceback.format_exc())
            message_list.append(f"<error>\n\n{str(e)}\n\n</error>\n\n")
            return {
                "status": "error",
                "message": "\n\n".join(message_list),
            }

    return {
        "status": "success",
        "message": "\n\n".join(message_list),
    }
