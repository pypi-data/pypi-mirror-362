from aiogram import Router
from aiogram.types import Message
from aiogram.filters import BaseFilter

class UserInDialog(BaseFilter):
    def __init__(self, dialog):
        self.dialog = dialog

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.dialog.users

class Dialog:
    def __init__(self, text, page, router: Router):
        self.text = text
        self.questions = []
        self.users = {}
        self.page = page

        @router.message(UserInDialog(self))
        async def on_msg(msg: Message):
            user = msg.chat.id

            self.users[user].args.append(msg.text)

            await msg.delete()
            await self.users[user].lastmsg.delete()

            try:
                if not await self.questions[len(self.users[user].args) - 1][1](msg, self.users[user].args):
                    del self.users[user].args[-1]
            except:
                del self.users[user].args[-1]
            
            try:
                self.users[user].lastmsg = await msg.answer(self.questions[len(self.users[user].args)][0])
            except:
                await self.cancel(msg)

    async def cancel(self, msg: Message):
        del self.users[msg.from_user.id]
        await self.page.func(msg, self.page.keyboard())

    def arg(self, text):
        def deco(func):
            self.questions.append((text, func))
        
            return func
        return deco

    async def start(self, msg: Message):
        da = DialogArgs(self, await msg.answer(self.questions[0][0]))
        self.users[msg.chat.id] = da

class DialogArgs:
    def __init__(self, dialog: Dialog, msg: Message):
        self.args = []
        self.lastmsg = msg