from asyncio import Queue
from uuid import UUID, uuid4


class LynceusExchange(Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__uid: UUID = uuid4()

    def __str__(self):
        return f'LynceusExchange-{self.__uid}'
