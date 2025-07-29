import abc


class AbstractService(abc.ABC):

    @abc.abstractmethod
    async def start(self) -> None: ...

    @abc.abstractmethod
    async def shutdown(self) -> None: ...
