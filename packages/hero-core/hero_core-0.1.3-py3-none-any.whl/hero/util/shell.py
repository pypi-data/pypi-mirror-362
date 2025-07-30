from hero.context import Context
from hero.util import log, function, stream
import re
import asyncio
from typing import Dict, Tuple
import traceback

async def shell_util(command: str, ctx: Context) -> Tuple[str, str]:
    command = re.sub(r"#.*\n?", "", command).strip()
    if not command:
        return "", ""

    log.debug(f"COMMAND: {command}")

    dir = ctx.get("dir", "")
    command = f"cd {dir} && {command}"

    log.debug(f"FULL COMMAND: {command}")

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )

        # 创建任务来实时读取stdout和stderr
        async def read_stream(std_stream, prefix):
            output = []
            buffer = b""
            last_line = None
            while True:
                try:
                    chunk = await std_stream.read(1024)
                    if not chunk:
                        break

                    # Process the chunk byte by byte
                    for byte in chunk:
                        if byte == ord(b"\r"):
                            # Found a carriage return, this might be a tqdm update
                            if buffer:
                                line_str = buffer.decode(
                                    "utf-8", errors="replace"
                                )
                                if "%" in line_str or "it/s" in line_str:
                                    # This is likely a tqdm progress line
                                    clean_line = re.sub(
                                        r"\x1b\[[0-9;]*[a-zA-Z]",
                                        "",
                                        line_str,
                                    )
                                    clean_line = clean_line.strip()
                                    # Skip if it's just a progress indicator
                                    if re.match(
                                        r"^\s*[\d.]+\%|\d+/\d+|\d+it/s",
                                        clean_line,
                                    ):
                                        buffer = b""
                                        continue
                                    if last_line:
                                        output[-1] = clean_line
                                        stream.push(
                                            component="terminal",
                                            action=prefix,
                                            timestamp=function.timestamp(),
                                            payload={
                                                "content": clean_line,
                                                "update_last": True,
                                            },
                                        )
                                    else:
                                        output.append(clean_line)
                                        stream.push(
                                            component="terminal",
                                            action=prefix,
                                            timestamp=function.timestamp(),
                                            payload={"content": clean_line},
                                        )
                                    last_line = clean_line
                                else:
                                    # Regular line with carriage return
                                    line_str = line_str.strip()
                                    if line_str:
                                        output.append(line_str)
                                        stream.push(
                                            component="terminal",
                                            action=prefix,
                                            timestamp=function.timestamp(),
                                            payload={"content": line_str},
                                        )
                                buffer = b""
                        elif byte == ord(b"\n"):
                            # Found a newline, process the buffer
                            if buffer:
                                line_str = buffer.decode(
                                    "utf-8", errors="replace"
                                ).strip()
                                if line_str:
                                    output.append(line_str)
                                    stream.push(
                                        component="terminal",
                                        action=prefix,
                                        timestamp=function.timestamp(),
                                        payload={"content": line_str},
                                    )
                                buffer = b""
                        else:
                            buffer += bytes([byte])

                except Exception as e:
                    log.error(f"Error reading stream: {str(e)}")
                    break

            # Process any remaining data in buffer
            if buffer:
                line_str = buffer.decode("utf-8", errors="replace").strip()
                if line_str:
                    output.append(line_str)
                    stream.push(
                        component="terminal",
                        action=prefix,
                        timestamp=function.timestamp(),
                        payload={"content": line_str},
                    )
            return output

        # 并发读取stdout和stderr
        stdout_lines, stderr_lines = await asyncio.gather(
            read_stream(process.stdout, "stdout"),
            read_stream(process.stderr, "stderr"),
        )

        # 等待进程完成
        await process.wait()

        stdout = function.clean_tqdm_output("\n".join(stdout_lines))
        stderr = function.clean_tqdm_output("\n".join(stderr_lines))

        return stdout, stderr

    except Exception as e:
        log.error(f"Error executing shell: {str(e)}")
        log.error(traceback.format_exc())
        return "", f"Error executing shell: {str(e)}"