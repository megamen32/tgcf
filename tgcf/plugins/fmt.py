import logging
import traceback
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from telethon.tl.types import ReactionCount

from tgcf.plugin_models import Format, Style
from tgcf.plugins import TgcfMessage, TgcfPlugin

STYLE_CODES = {"bold": "**", "italics": "__", "code": "`", "strike": "~~", "plain": "",'forward':"%author%"}


class TgcfFmt(TgcfPlugin):
    id_ = "fmt"

    def __init__(self, data) -> None:
        self.format = data
        logging.info(self.format)

    def modify(self, tm: TgcfMessage) -> TgcfMessage:
        if self.format.style is Style.PRESERVE:
            return tm
        msg_text: str = tm.raw_text
        if not msg_text and self.format.style!='forward':
            return tm
        style = STYLE_CODES.get(self.format.style)

        author_name=''
        try:
            author_name = f"@{tm.message.sender.username} "
            author_name+=f"{tm.message.sender.first_name or ''} {tm.message.sender.last_name or ''} :"
        except:pass
        def reacount(item:ReactionCount):
            text=f'{item.count}{item.reaction.emoticon}'
            return text

        if tm.message.reactions is not None:
            reactions ='\n'+ ', '.join(list(map(reacount, tm.message.reactions.results)))
        else:
            reactions = ''
        tm.text = f"{style}{msg_text}{style}".replace('%author%',author_name,1).replace('%author%', reactions)
        return tm
