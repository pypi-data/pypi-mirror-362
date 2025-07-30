# arachnid-shield-sdk
An SDK for consuming the Arachnid Shield API.

## Installation

```sh
pip install arachnid-shield-sdk
```

## Usage

First, obtain login credentials by contacting [Project Arachnid](https://shield.projectarachnid.com/). 

This client acts simply as a global resource that may live as long as your application. So you may use it in different ways.

### Vanilla Python (Sync)

You may use the `ArachnidShield` client that has all the methods needed to consume the Arachnid Shield API.

```python
from arachnid_shield_sdk import ArachnidShield

shield = ArachnidShield(username="", password="")
    
def process_media(contents):

    scanned_media = shield.scan_media_from_bytes(contents, "image/jpeg")
    if scanned_media.matches_known_image:
        print(f"harmful media found!: {scanned_media}")
    ... 


def main():
    
    with open("some-image.jpeg", "rb") as f:
        contents = f.read()
    
    process_media_for_user(contents)


if __name__ == '__main__':
    main()

```

### Vanilla Python (Async)

In `async` environments, you may use the `ArachnidShieldAsync` client which has the exact same interface as the `ArachnidShield` client but where all the methods are awaitable coroutines.

```python
import asyncio
from arachnid_shield_sdk import ArachnidShieldAsync as ArachnidShield

shield = ArachnidShield(username="", password="")

async def process_media(contents):

    scanned_media = await shield.scan_media_from_bytes(contents, "image/jpeg")
    if scanned_media.matches_known_image:
        print(f"harmful media found!: {scanned_media}")
    ... 


async def main():
    with open("some-image.jpeg", "rb") as f:
        contents = f.read()
    await process_media(contents)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

```
