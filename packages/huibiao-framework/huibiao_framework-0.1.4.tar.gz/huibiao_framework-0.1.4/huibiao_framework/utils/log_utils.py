import os

from loguru import logger


class LoguruSetup:
    @staticmethod
    def save_to_file(
        service_name: str,
        log_dir: str,
        *,
        add_pid_suffix: bool = True,
        max_size_mb: int = 100,
    ):
        os.makedirs(log_dir, exist_ok=True)
        pid_suffix = f"_{os.getpid()}" if add_pid_suffix else ""

        # 配置 INFO 及以上级别日志
        logger.add(
            os.path.join(log_dir, f"{service_name}_info{pid_suffix}.log"),
            rotation=f"{max_size_mb} MB",
            filter=lambda record: record["level"].no >= 20,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {process} | {message}",
            enqueue=True,
        )

        # 配置 DEBUG 级别日志
        logger.add(
            os.path.join(log_dir, f"{service_name}_debug{pid_suffix}.log"),
            rotation=f"{max_size_mb} MB",
            level="DEBUG",
            filter=lambda record: record["level"].no >= 10,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            enqueue=True,
        )
