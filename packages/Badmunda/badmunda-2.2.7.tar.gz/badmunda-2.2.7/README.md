<p align="center">
    <a href="https://gitlab.com/Badmunda98/Bad">
        <img src="https://files.catbox.moe/4z3iiu.png" alt="Badmunda" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://gitlab.com/Badmunda98/Bad">
        Homepage
    </a>
    •
    <a href="https://t.me/PBX_UPDATE">
        Updates
    </a>
    •
    <a href="https://t.me/PBX_CHAT">
        Chat
    </a>
</p>

## Badmunda

> [!NOTE]
> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots.

```python
from Badmunda import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Badmunda!")


app.run()



#Installing

Stable version
``pip3 install Badmunda``

Dev version
``pip3 install git+https://gitlab.com/Badmunda98/Bad.git --force-reinstall``