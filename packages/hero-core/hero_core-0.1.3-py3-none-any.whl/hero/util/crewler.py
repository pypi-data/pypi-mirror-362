import asyncio
from pathlib import Path
from typing import Set
from playwright.async_api import async_playwright
import threading
import random
import time
import os
import weakref
from . import log, function

# 用于控制最大并发数的信号量
MAX_CONCURRENT_BROWSERS = 5
MAX_RETRY_COUNT = 2
MONITOR_INTERVAL = 10
browser_semaphore = threading.Semaphore(MAX_CONCURRENT_BROWSERS)

HEADLESS = True

# 全局活跃浏览器实例跟踪
_active_scrapers: Set[weakref.ref] = set()
_global_monitor_running = False
_global_monitor_lock = threading.Lock()


# 全局监控任务，定期检查浏览器状态和信号量
async def _global_browser_monitor():
    """Global monitoring task, periodically check and clean inactive browser instances"""
    # log.info("Global browser monitoring task started")

    while True:
        try:
            # 每30秒检查一次
            await asyncio.sleep(MONITOR_INTERVAL)

            # 检查信号量状态
            semaphore_value = browser_semaphore._value
            if semaphore_value < 0 or semaphore_value > MAX_CONCURRENT_BROWSERS:
                log.warning(
                    f"Semaphore value is abnormal: {semaphore_value}, reset to {MAX_CONCURRENT_BROWSERS}"
                )
                browser_semaphore._value = MAX_CONCURRENT_BROWSERS

            # 检查活跃的抓取器
            active_count = len(_active_scrapers)
            # logger.info(
            #     f"当前活跃抓取器: {active_count}，可用信号量: {semaphore_value}/{MAX_CONCURRENT_BROWSERS}"
            # )

            # 清理已失效的弱引用
            dead_refs = []
            for ref in _active_scrapers:
                if ref() is None:
                    dead_refs.append(ref)

            for ref in dead_refs:
                _active_scrapers.remove(ref)

            # 如果信号量全部被占用但没有活跃的抓取器，重置信号量
            if semaphore_value <= 0 and len(_active_scrapers) == 0:
                log.warning(
                    "Detected that the signal is exhausted but there are no active scrapers, reset the signal"
                )
                browser_semaphore._value = MAX_CONCURRENT_BROWSERS

        except Exception as e:
            log.error(f"Global monitoring task error: {str(e)}")


# 启动全局监控
def ensure_monitor_running():
    """Ensure that the global monitoring task is running"""
    global _global_monitor_running

    with _global_monitor_lock:
        if not _global_monitor_running:
            try:
                # 创建新的事件循环运行监控任务
                monitor_loop = asyncio.new_event_loop()

                def run_monitor():
                    asyncio.set_event_loop(monitor_loop)
                    monitor_loop.run_until_complete(_global_browser_monitor())

                # 启动监控线程
                monitor_thread = threading.Thread(target=run_monitor, daemon=True)
                monitor_thread.start()
                _global_monitor_running = True
                log.info("Global browser monitoring thread started")
            except Exception as e:
                log.error(f"Failed to start monitoring thread: {str(e)}")


# 确保监控启动
ensure_monitor_running()


class Crewler:
    """
    Web crawler, specifically for crawling web content and screenshots
    Completely redesigned, no longer using the singleton pattern, each instance uses a separate Playwright
    """

    def __init__(self, workspace_path: str, headless: bool = HEADLESS):
        """
        Initialize the web crawler

        Args:
            workspace_path: The workspace path, used to save screenshots and content
        """
        self.workspace_path = Path(workspace_path)
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.playwright = None
        self.browser = None
        self.initialized = False
        self._default_timeout = 30000  # 默认超时时间，毫秒
        self.last_activity_time = time.time()
        self.headless = headless
        # 为每个实例生成唯一ID，用于日志跟踪
        self.instance_id = (
            f"crewler-{threading.get_ident()}-{random.randint(1000, 9999)}"
        )
        log.info(f"Create a new Crewler instance: {self.instance_id}")

        # 将实例添加到全局跟踪
        _active_scrapers.add(weakref.ref(self))

    async def initialize(self) -> None:
        """
        Initialize Playwright and browser
        Use the signal to control the maximum concurrency, add a timeout mechanism to prevent deadlocks
        """
        if self.initialized:
            return

        # 使用信号量控制并发数量，添加超时获取机制
        acquired = False
        try:
            acquired = browser_semaphore.acquire(blocking=False)
            if not acquired:
                log.info(
                    f"[{self.instance_id}] Waiting to acquire browser signal (current active: {MAX_CONCURRENT_BROWSERS - browser_semaphore._value})"
                )

                # 设置最大等待时间为30秒
                wait_start = time.time()
                max_wait_time = 30  # 30秒超时

                while not acquired and time.time() - wait_start < max_wait_time:
                    # 短暂等待后再次尝试
                    time.sleep(0.5)
                    acquired = browser_semaphore.acquire(blocking=False)

                # 如果超时仍未获取到信号量，记录警告并强制继续
                if not acquired:
                    log.warning(
                        f"[{self.instance_id}] Waiting for signal timeout ({max_wait_time} seconds), try to force release the signal"
                    )
                    # 强制释放一个信号量位置（可能导致并发数超过限制，但避免死锁）
                    try:
                        # 尝试重置信号量计数
                        current_value = browser_semaphore._value
                        if current_value <= 0:
                            # 此处可能有风险，但为避免死锁，强制增加一个信号量位置
                            browser_semaphore._value = 1
                            log.warning(
                                f"[{self.instance_id}] Force reset the signal value, original value: {current_value}, new value: 1"
                            )
                        acquired = True
                    except Exception as reset_error:
                        log.error(
                            f"[{self.instance_id}] Error resetting the signal value: {str(reset_error)}"
                        )
                        # 即使出错也继续，避免完全卡死
                        acquired = True
        except Exception as sem_error:
            log.error(
                f"[{self.instance_id}] Error acquiring the signal: {str(sem_error)}"
            )
            # 为避免彻底卡死，我们继续执行
            acquired = True

        try:
            # 使用独立的Playwright实例
            log.info(f"[{self.instance_id}] Start initializing Playwright and browser")
            self.playwright = await async_playwright().start()

            # 启动浏览器时使用更多优化选项
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
                    "--single-process",
                    "--no-zygote",  # 禁用zygote进程
                    "--no-first-run",  # 跳过首次运行检查
                    "--disable-extensions",  # 禁用扩展
                    "--disable-infobars",  # 禁用信息栏
                    "--mute-audio",  # 静音
                ],
            )
            self.initialized = True
            log.info(
                f"[{self.instance_id}] Playwright and browser initialized successfully"
            )
        except Exception as e:
            # 初始化失败，释放信号量
            if acquired:
                browser_semaphore.release()
            log.error(f"[{self.instance_id}] Failed to initialize Playwright: {str(e)}")
            # 确保资源被清理
            await self._cleanup_resources()
            raise e

    async def _cleanup_resources(self) -> None:
        """
        清理所有资源，确保在任何情况下都能释放信号量
        """
        resources_closed = False
        try:
            if self.browser:
                log.info(f"[{self.instance_id}] Close browser")
                try:
                    await self.browser.close()
                except Exception as e:
                    log.error(f"[{self.instance_id}] Error closing browser: {str(e)}")
                finally:
                    self.browser = None

            if self.playwright:
                log.info(f"[{self.instance_id}] Stop Playwright")
                try:
                    await self.playwright.stop()
                except Exception as e:
                    log.error(
                        f"[{self.instance_id}] Error stopping Playwright: {str(e)}"
                    )
                finally:
                    self.playwright = None

            self.initialized = False
            resources_closed = True
        finally:
            # 确保信号量被释放，即使资源清理失败
            if self.initialized or not resources_closed:
                log.warning(
                    f"[{self.instance_id}] Resources may not be fully cleaned up, force marking as not initialized"
                )
                self.initialized = False

            # 确保信号量被释放
            try:
                browser_semaphore.release()
                current_value = browser_semaphore._value
                log.info(
                    f"[{self.instance_id}] Release browser signal (current available: {current_value}/{MAX_CONCURRENT_BROWSERS})"
                )

                # 检查信号量值是否有异常（超过最大值）
                if current_value > MAX_CONCURRENT_BROWSERS:
                    log.warning(
                        f"[{self.instance_id}] Signal value is abnormal: {current_value}, reset to {MAX_CONCURRENT_BROWSERS}"
                    )
                    # 信号量值异常，重置为最大值
                    browser_semaphore._value = MAX_CONCURRENT_BROWSERS
            except Exception as e:
                log.error(f"[{self.instance_id}] Error releasing the signal: {str(e)}")
                # 紧急情况：重置信号量
                try:
                    browser_semaphore._value = MAX_CONCURRENT_BROWSERS
                    log.warning(
                        f"[{self.instance_id}] Emergency reset the signal value to {MAX_CONCURRENT_BROWSERS}"
                    )
                except:
                    pass

    async def scrape_url(
        self, url: str, index: int, dir: str, timeout: int | None = None
    ) -> str:
        """
        Scrape the content of the specified URL and save the screenshot
        """
        if timeout is None:
            timeout = self._default_timeout

        # 确保工作区目录存在
        workspace_dir = dir

        # 最大重试次数
        max_retries = MAX_RETRY_COUNT
        last_exception = None

        # 初始化Playwright和浏览器
        try:
            await self.initialize()
        except Exception as e:
            raise Exception(f"Failed to initialize Crewler: {str(e)}")

        # 添加递增的延迟，每次重试等待更长时间
        for retry_count in range(max_retries):
            context = None
            page = None

            try:
                # 如果不是第一次尝试，添加延迟
                if retry_count > 0:
                    delay = 2 * retry_count
                    log.info(
                        f"[{self.instance_id}] Try to scrape {url} for the {retry_count+1}/{max_retries} time, wait {delay} seconds before retrying"
                    )
                    await asyncio.sleep(delay)

                # 创建浏览器上下文和页面
                log.info(f"[{self.instance_id}] Create browser context for {url}")
                if not self.browser:
                    raise Exception("Browser not initialized")
                context = await self.browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    locale="zh-CN",  # 设置语言
                    timezone_id="Asia/Shanghai",  # 设置时区
                    device_scale_factor=1.0,  # 设备比例因子
                    is_mobile=False,  # 非移动设备
                    has_touch=False,  # 无触摸
                    java_script_enabled=True,  # 启用JavaScript
                )

                log.info(f"[{self.instance_id}] Create a new page for {url}")
                page = await context.new_page()

                # 设置页面超时
                page.set_default_timeout(timeout)
                page.set_default_navigation_timeout(timeout)

                # 导航到页面
                log.info(f"[{self.instance_id}] Start navigating to the page: {url}")
                try:
                    response = await page.goto(
                        url, timeout=timeout, wait_until="domcontentloaded"
                    )

                    if response and not response.ok:
                        raise Exception(f"HTTP错误! 状态码: {response.status}")
                except Exception as nav_error:
                    log.error(
                        f"[{self.instance_id}] Failed to navigate to the page (attempt {retry_count+1}/{max_retries}): {str(nav_error)}"
                    )
                    last_exception = nav_error
                    continue

                # 等待页面加载完成
                try:
                    log.info(f"[{self.instance_id}] Waiting for the page {url} to load")
                    await page.wait_for_load_state(
                        "domcontentloaded", timeout=timeout / 2
                    )
                except Exception as load_error:
                    log.error(
                        f"[{self.instance_id}] Failed to wait for the page {url} to load (attempt {retry_count+1}/{max_retries}): {str(load_error)}"
                    )
                    last_exception = load_error
                    continue

                # 获取页面内容
                try:
                    log.info(
                        f"[{self.instance_id}] Extract the content of the page {url}"
                    )
                    # content = await page.evaluate(
                    #     """() => {
                    #     // 移除脚本和样式元素
                    #     const scripts = document.getElementsByTagName("script");
                    #     const styles = document.getElementsByTagName("style");
                    #     for (let i = scripts.length - 1; i >= 0; i--) {
                    #         scripts[i].remove();
                    #     }
                    #     for (let i = styles.length - 1; i >= 0; i--) {
                    #         styles[i].remove();
                    #     }

                    #     // 获取文本内容
                    #     return document.body ? document.body.innerText : document.documentElement.innerText;
                    # }"""
                    # )
                    content = await function.clean_html(page)
                except Exception as eval_error:
                    log.error(
                        f"[{self.instance_id}] Failed to get the page content (attempt {retry_count+1}/{max_retries}): {str(eval_error)}"
                    )
                    last_exception = eval_error
                    continue

                # 保存截图
                try:
                    log.info(
                        f"[{self.instance_id}] Save the screenshot of the page {url}"
                    )
                    screenshot_path = os.path.join(
                        workspace_dir, f"screenshot_{index}.png"
                    )
                    await page.screenshot(
                        path=screenshot_path, full_page=True, timeout=timeout / 2
                    )
                except Exception as ss_error:
                    log.error(
                        f"[{self.instance_id}] Failed to save the screenshot (attempt {retry_count+1}/{max_retries}): {str(ss_error)}"
                    )
                    # 截图失败不会导致整个抓取失败

                # 成功抓取，返回内容
                log.info(f"[{self.instance_id}] Successfully scraped the page: {url}")
                return content

            except Exception as e:
                log.error(
                    f"[{self.instance_id}] An unhandled exception occurred during scraping (attempt {retry_count+1}/{max_retries}): {str(e)}"
                )
                last_exception = e

                # 如果是关闭通信管道的错误，尝试重新初始化浏览器
                if "the handler is closed" in str(e) or "connection is closed" in str(
                    e
                ):
                    log.warning(
                        f"[{self.instance_id}] Detected that the communication pipe is closed, will reinitialize the browser"
                    )
                    await self._cleanup_resources()
                    try:
                        await self.initialize()
                    except Exception as init_error:
                        log.error(
                            f"[{self.instance_id}] Failed to reinitialize the browser: {str(init_error)}"
                        )

            finally:
                # 确保资源被正确释放
                try:
                    if page:
                        log.info(f"[{self.instance_id}] Close the page {url}")
                        await page.close()
                except Exception as close_error:
                    log.error(
                        f"[{self.instance_id}] Failed to close the page {url}: {str(close_error)}"
                    )

                try:
                    if context:
                        log.info(f"[{self.instance_id}] Close the context {url}")
                        await context.close()
                except Exception as close_error:
                    log.error(
                        f"[{self.instance_id}] Failed to close the context {url}: {str(close_error)}"
                    )

        # 所有重试都失败，抛出最后一个异常
        if last_exception:
            error_msg = f"Failed to scrape URL {url} after multiple attempts: {str(last_exception)}"
            log.error(f"[{self.instance_id}] {error_msg}")
            raise Exception(error_msg)
        else:
            error_msg = f"Failed to scrape URL {url}, unknown reason"
            log.error(f"[{self.instance_id}] {error_msg}")
            raise Exception(error_msg)

    async def close(self):
        """
        关闭所有资源
        """
        log.info(f"[{self.instance_id}] Close Crewler")
        await self._cleanup_resources()

        # 从全局跟踪中移除自己
        self_ref = None
        for ref in _active_scrapers:
            if ref() is self:
                self_ref = ref
                break

        if self_ref:
            _active_scrapers.remove(self_ref)
            log.info(
                f"[{self.instance_id}] Removed from global tracking, current remaining scrapers: {len(_active_scrapers)}"
            )