# Asynctodon

Asyncio client for the Mastodon API

[Documentation](https://docs.barkshark.xyz/asynctodon)


## Example

Check [usage](https://docs.barkshark.xyz/asynctodon/src/usage.html) for a more complex example

```
import asyncio
import webbrowser

from asynctodon import Client


client = Client("example.com", "f4jl3f2309fj20fj02efj02efj")


async def main():
	status = await client.new_status("im gay")
	webbrowser.open(status.url)


asyncio.run(main())
```
