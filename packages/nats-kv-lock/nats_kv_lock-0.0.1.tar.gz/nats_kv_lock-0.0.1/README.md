# nats-kv-lock
A simple, distributed lock using NATS.io

### Note!

- This is a simple PoC and perhaps shouldn't be used in a production environment
- This does NOT guarantee order, i.e. it is an unfair lock.

## Installation

Assuming you already have NATS installed, you can simply `pip install nats-kv-lock`


## Example

All you need to do is create a KV bucket, then initialize an instance of `NatsKvLock` using that bucket with a shared `lock_name`.

```python
import asyncio

from nats import connect
from nats_kv_lock import NatsKvLock

async def main():
    print('connecting...')
    nc = await connect()
    print('connected!')
    
    js = nc.jetstream()
    try:
        kv = await js.key_value(bucket='my_locks')
    except:
        kv = await js.create_key_value(bucket='my_locks')
    
    my_lock = NatsKvLock(kv, 'my_lock')

    print('acquiring lock...')
    
    async with my_lock:
        print('acquired! doing work...')
        await asyncio.sleep(10)
        print('releasing lock...')

    print('released lock!')

if __name__ == '__main__':
    asyncio.run(main())
```