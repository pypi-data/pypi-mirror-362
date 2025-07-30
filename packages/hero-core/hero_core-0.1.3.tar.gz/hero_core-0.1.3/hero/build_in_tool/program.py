from typing import Dict, List, TypedDict
import traceback
from hero.agent import Agent
from hero.model import Model
from hero.context import Context
from hero.util import log, function, stream, shell_queue, shell_util
import os
import re
import json
import sys
import platform
from hero.tool import Tool

tool = Tool()

class ProgramParams(TypedDict):
    coder: Model
    patcher: Model
    config_venv_dir: str

@tool.init("program", {
    "coder": Model(),
    "patcher": Model(),
    "config_venv_dir": "",
}, params_type=ProgramParams)
async def program(demand: str, reference_file_list: List[str], params: ProgramParams, ctx: Context):
    """
    <desc>Through programming, accomplish tasks like data processing, mathematical calculations, chart drawing, encoding/decoding, website building, and user demand implementation. The programming languages available include Python, shell (bash), HTML, CSS, JavaScript, TypeScript, Node.js, etc.</desc>
    <params>
        <demand type="string">The detailed requirement to be accomplished through programming, the requirement must be something the program can complete independently without the user making additional modifications or providing extra information. The key information in the user's question or task history should be directly reflected in the requirement.</demand>
        <reference_file_list type="list">Read some files as programming references.</reference_file_list>
    </params>
    <example>
        {
            "tool": "program",
            "params": {
                "demand": "Write a Python program to calculate the sum of two numbers",
                "reference_file_list": ["1.txt", "2.txt"]
            }
        }
    </example>
    """
    try:

        if not demand:
            raise ValueError("demand is required")

        if not reference_file_list:
            reference_file_list = []

        result = await program_run(demand, reference_file_list, params, ctx)

        return result

    except Exception as e:
        log.error(f"Error: {str(e)}")
        log.error(traceback.format_exc())

        return {
            "status": "error",
            "message": f"Error: {str(e)}",
        }

async def program_run(
    demand: str, reference_file_list: List[str], params: ProgramParams, ctx: Context
) -> Dict[str, str]:
    
    run_count = 0
    coder = Agent(name="coder", model=params["coder"], prompt=function.read_default_tool_prompt("coder.md"))
    patcher = Agent(name="patcher", model=params["patcher"], prompt=function.read_default_tool_prompt("patcher.md"))
    config_venv_dir = params["config_venv_dir"]

    # Initialize stdout and stderr
    stdout = b""
    stderr = b""
    is_shell = False
    is_json = False
    json_content = ""

    resolve_error_demand = ""
    is_output_file = False
    output_file_path = ""
    output_file_name = ""
    output_file_list = []
    result_list = []
    shell_list = []

    try:
        run_count += 1
        log.debug(f"program run_count: {run_count}")

        reference_file_content = ""

        dir = ctx.get("dir", "")

        # 数组去重
        reference_file_list = list(set(reference_file_list))

        for file_name in reference_file_list:
            extension = os.path.splitext(file_name)[1].lower()

            file_path = os.path.join(dir, file_name)
            if not os.path.exists(file_path):
                log.error(f"File {file_name} does not exist")
                continue

            log.debug(f"REFERENCE FILE: {file_name}")

            reference_file_content += f"<file name=\"{file_name}\">\n"

            if extension in [
                ".py",
                ".js",
                ".ts",
                ".html",
                ".css",
                ".json",
                ".yaml",
            ]:
                reference_file_content += function.read_file(dir, file_name)
            elif extension in [".png", ".jpg", ".jpeg", ".gif"]:
                result = function.image_to_base64_url(file_path)
                if result["status"] == "success":
                    # 图片截断，否则会超过长度
                    truncated = result["base64_url"][:5000] + " ...(truncated)"
                    reference_file_content += truncated
                else:
                    reference_file_content += f"Error converting image: {result['message']}"
                # 其他格式文件，可能是数据文件，读取前100行
            else:
                reference_file_content += function.read_file_n_lines(
                    dir, file_name, 100
                )

            reference_file_content += "\n</file>\n"

        workspace_file_list = function.list_files_recursive(dir)
        log.debug(f"workspace_file_list: {workspace_file_list}")

        environment = f'- OS: {platform.system()} {platform.release()}\n- Local supported fonts: "Arial Unicode MS", "sans-serif"\n'
        environment += f"- Python version: {sys.version}\n"
        
        log.debug(f"environment: {environment}")

        user_message = function.read_user_message(ctx)

        async for token in coder.chat(
            message=demand
            + "\n\n"
            + "Please generate the code file and the shell command to execute the code file.",
            params={
                "environment": environment,
                "reference_file": reference_file_content,
                "user_message": user_message,
                "workspace_file_list": workspace_file_list,
            },
        ):
            if token.get("action") == "content_line":
                line = token.get("payload", {}).get("content")

                # 处理代码文件
                if re.search(r"<code language=\"(.*?)\" file=\"(.*?)\">", line):
                    match = re.search(
                        r"<code language=\"(.*?)\" file=\"(.*?)\">", line
                    )
                    if match:
                        output_file_name = match.group(2)
                    output_file_path = os.path.join(dir, output_file_name)

                    # 不添加.patch文件到output_file_list
                    if not output_file_name.endswith(".patch"):
                        output_file_list.append(output_file_name)

                    # 如果文件存在，则把现有文件改名
                    if os.path.exists(output_file_path):
                        # 获取当前时间
                        timestamp = function.timestamp()
                        # 改名
                        os.rename(
                            output_file_path,
                            os.path.join(
                                dir, f"__{output_file_name}_{timestamp}.py"
                            ),
                        )

                    # 新建空文件
                    with open(output_file_path, "w", encoding="utf-8") as f:
                        f.write("")

                    # 设置标志位，后续将 line 写入文件
                    is_output_file = True

                    stream.push(
                        component="editor",
                        action="open_file",
                        timestamp=function.timestamp(),
                        payload={"path": output_file_name},
                    )

                    # 清空 line，特殊标志不输出，原始内容debug打印出来
                    line = None

                elif "</code>" in line:
                    stream.push(
                        component="editor",
                        action="close_file",
                        timestamp=function.timestamp(),
                        payload={"path": output_file_name},
                    )
                    
                    is_output_file = False
                    output_file_name = ""
                    output_file_path = ""
                    line = None

                # 处理 shell 命令
                elif "<shell>" in line:
                    is_shell = True

                    stream.push(
                        component="message",
                        action="shell_start",
                        timestamp=function.timestamp(),
                        payload={},
                    )
                    line = None
                elif "</shell>" in line:
                    is_shell = False

                    stream.push(
                        component="message",
                        action="shell_end",
                        timestamp=function.timestamp(),
                        payload={},
                    )
                    line = None

                # 处理结果
                elif re.search(r"<result file=\"(.*?)\">", line):
                    match = re.search(r"<result file=\"(.*?)\">", line)
                    if match:
                        file_name = match.group(1)
                    else:
                        file_name = ""
                    result_list.append(file_name)

                    stream.push(
                        component="message",
                        action="program_result",
                        timestamp=function.timestamp(),
                        payload={
                            "name": "coder",
                            "content": file_name,
                            "reasoning_content": "",
                        },
                    )
                    line = None

                # 处理json内容
                elif re.search(r"^```json$", line):
                    is_json = True
                    is_output_file = False
                    line = None
                    stream.push(
                        component="message",
                        action="json_start",
                        timestamp=function.timestamp(),
                        payload=token.get("payload", {}),
                    )
                elif re.search(r"^```$", line):
                    is_json = False
                    is_output_file = False
                    line = None
                    stream.push(
                        component="message",
                        action="json_end",
                        timestamp=function.timestamp(),
                        payload=token.get("payload", {}),
                    )

                if not line == None:
                    if is_output_file:
                        with open(output_file_path, "a", encoding="utf-8") as f:
                            f.write(line)

                        stream.push(
                            component="editor",
                            action="append_file",
                            timestamp=function.timestamp(),
                            # TODO: 修改 prompt 返回路径
                            payload={"path": output_file_name, "content": line},
                        )
                    elif is_shell:
                        shell_list.append(line)

                        stream.push(
                            component="message",
                            action="shell_line",
                            timestamp=function.timestamp(),
                            payload={
                                "file_name": output_file_name,
                                "content": line,
                            },
                        )
                    elif is_json:
                        json_content += line

                        stream.push(
                            component="message",
                            action="json_line",
                            timestamp=function.timestamp(),
                            payload=token.get("payload", {}),
                        )
                    else:
                        stream.push(
                            component="message",
                            action=token.get("action", ""),
                            timestamp=function.timestamp(),
                            payload={
                                "name": "coder",
                                "content": line,
                                "reasoning_content": "",
                            },
                        )
            else:
                stream.push(
                    component="message",
                    action=token.get("action", ""),
                    timestamp=function.timestamp(),
                    payload=token.get("payload", {}),
                )
        # 处理 json 内容
        if json_content:
            try:
                json_data = json.loads(json_content)
                log.debug(f"json_data: {json_data}")
                if json_data.get("tool") == "search":
                    message = f"Need to search for more information, and the query is: {json_data.get('query')}\n\n"
                    return {
                        "status": "interrupt",
                        "message": message,
                    }
                elif json_data.get("tool") == "complated":
                    message = f"The program has completed, please check the workspace_file_list to get the result.\n\n"
                    return {
                        "status": "success",
                        "message": message,
                    }
                elif json_data.get("tool") == "execute_shell":
                    command_list = json_data.get("params").get("command_list")
                    shell_list.extend(command_list)
            except Exception as e:
                log.error(f"Error: {str(e)}")
                log.error(traceback.format_exc())

        # 执行 shell 命令
        for line in shell_list:
            log.debug(f"shell: {line}")
            line = re.sub(r"#.*\n?", "", line).strip()
            log.debug(f"shell clean: {line}")
            if not line:
                continue

            stdout, stderr = await shell_util(build_command(config_venv_dir, line), ctx)
            # patch 命令执行失败，则需要修复
            if (stderr or "failed at" in stdout) and line.startswith("patch"):

                # 用正则删除^patch --batch --verbose
                file_part = re.sub(r"^patch", "", line).strip()
                file_part = (
                    file_part.replace("--batch", "")
                    .replace("--verbose", "")
                    .strip()
                )

                original_file = file_part.split("<")[0].strip()
                log.debug(f"original_file: {original_file}")
                patch_file = file_part.split("<")[1].strip()
                log.debug(f"patch_file: {patch_file}")
                patch_shell_command = line
                error_message = stdout + "\n\n" + stderr

                result = await patch_run(
                    config_venv_dir,
                    original_file,
                    patch_file,
                    patch_shell_command,
                    error_message,
                    patcher=patcher,
                    patch_count=0,
                    ctx=ctx,
                )

                log.debug(f"patch_run result: {result}")

                # 修复成功，则不输出错误信息，并删除patch文件
                if result.get("status") == "success":
                    stderr = ""

            if stderr:
                run_error = True
                resolve_error_demand += f"## Execute command `{line}`\n\n"
                resolve_error_demand += f"### stdout:\n\n"
                resolve_error_demand += (
                    f"{function.get_head_and_tail_n_chars(stdout)}\n\n"
                )
                resolve_error_demand += f"### stderr:\n\n"
                resolve_error_demand += (
                    f"{function.get_head_and_tail_n_chars(stderr)}\n\n"
                )
                resolve_error_demand += f"Please resolve the error. Don't output the normal information in the stderr.\n"

                # 跳过剩余命令执行
                break

            if line.startswith("patch"):
                if os.path.exists(os.path.join(dir, line.split("<")[1].strip())):
                    os.remove(os.path.join(dir, line.split("<")[1].strip()))

            # 保存执行结果
            shell_result = f"## Execute command `{line}` result:\n\n"
            shell_result += f"### stdout:\n\n"
            shell_result += f"{stdout}\n\n"
            shell_result += f"### stderr:\n\n"
            shell_result += f"{stderr}\n\n"

            with open(
                os.path.join(dir, f"__shell_result_{function.timestamp()}.md"),
                "a",
                encoding="utf-8",
            ) as f:
                f.write(shell_result)

        if len(shell_list) == 0:
            resolve_error_demand += "The code has not been executed. You must use the shell command to execute the code.\n\n"

        message = ""
        if stdout or stderr:  # Only add stdout/stderr sections if there was output
            if stdout:
                message += f"## Stdout:\n\n"
                message += f"{function.get_head_and_tail_n_chars(stdout)}\n\n"
            if stderr:
                message += f"## Stderr:\n\n"
                message += f"{function.get_head_and_tail_n_chars(stderr)}\n\n"

        # 如果执行成功，返回结果
        return {
            "status": "success",
            "message": message,
            # "result": result_list,
        }

    except Exception as e:
        log.error(f"Error: {str(e)}")
        log.error(traceback.format_exc())

        message = ""

        if stdout or stderr:  # Only add stdout/stderr sections if there was output
            if stdout:
                message += f"## Stdout:\n\n"
                message += f"{function.get_head_and_tail_n_chars(stdout)}\n\n"
            if stderr:
                message += f"## Stderr:\n\n"
                message += f"{function.get_head_and_tail_n_chars(stderr)}\n\n"

        # 把已生成文件，添加到 reference_file_list 中
        for file_name in output_file_list:
            if file_name in result_list:
                continue
            reference_file_list.append(file_name)

        message = f"Please resolve the error. Error: {str(e)}\n\n"

        # 重新执行
        result = await program_run(message, reference_file_list, params, ctx)
        return result
    
async def shell_run(command: str, dir: str):
    """
    TODO: 让 coder 判断当前命令是否是一个需要长时间运行的命令如启动一个图形界面或网站
    """
    run_error = False
    resolve_error_demand = ""
    shell_result = ""

    try:
        async for output in shell_queue.add_shell(dir, command):
            if isinstance(output, Exception):
                output = str(output)
                run_error = True
                resolve_error_demand += f"## Execute command `{command}` error:\n"
                resolve_error_demand += f"{output}\n"
                resolve_error_demand += f"Please resolve the error.\n"
            else:
                shell_result = f"## Execute command `{command}` result:\n\n"
                shell_result += f"### stdout:\n\n"
                shell_result += f"{output}\n\n"
                shell_result += f"### stderr:\n\n"
                shell_result += f"{output}\n\n"
            stream.push(
                component="terminal",
                action="output",
                timestamp=function.timestamp(),
                payload={"output": output},
            )
    except Exception as e:
        log.error(f"Error: {str(e)}")
        log.error(traceback.format_exc())
        run_error = True
        resolve_error_demand += f"## Execute command `{command}` error:\n"
        resolve_error_demand += f"{str(e)}\n"
        resolve_error_demand += f"Please resolve the error.\n"

    with open(os.path.join(dir, f"__shell_result_{function.timestamp()}.md"), "a") as f:
                f.write(shell_result)

    return run_error, resolve_error_demand

async def patch_run(
    config_venv_dir: str,
    original_file: str,
    patch_file: str,
    patch_shell_command: str,
    error_message: str,
    patcher: Agent,
    patch_count: int,
    ctx: Context,
) -> Dict[str, str]:
    try:
        patch_count += 1

        if patch_count > 3:
            patch_count = 0
            return {
                "status": "error",
                "message": f"Patch file fixed failed, try {patch_count - 1} times",
            }

        log.debug(f"patch run_count: {patch_count}")

        dir = ctx.get("dir")

        original_file_content = function.file_to_text_with_line_number(
            os.path.join(dir or "", original_file)
        )
        patch_file_content = function.file_to_text_with_line_number(
            os.path.join(dir or "", patch_file)
        )

        is_output_file = False
        output_file_path = ""
        output_file_name = ""
        output_file_list = []

        is_shell = False
        shell_list = []

        async for token in patcher.chat(
            message="Please fix the error of patch file carefully, then return the fixed patch file and the fixed patch shell command accurately.",
            params={
                "original_file": original_file_content,
                "patch_file": patch_file_content,
                "patch_shell_command": patch_shell_command,
                "error_message": error_message,
            },
        ):
            if token.get("action") == "content_line":
                line = token.get("payload", {}).get("content")

                # 处理代码文件
                if re.search(
                    r"<code language=\"(.*?)\" file=\"(.*?)\" file=\"(.*?)\">",
                    line,
                ):
                    match = re.search(
                        r"<code language=\"(.*?)\" file=\"(.*?)\" file=\"(.*?)\">",
                        line,
                    )
                    if match:
                        output_file_name = match.group(2)
                    output_file_path = os.path.join(dir or "", output_file_name)
                    output_file_list.append(output_file_name)

                    # 如果文件存在，则把现有文件改名
                    if os.path.exists(output_file_path):
                        # 获取当前时间
                        timestamp = function.timestamp()
                        # 改名
                        os.rename(
                            output_file_path,
                            os.path.join(
                                dir or "", f"__{output_file_name}_{timestamp}.py"
                            ),
                        )

                    # 新建空文件
                    with open(output_file_path, "w", encoding="utf-8") as f:
                        f.write("")

                    # 设置标志位，后续将 line 写入文件
                    is_output_file = True

                    stream.push(
                        component="editor",
                        action="open_file",
                        timestamp=function.timestamp(),
                        payload={"file_name": output_file_name},
                    )

                    # 清空 line，特殊标志不输出，原始内容debug打印出来
                    line = None

                elif "</code>" in line:
                    stream.push(
                        component="editor",
                        action="close_file",
                        timestamp=function.timestamp(),
                        payload={"file_name": output_file_name},
                    )

                    is_output_file = False
                    output_file_name = ""
                    output_file_path = ""
                    line = None

                # 处理 shell 命令
                elif "<shell>" in line:
                    is_shell = True

                    stream.push(
                        component="message",
                        action="shell_start",
                        timestamp=function.timestamp(),
                        payload={},
                    )
                    line = None
                elif "</shell>" in line:
                    is_shell = False

                    stream.push(
                        component="message",
                        action="shell_end",
                        timestamp=function.timestamp(),
                        payload={},
                    )
                    line = None

                if not line == None:
                    if is_output_file:
                        with open(output_file_path, "a", encoding="utf-8") as f:
                            f.write(line)

                        stream.push(
                            component="editor",
                            action="append_file",
                            timestamp=function.timestamp(),
                            payload={
                                "file_name": output_file_name,
                                "content": line,
                            },
                        )
                    elif is_shell:
                        shell_list.append(line)

                        stream.push(
                            component="message",
                            action="shell_line",
                            timestamp=function.timestamp(),
                            payload={"content": line},
                        )
                    else:
                        stream.push(
                            component="message",
                            action=token.get("action", ""),
                            timestamp=function.timestamp(),
                            payload={
                                "name": "coder",
                                "content": line,
                                "reasoning_content": "",
                            },
                        )
            else:
                stream.push(
                    component="message",
                    action=token.get("action", ""),
                    timestamp=function.timestamp(),
                    payload=token.get("payload", {}),
                )

        for line in shell_list:
            line = re.sub(r"#.*\n?", "", line).strip()
            if not line:
                continue

            stdout, stderr = await shell_util(build_command(config_venv_dir, line), ctx)

            if stderr or "failed at" in stdout:
                return await patch_run(
                    config_venv_dir=config_venv_dir,
                    original_file=original_file,
                    patch_file=output_file_list[0],
                    patch_shell_command=line,
                    error_message=stdout + "\n\n" + stderr,
                    patcher=patcher,
                    patch_count=patch_count,
                    ctx=ctx,
                )
            else:
                patch_count = 0
                if os.path.exists(os.path.join(dir or "", patch_file)):
                    os.remove(os.path.join(dir or "", patch_file))
                clean_patch_file(dir or "")

        return {
            "status": "success",
            "message": "Patch file fixed successfully",
        }

    except Exception as e:
        log.error(f"Error: {str(e)}")
        log.error(traceback.format_exc())

        return await patch_run(
            config_venv_dir=config_venv_dir,
            original_file=original_file,
            patch_file=patch_file,
            patch_shell_command=patch_shell_command,
            error_message=error_message,
            patcher=patcher,
            patch_count=patch_count,
            ctx=ctx,
        )

def clean_patch_file(dir: str):
    for file in os.listdir(dir):
        if (
            file.endswith(".orig")
            or file.endswith(".rej")
            or file.endswith(".patch")
            or file.endswith(".patchf")
        ):
            os.remove(os.path.join(dir, file))

def build_command(config_venv_dir: str, line: str):
        """构建激活虚拟环境的命令"""
        if config_venv_dir:
            return f"bash -c 'source {config_venv_dir}/bin/activate && {line}'"

        return line