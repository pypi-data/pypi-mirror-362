from asyncio import run

from x_model import init_db
from xync_schema import models

from xync_client.Abc.InAgent import BaseInAgentClient
from xync_client.Bybit.agent import AgentClient
from xync_client.Bybit.ws import prv
from xync_client.loader import PG_DSN


class InAgentClient(BaseInAgentClient):
    agent_client: AgentClient

    async def start_listen(self):
        t = await self.agent_client.ott()
        ts = int(float(t["time_now"]) * 1000)
        await prv(self.agent_client.actor.agent.auth["deviceId"], t["result"], ts, listen)

    # 3N: [T] - Уведомление об одобрении запроса на сделку
    async def request_accepted_notify(self) -> int: ...  # id


def listen(data: dict):
    print(data)


async def main():
    from xync_schema import TORM

    _ = await init_db(TORM, True)
    # pbot = PyroClient(bot)
    # await pbot.app.start()
    # await pbot.app.create_channel("tc")
    # await pbot.app.stop()

    actor = await models.Actor.filter(ex_id=9, agent__auth__isnull=False).prefetch_related("ex", "agent").first()
    cl: InAgentClient = actor.in_client()
    _ = await cl.start_listen()
    await cl.agent_client.close()


if __name__ == "__main__":
    run(main())
