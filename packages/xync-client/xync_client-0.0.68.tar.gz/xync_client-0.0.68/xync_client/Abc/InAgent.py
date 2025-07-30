from abc import abstractmethod

from xync_schema.models import Actor

from xync_client.Abc.Agent import BaseAgentClient


class BaseInAgentClient:
    def __init__(self, actor: Actor):
        self.agent_client: BaseAgentClient = actor.client()

    @abstractmethod
    async def start_listen(self) -> bool: ...

    # 3N: [T] - Уведомление об одобрении запроса на сделку
    @abstractmethod
    async def request_accepted_notify(self) -> int: ...  # id
