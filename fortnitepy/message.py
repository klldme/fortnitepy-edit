# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019-2021 Terbau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .client import Client
    from .friend import Friend
    from .party import ClientParty, PartyMember


class MessageBase:

    __slots__ = ('_client', '_author', '_content', '_created_at')

    def __init__(self, client: 'Client',
                 author: Union['Friend', 'PartyMember'],
                 content: str) -> None:
        self._client = client
        self._author = author
        self._content = content
        self._created_at = datetime.datetime.utcnow()

    @property
    def client(self) -> 'Client':
        """:class:`Client`: The client."""
        return self._client

    @property
    def author(self) -> 'Friend':
        """:class:`Friend`: The author of the message."""
        return self._author

    @property
    def content(self) -> str:
        """:class:`str`: The content of the message."""
        return self._content

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: The time of when this message was
        received in UTC.
        """
        return self._created_at


class FriendMessage(MessageBase):

    __slots__ = MessageBase.__slots__

    def __init__(self, client: 'Client',
                 author: 'Friend',
                 content: str) -> None:
        super().__init__(client, author, content)

    def __repr__(self) -> str:
        return ('<FriendMessage author={0.author!r} '
                'created_at={0.created_at!r}>'.format(self))

    async def reply(self, content: str) -> None:
        """|coro|

        Replies to the message with the given content.

        Parameters
        ----------
        content: :class:`str`
            The content of the message
        """
        return await self.author.send(content)


class PartyMessage(MessageBase):

    __slots__ = MessageBase.__slots__ + ('party',)

    def __init__(self, client: 'Client',
                 party: 'ClientParty',
                 author: 'PartyMember',
                 content: str) -> None:
        super().__init__(client, author, content)
        self.party = party

    def __repr__(self) -> str:
        return ('<PartyMessage party={0.party!r} author={0.author!r} '
                'created_at={0.created_at!r}>'.format(self))

    @property
    def author(self) -> 'PartyMember':
        """:class:`PartyMember`: The author of a message."""
        return self._author

    async def reply(self, content: str) -> None:
        """|coro|

        Replies to the message with the given content.

        Parameters
        ----------
        content: :class:`str`
            The content of the message
        """
        return await self.party.send(content)
