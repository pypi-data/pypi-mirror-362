from types import TracebackType
import uuid
from nats.errors import TimeoutError
from nats.js.errors import KeyWrongLastSequenceError
from nats.js.kv import KeyValue, KV_DEL


class NatsKvLock:
    """An async, unfair, distributed lock that uses a Nats KV backend
    """

    def __init__(self, kv: KeyValue, lock_name: str):
        self.kv = kv
        self.lock_name = lock_name
        self.owner_id = str(uuid.uuid4())

        self._locked = False


    async def acquire(self, timeout: float | None = None):
        """Acquires a lock.

        Args:
            timeout (float | None, optional): An optional timeout. Defaults to None.

        Returns:
            bool: returns True on success, False if it could not acquire a lock in time
        """

        # TODO
        # - ttl can be simulated by checking if .create fails -> we should see if the existing key is out of date
        #   - this is problematic b/c two locks can have different ttls

        while True:
            try:
                await self.kv.create(self.lock_name, self.owner_id.encode())
                self._locked = True
                return True
            except KeyWrongLastSequenceError:
                watcher = await self.kv.watch(self.lock_name) # type: ignore

                while True:
                    try:
                        event = await watcher.updates(timeout=timeout) # type: ignore

                        if event is None:
                            # first call
                            continue
                        
                        if event.operation == KV_DEL:
                            # key was deleted - we should try and create a key
                            await watcher.stop()
                            break
                    except TimeoutError:
                        await watcher.stop()
                        return False

    async def release(self):
        """Releases the lock
        """
        if not self._locked:
            return

        try:
            entry = await self.kv.get(self.lock_name)
            if entry.value is not None and entry.value.decode() == self.owner_id:
                await self.kv.delete(self.lock_name)
        finally:
            self._locked = False

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None):
        await self.release()

