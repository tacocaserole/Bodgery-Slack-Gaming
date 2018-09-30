import unittest
import mentionrouter


class MockHandler( mentionrouter.Handler ):
    def __init__( self, test ):
        self.test = test
        self.last_seen_from_user = None
        self.last_seen_to_user = None
        self.last_seen_cmd = None
        self.last_seen_remaining_msg = None

    def handle_mention( self, from_user, to_user, cmd, remaining_msg ):
        self.last_seen_from_user = from_user
        self.last_seen_to_user = to_user
        self.last_seen_cmd = cmd
        self.last_seen_remaining_msg = remaining_msg
 
class TestMentionRouter(unittest.TestCase):
    '''routes messages to callbacks based on mentions'''
    def test_mentions(self):
        handler = MockHandler( self )
        last_resort_handler = MockHandler( self )
        router = mentionrouter.Router()
        router.register( "test_cmd", handler )
        router.last_resort_handler = last_resort_handler

        router.handle_mention(
            user = "U3658AB",
            text = "<@U27438XF> test_cmd do thing",
            channel = "C0LATF2Q",
        )
        self.assertEqual( handler.last_seen_from_user, "U3658AB",
            "Passed from_user" );
        self.assertEqual( handler.last_seen_to_user, "U27438XF",
            "Passed to_user" );
        self.assertEqual( handler.last_seen_cmd, "test_cmd",
            "Passed cmd" );
        self.assertEqual( handler.last_seen_remaining_msg, "do thing",
            "Passed remaining msg" );
        self.assertIsNone( last_resort_handler.last_seen_cmd,
            "Did not hit last resort handler" )

        router.handle_mention(
            user = "U3658AB",
            text = "<@U27438XF> bad_cmd do thing",
            channel = "C0LATF2Q",
        )
        self.assertEqual( handler.last_seen_cmd, "test_cmd",
            "Did not hit test_cmd handler" )
        self.assertEqual( last_resort_handler.last_seen_cmd, "bad_cmd",
            "Hit last resort handler" )

        router.handle_mention(
            user = "U3658AB",
            text = "test_cmd <@U27438XF> do other thing",
            channel = "C0LATF2Q",
        )
        self.assertEqual( handler.last_seen_remaining_msg, "do other thing",
            "Handle alternative formatting" )

   
if __name__ == '__main__':
    unittest.main()
