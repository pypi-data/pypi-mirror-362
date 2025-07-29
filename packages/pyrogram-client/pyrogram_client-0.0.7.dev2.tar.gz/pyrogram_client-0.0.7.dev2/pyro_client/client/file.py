from io import BytesIO

from pyrogram.raw.functions.messages import UploadMedia
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import (
    MessageMediaDocument,
    InputMediaUploadedDocument,
    InputPeerSelf,
    MessageMediaPhoto,
    InputMediaUploadedPhoto,
    InputDocumentFileLocation,
    InputPhotoFileLocation,
)
from pyrogram.raw.types.upload import File
from pyrogram.types import Message

from pyro_client.client.bot import BotClient


class FileClient(BotClient):
    @staticmethod
    def ref_enc(ph_id: int, access_hash: int, ref: bytes) -> bytes:
        return ph_id.to_bytes(8, "big") + access_hash.to_bytes(8, "big", signed=True) + ref

    @staticmethod
    def ref_dec(full_ref: bytes) -> tuple[int, int, bytes]:
        pid, ah = int.from_bytes(full_ref[:8], "big"), int.from_bytes(full_ref[8:16], "big", signed=True)
        return pid, ah, full_ref[16:]

    async def save_doc(self, byts: bytes, ctype: str) -> tuple[MessageMediaDocument, bytes]:
        in_file = await self.save_file(BytesIO(byts))
        imud = InputMediaUploadedDocument(file=in_file, mime_type=ctype, attributes=[])
        upf: MessageMediaDocument = await self.invoke(UploadMedia(peer=InputPeerSelf(), media=imud))
        return upf, (
            upf.document.id.to_bytes(8, "big")
            + upf.document.access_hash.to_bytes(8, "big", signed=True)
            + upf.document.file_reference
        )

    async def save_photo(self, file: bytes) -> tuple[MessageMediaPhoto, bytes]:
        in_file = await self.save_file(BytesIO(file))
        upm = UploadMedia(peer=InputPeerSelf(), media=InputMediaUploadedPhoto(file=in_file))
        upp: MessageMediaPhoto = await self.invoke(upm)
        return upp, self.ref_enc(upp.photo.id, upp.photo.access_hash, upp.photo.file_reference)

    async def get_doc(self, fid: bytes) -> File:
        pid, ah, ref = self.ref_dec(fid)
        loc = InputDocumentFileLocation(id=pid, access_hash=ah, file_reference=ref, thumb_size="x")
        return await self.invoke(GetFile(location=loc, offset=0, limit=512 * 1024))

    async def get_photo(self, fid: bytes, st: str) -> File:
        pid, ah, ref = self.ref_dec(fid)
        loc = InputPhotoFileLocation(id=pid, access_hash=ah, file_reference=ref, thumb_size=st)
        return await self.invoke(GetFile(location=loc, offset=0, limit=512 * 1024))

    async def bot_got_msg(self, _, msg: Message):
        if state := self.storage.session.state.pop("bot", None):
            self.storage.session.state[state] = msg.text
