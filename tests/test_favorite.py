from . import WikiBaseTestCase
from wiki.web.user import UserManager
from wiki.web.favorites import Favorites


class FavoriteTestCase(WikiBaseTestCase):
    """
        Various tests testing the favorites functionality
    """
    def test_add_favorite(self):
        """
            Make sure the add favorite works
        """
        manager = UserManager("hash", "tests")

        user = manager.get_user("testUser1")
        url = "testURL"
        title = "testTitle"
        favorite = Favorites()
        response = favorite.add_favorite(user.name, url, title)
        assert True(response)

    def test_get_favorites(self):
        """
            Make sure the get favorites works
        """
        manager = UserManager("hash", "tests")

        user = manager.get_user("testUser1")
        url = "testURL"
        title = "testTitle"
        favorite = Favorites()
        favorite.add_favorite(user.name, "test", "test")
        fav_pages = favorite.get_favorites(user.name)
        size = len(fav_pages)
        assert size > 0
