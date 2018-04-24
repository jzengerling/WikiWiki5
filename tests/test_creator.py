from wiki import *
import creator_module

class PageHasCreatorTestCase(WikiBaseTestCase):

    def test_page_has_creator(self):
        """
            Assert that given page has a json entry that isn't empty
        """
        data = creator_module.get_page_data('colton')
        assert data
        
    def test_search_page(self):
        """
            Assert that pages matching creator's name exists
        """
        pages = self.index()
        regex = re.compile('nick', re.IGNORECASE if ignore_case else 0)
        matched = []
        matched = creator_module.search_by_creator(pages, regex)
        assert matched
        
        