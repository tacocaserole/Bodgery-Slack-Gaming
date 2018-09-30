import re
from abc import ABC, abstractmethod


match_to_user_msg = re.compile( '<@(\w+)>' )
match_cmd = re.compile( '^\s*(\w+)' )
trim_leading_whitespace = re.compile( '^\s*' )
trim_trailing_whitespace = re.compile( '\s*$' )


class Handler:
    @abstractmethod
    def handle_mention( self, from_user, to_user, cmd, remaining_msg ):
        pass

class DefaultLastResortRouter( Handler ):
    def handle_mention( self, from_user, to_user, cmd, remaining_msg ):
        # TODO message failure back to the user
        pass

class Router:
    def __init__( self ):
        self.last_resort_handler = DefaultLastResortRouter()
        self.cmds = {}

    def set_last_resort_handler( handler ):
        self.last_resort_handler = handler
    def register( self, cmd, handler ):
        self.cmds[cmd] = handler

    def handle_mention( self, user, text, channel ):
        to_user, cmd, remaining_msg = self._parse_msg( text )
        handler = self.cmds[cmd] if cmd in self.cmds else self.last_resort_handler
        handler.handle_mention( user, to_user, cmd, remaining_msg )

    def _parse_msg( self, msg ):
        to_user_match = match_to_user_msg.search( msg )
        to_user = to_user_match.group(1) if to_user_match is not None else ""

        userless_msg = match_to_user_msg.sub( '', msg )
        cmd_match = match_cmd.search( userless_msg )
        cmd = cmd_match.group(1) if cmd_match is not None else ""
        remaining_msg = match_cmd.sub( '', userless_msg )
        remaining_msg = trim_leading_whitespace.sub( '', remaining_msg )
        remaining_msg = trim_trailing_whitespace.sub( '', remaining_msg )

        return to_user, cmd, remaining_msg
