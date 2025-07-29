from pyro_client.client.base import BaseClient, AuthTopic
from pyro_client.loader import TOKEN


class BotClient(BaseClient):
    def __new__(cls, bid: int | str) -> "BotClient":
        """
        :param bid: int | str - Если для такого bot_id в бд есть Session с его токеном в is_bot - можно просто id: int
        если нет - нужно передавать весь токен, что б Сессия в бд создалась.
        """
        if isinstance(bid, str):
            bid = int(bid.split(":")[0])
        return super().__new__(cls, bid)

    def __init__(self, bid: int | str):
        bt = isinstance(bid, str) and ":" in bid and bid
        super().__init__(bid, bot_token=bt or None)

    async def wait_auth_from(self, uid: int, topic: AuthTopic, past: int = 0, timeout: int = 60) -> str:
        return await super().wait_from(uid, topic, past, timeout)


async def main():
    from x_model import init_db
    from pyro_client.loader import TORM

    _ = await init_db(TORM, True)

    bc: BotClient = BotClient(6806432376)
    bc1: BotClient = BotClient(TOKEN)
    await bc.start()
    await bc1.start()
    await bc.stop()


if __name__ == "__main__":
    from asyncio import run

    run(main())
