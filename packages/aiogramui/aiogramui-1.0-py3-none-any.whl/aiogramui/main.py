from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .dialog import *
from .button import *

router = 0
def init(r):
    global router

    router = r

class Root:
    cqs = []

    def __init__(self, text, backtext, back=False, allow=[]):
        self.text = text
        self.backtext = backtext
        self.back = back
        self.allow = allow

        self.local = []
        if not back:
            Root.cqs.append(self)
    
    def page(self, text, allow=[]):
        root = Root(text, self.backtext, back=self, allow=allow)

        Root.cqs.append(root)
        self.local.append(root)

        return root
    
    def dialog(self, text):
        dialog = Dialog(text, self, router)

        Root.cqs.append(dialog)
        self.local.append(dialog)

        return dialog
    
    def button(self, text):
        button = Button(text)

        Root.cqs.append(button)
        self.local.append(button)

        return button

    def keyboard(self, user=None, adjust=2):
        k = InlineKeyboardBuilder()

        for i in self.local:
            if getattr(i, 'allow', None) and user:
                if user not in i.allow:
                    continue
            
            k.button(
                text=i.text,
                callback_data=str(Root.cqs.index(i))
            )
        
        if self.back:
            k.button(
                text=self.backtext,
                callback_data=str(Root.cqs.index(self.back))
            )

        k.adjust(adjust)
        
        return k
    
    def generate_doc(self):
        txt = f'{self.text} - {self.func.__doc__}' if self.func.__doc__ else self.text
        for i in self.local:
            if not isinstance(i, Root):
                txt += f'\n    {i.text}'
            else:
                if i.allow:
                    continue
                for j in i.generate_doc().split('\n'):
                    txt += f'\n    {j}'
        
        return txt
    
    def __call__(self, func):
        self.func = func

        return func

def register():
    async def handler(cq: CallbackQuery):
        element = Root.cqs[int(cq.data)]
        msg = cq.message

        tp = type(element)

        if tp == Dialog:
            await msg.delete()
            await element.start(msg)
        elif tp == Button:
            await element.func(cq)
        elif tp == Root:
            await msg.delete()
            await element.func(msg, element.keyboard())

    router.callback_query.register(handler)