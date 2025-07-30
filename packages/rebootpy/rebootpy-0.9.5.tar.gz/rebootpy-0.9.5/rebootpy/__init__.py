# -*- coding: utf-8 -*-
# flake8: noqa

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

__version__ = '0.9.5'

from .client import (BasicClient, Client, run_multiple, start_multiple,
                     close_multiple)
from .auth import (Auth, DeviceCodeAuth, ExchangeCodeAuth,
                   AuthorizationCodeAuth, DeviceAuth, RefreshTokenAuth,
                   AdvancedAuth)
from .friend import Friend, IncomingPendingFriend, OutgoingPendingFriend
from .message import FriendMessage, PartyMessage
from .party import (DefaultPartyConfig, DefaultPartyMemberConfig, PartyMember,
                    ClientPartyMember, Party,  ClientParty,
                    ReceivedPartyInvitation, SentPartyInvitation,
                    PartyJoinConfirmation, PartyJoinRequest, SquadAssignment,
                    PlaylistRequest)
from .presence import Presence, PresenceGameplayStats, PresenceParty
from .user import (ClientUser, User, BlockedUser, ExternalAuth,
                   UserSearchEntry, SacSearchEntryUser)
from .stats import StatsV2, StatsCollection, CompetitiveRank
from .enums import *
from .errors import *
from .store import Store, StoreItem
from. creative import CreativeIsland, CreativeIslandRating
from .news import BattleRoyaleNewsPost
from .playlist import Playlist
from .avatar import Avatar
from .http import HTTPRetryConfig, Route
from .utils import *
