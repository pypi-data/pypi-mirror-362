[![PyPI version](https://badge.fury.io/py/aiogramui.svg)](https://pypi.org/project/aiogramui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# aiogramui
✨ A minimalistic UI framework for aiogram bots.

## Contents

- [Installation](#installation)
- [Features](#features)
  - [Building menu](#building-menu)
  - [Adding buttons and dialogs](#adding-buttons-and-dialogs)
  - [Generating doc](#generating-doc)
- [Pro tips](#pro-tips)

## Installation
1. Via pip
```bash
pip install aiogramui
```
2. Using git
```bash
git clone https://github.com/evryoneowo/aiogramui && cd aiogramui
pip install .
```

## Features
### Building menu
```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogramui import init, Root, register

router = Router()

init(router)

start = Root('Start', backtext='back')
wallet = start.page('Wallet')

@start
@router.message(Command('start'))
async def on_start(msg: Message, keyboard=None):
    await msg.answer('Start page', reply_markup=start.keyboard().as_markup())

@wallet
async def on_wallet(msg: Message, keyboard):
    await msg.answer('Wallet page', reply_markup=keyboard.as_markup())

register()
```

### Adding buttons and dialogs
```python
from aiogram.types import CallbackQuery

helloworld = start.button('HelloWorld')

@helloworld
async def on_helloworld(cq: CallbackQuery):
    await cq.message.answer('Hello, world!')
```

```python
helloname = start.dialog('HelloName')

@helloname.arg('Enter your name:')
async def on_helloname(msg: Message, args):
    await msg.answer(f'Hello, {args[0]}!')

    return True
```

### Generating doc
```python
doc = start.generate_doc()
```

## Pro tips
### Cancel and repeat in dialogs
```python
password = start.dialog('Password')

@password.arg('Enter the password:')
async def on_password(msg: Message, args):
    if args[0] != '1234': return # <- If user entered not valid password then it will ask him again.

    await msg.answer('Right!')
    
    return True
```

```python
password = start.dialog('Password')

@password.arg('Enter the password:')
async def on_password(msg: Message, args):
    if args[0] != '1234': await password.cancel(msg) # <- If user entered not valid password then it will cancel dialog.

    await msg.answer('Right!')
    
    return True
```

### Pages only for allowed users
```python
admins = [123, 321]

admin = start.page('Admin', allow=admins)

@admin
async def on_admin(msg: Message, keyboard):
    await msg.answer('Admin page', reply_markup=keyboard.as_markup())
```

> [!WARNING]
> If you show a page only for allowed users, then you must get keyboard manually with `user` arg in parent page.