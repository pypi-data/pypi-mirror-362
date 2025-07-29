import asyncio


def is_running_in_jupyter():
    """
    判断是否在 Jupyter 环境中运行

    Returns
    -------
    bool
    """
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook 或 JupyterLab
        elif shell == "TerminalInteractiveShell":
            return False  # 普通 IPython 终端
        else:
            return False  # 其他类型
    except (ImportError, NameError):
        return False  # 不是 IPython 环境


def run_async(coro):
    """
    同步方式运行协程程序

    Returns
    -------
    Any
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        # 已有事件循环（如Jupyter），用create_task
        task = asyncio.create_task(coro)
        return asyncio.get_event_loop().run_until_complete(task)
    else:
        # 没有事件循环
        return asyncio.run(coro)
