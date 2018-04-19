from . import WikiBaseTestCase
from wiki.web import get_users


class UserContentTestCase(WikiBaseTestCase):
    """
        Various test cases around user content.
    """
    def test_user_available(self):
        """
            Assert that users are present
        """
        users = get_users()
        assert users != {}
