import logging

from binance import Client
from rich.logging import RichHandler

from cryptoservice.exceptions import MarketDataError

# 设置 rich logger
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


class BinanceClientFactory:
    """Binance客户端工厂类."""

    _instance: Client | None = None

    @classmethod
    def create_client(cls, api_key: str, api_secret: str) -> Client:
        """创建或获取Binance客户端实例（单例模式）

        Args:
            api_key: API密钥
            api_secret: API密钥对应的secret

        Returns:
            Client: Binance客户端实例

        Raises:
            MarketDataError: 当客户端初始化失败时抛出
        """
        if not cls._instance:
            try:
                if not api_key or not api_secret:
                    raise ValueError("Missing Binance API credentials")
                cls._instance = Client(api_key, api_secret)
                logger.info("[green]Successfully created Binance client[/green]")
            except Exception as e:
                logger.error(f"[red]Failed to initialize Binance client: {e}[/red]")
                raise MarketDataError(f"Failed to initialize Binance client: {e}") from e
        return cls._instance

    @classmethod
    def get_client(cls) -> Client | None:
        """获取现有的客户端实例."""
        return cls._instance

    @classmethod
    def reset_client(cls) -> None:
        """重置客户端实例."""
        cls._instance = None
