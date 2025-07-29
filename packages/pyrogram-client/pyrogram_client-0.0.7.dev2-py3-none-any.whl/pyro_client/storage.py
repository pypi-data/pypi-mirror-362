import time
from typing import Any

from pyrogram import raw, utils
from pyrogram.storage import Storage
from x_auth.enums import PeerType
from x_auth.models import Username, Version, Session, Peer, UpdateState


def get_input_peer(peer_id: int, access_hash: int, peer_type: PeerType):
    if peer_type in [PeerType.user, PeerType.bot]:
        return raw.types.InputPeerUser(user_id=peer_id, access_hash=access_hash)
    if peer_type == PeerType.group:
        return raw.types.InputPeerChat(chat_id=-peer_id)
    if peer_type in [PeerType.channel, PeerType.supergroup]:
        return raw.types.InputPeerChannel(channel_id=utils.get_channel_id(peer_id), access_hash=access_hash)
    raise ValueError(f"Invalid peer type: {peer_type.name}")


class PgStorage(Storage):
    VERSION = 1
    USERNAME_TTL = 30 * 24 * 3600
    session: Session
    sid: int

    async def open(self):
        self.sid = int(self.name)
        if not self.session:
            self.session = await Session[self.sid]

    async def save(self):
        await self.date(int(time.time()))

    async def close(self): ...

    async def delete(self):
        await Session.filter(id=self.sid).delete()

    async def update_peers(self, peers: list[tuple[int, int, str, str]]):
        for peer in peers:
            uid, ac_hsh, typ, phone = peer
            un, _ = await Username.update_or_create(phone and {"phone": phone}, id=uid)
            await Peer.update_or_create(
                {"username": un, "type": PeerType[typ], "phone_number": phone}, session_id=self.sid, id=ac_hsh
            )

    async def update_usernames(self, usernames: list[tuple[int, list[str]]]):
        for telegram_id, user_list in usernames:
            for username in user_list:
                await Username.update_or_create({"username": username}, id=telegram_id)

    async def get_peer_by_id(self, uid: int | str):
        if isinstance(uid, str):
            if uid.isnumeric():
                uid = int(uid)
            else:
                return await self.get_peer_by_username(uid)
        if not (peer := await Peer.get_or_none(session_id=self.sid, username_id=uid)):
            raise KeyError(f"Peer#{uid} not found")
        if peer.last_update_on:
            if abs(time.time() - peer.last_update_on.timestamp()) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {uid}")
        return get_input_peer(peer.username_id, peer.id, peer.type)

    async def get_peer_by_username(self, username: str):
        if not (peer := await Peer.get_or_none(session_id=self.sid, username__username=username)):
            if not (user := await Username.get_or_none(username=username)):
                raise KeyError(f"Username: {username} not found")
            return await self.get_peer_by_id(user.id)
        return get_input_peer(peer.username_id, peer.id, peer.type)

    async def update_state(self, value: tuple[int, int, int, int, int] = ...):
        if value is None:
            return await UpdateState.filter(session_id=self.sid)
        elif isinstance(value, int):
            await UpdateState.filter(session_id=self.sid, id=value).delete()
        else:
            sid, pts, qts, date, seq = value
            await UpdateState.get_or_create(
                {"pts": pts, "qts": qts, "date": date, "seq": seq}, session_id=self.sid, id=sid
            )

    async def get_peer_by_phone_number(self, phone_number: str):
        attrs = "id", "access_hash", "type"
        if not (peer := await Peer.get_or_none(session_id=self.sid, phone_number=phone_number).values_list(*attrs)):
            peer = await Peer.get(session_id=self.sid, username__phone=phone_number).values_list(*attrs)
        return get_input_peer(*peer)

    async def _get(self, attr: str):
        return await Session.get(id=self.sid).values_list(attr, flat=True)

    async def _set(self, attr: str, value):
        # if "__" in attr:
        #     table, attr = attr.split("__")
        #     rel = await self.session.__getattribute__(table)
        #     rel.__setattr__(attr, value)
        #     await rel.save()
        # else:
        await Session.update_or_create({attr: value}, id=self.sid)

    async def _accessor(self, attr: str, value: Any = ...):
        if value is ...:
            return await self._get(attr)
        # elif attr == ...:
        #     return await self._set(attr, ...)
        else:
            await self._set(attr, value)

    async def dc_id(self, value: int = ...):
        return await self._accessor("dc_id", value)

    async def api_id(self, value: int = ...):
        return await self._accessor("api_id", value)

    async def test_mode(self, value: bool = ...):
        return await self._accessor("test_mode", value)

    async def auth_key(self, value: bytes = ...):
        return await self._accessor("auth_key", value)

    async def date(self, value: int = ...):
        return await self._accessor("date", value)

    async def user_id(self, value: int = ...):
        return await self._accessor("user_id", value)

    async def is_bot(self, value: bool = ...):
        if value is not ...:
            value = self.session.is_bot if value else None  # dirty
        return bool(await self._accessor("is_bot", value))

    @staticmethod
    async def version(value: int = ...):
        if value is ...:
            ver = await Version.first()
            return ver.number
        else:
            await Version.update_or_create(id=value)
