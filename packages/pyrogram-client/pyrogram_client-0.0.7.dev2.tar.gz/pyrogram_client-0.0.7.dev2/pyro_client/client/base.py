import asyncio
from collections import OrderedDict
from io import BytesIO
from typing import Literal

from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, Unauthorized
from pyrogram.filters import chat, contact, AndFilter
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from x_auth.models import Session, App, Username

from pyro_client.storage import PgStorage

AuthTopic = Literal["phone", "code", "pass"]


class BaseClient(Client):
    storage: PgStorage
    uid: int = None

    _insts: dict[int, "BaseClient"] = {}

    def __new__(cls, uid: int, *args, **kwargs):
        """Single client for each uid"""
        cls.uid = uid
        if uid not in cls._insts:
            cls._insts[uid] = Client.__new__(cls)
        return cls._insts[uid]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "name"):
            name = str(self.uid)
            super().__init__(name, storage_engine=PgStorage(name), **kwargs)  # , workers=2

    async def preload(self):
        if not (session := await Session.get_or_none(id=self.uid).prefetch_related("api")):
            app = await App[20373304]
            username, _ = await Username.get_or_create(id=self.uid)
            bt = self.bot_token and self.bot_token.split(":")[1]
            session = await Session.create(id=self.uid, api=app, user=username, is_bot=bt)
            self.api_id = app.id
            self.api_hash = app.hsh
            await session.fetch_related("api")
        self.storage.session = session

    async def start(self, use_qr: bool = False, except_ids: list[int] = None):
        if not self.is_connected:
            await self.preload()
            try:
                return await super().start(use_qr=use_qr, except_ids=except_ids or [])
            except (AuthKeyUnregistered, Unauthorized) as e:
                await self.storage.session.delete()
                raise e
        return self

    async def send(
        self,
        txt: str,
        uid: int | str = "me",
        btns: list[InlineKeyboardButton | KeyboardButton] = None,
        photo: bytes = None,
        video: bytes = None,
    ) -> Message:
        ikm = (
            (
                InlineKeyboardMarkup([btns])
                if isinstance(btns[0], InlineKeyboardButton)
                else ReplyKeyboardMarkup([btns], one_time_keyboard=True)
            )
            if btns
            else None
        )
        if photo:
            return await self.send_photo(uid, BytesIO(photo), txt, reply_markup=ikm)
        elif video:
            return await self.send_video(uid, BytesIO(video), txt, reply_markup=ikm)
        else:
            return await self.send_message(uid, txt, reply_markup=ikm)

    async def wait_from(self, uid: int, topic: str, past: int = 0, timeout: int = 10) -> str | None:
        fltr = chat(uid)
        if topic == "phone":
            fltr &= contact
        handler = MessageHandler(self.got_msg, fltr)
        # handler, g = self.add_handler(handler, 1)
        g = 0
        if g not in self.dispatcher.groups:
            self.dispatcher.groups[g] = []
            self.dispatcher.groups = OrderedDict(sorted(self.dispatcher.groups.items()))
        self.dispatcher.groups[g].append(handler)
        self.storage.session.state |= {uid: {"waiting_for": topic}}
        #
        while past < timeout:
            if txt := self.storage.session.state.get(uid, {}).pop(topic, None):
                # self.remove_handler(handler)
                self.dispatcher.groups[g].remove(handler)
                #
                return txt
            await asyncio.sleep(1)
            past += 1
        return self.remove_handler(handler, g)

    async def got_msg(self, _, msg: Message):
        if tpc := self.storage.session.state.get(msg.from_user.id, {}).pop("waiting_for", None):
            self.storage.session.state[msg.from_user.id][tpc] = msg.contact.phone_number if tpc == "phone" else msg.text

    def rm_handler(self, uid: int):
        for gi, grp in self.dispatcher.groups.items():
            [self.remove_handler(h, gi) for h in grp if isinstance(h.filters, AndFilter) and uid in h.filters.base]
