import re
from abc import ABC, abstractmethod


match_to_user_msg = re.compile( '<@(\w+)>' )
match_cmd = re.compile( '^\s*(\w+)' )
trim_leading_whitespace = re.compile( '^\s*' )
trim_trailing_whitespace = re.compile( '\s*$' )


class Handler:
    """Handles commands sent by the Router"""
    @abstractmethod
    def handle_mention( self, from_user, to_user, cmd, remaining_msg, channel ):
        """Called when the Router decides you should be the one to handle a message"""
        pass

class DefaultLastResortRouter( Handler ):
    """The Handler that gets hit by default when nothing else does"""
    def handle_mention( self, from_user, to_user, cmd, remaining_msg, channel ):
        # TODO message failure back to the user
        pass

class Router:
    """Takes registration of Handler objects, and routes to them when the command is hit"""
    def __init__( self ):
        self.last_resort_handler = DefaultLastResortRouter()
        self.cmds = {}

    def set_last_resort_handler( handler ):
        """Set the Handler that gets hit when nothing else matches"""
        self.last_resort_handler = handler

    def register( self, cmd, handler ):
        """Set a Handler to be hit when the given command string is made"""
        self.cmds[cmd] = handler

    def handle_mention( self, user, text, channel ):
        """When the bot user is mentioned, this gets called with the text of the chat"""
        to_user, cmd, remaining_msg = self._parse_msg( text )
        handler = self.cmds[cmd] if cmd in self.cmds else self.last_resort_handler
        handler.handle_mention( user, to_user, cmd, remaining_msg, channel )

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
