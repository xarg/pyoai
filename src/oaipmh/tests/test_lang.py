from unittest import TestCase, TestSuite, main, makeSuite
from fakeclient import FakeClient, GranularityFakeClient, TestError
import os
from datetime import datetime
from oaipmh import metadata

directory = os.path.dirname(__file__)
fake8 = os.path.join(directory, 'fake8')
fakeclient = FakeClient(fake8)

fakeclient.getMetadataRegistry().registerReader(
    'oai_dc', metadata.oai_dc_reader)

class LangTestCase(TestCase):
    
    def test_lang_absent(self):
        records = fakeclient.listRecords(from_=datetime(2003, 04, 10),
                                         metadataPrefix='oai_dc')
        records = list(records)
        # lazy, just test first one
        header, metadata, about = records[0][0]
        m = metadata._map
        self.assertFalse(m.has_key('description:es'))
        self.assertFalse(m.has_key('description:en'))
        self.assertFalse(m.has_key('description:fr'))
        self.assertFalse(m.has_key('subject:es'))
        self.assertFalse(m.has_key('subject:en'))
        self.assertFalse(m.has_key('subject:fr'))
        self.assertFalse(m.has_key('language:fr'))
        self.assert_(m.has_key('language'))

    def test_lang_present(self):
        records = fakeclient.listRecords(from_=datetime(2003, 04, 11),
                                         metadataPrefix='oai_dc')
        records = list(records)
        # lazy, just test first one
        header, metadata, about = records[0][0]
        m = metadata._map
        self.assert_(m.has_key('description:es'))
        self.assert_(m.has_key('description:en'))
        self.assert_(m.has_key('description:fr'))
        self.assert_(m.has_key('subject:es'))
        self.assert_(m.has_key('subject:en'))
        self.assert_(m.has_key('subject:fr'))
        self.assertFalse(m.has_key('language:fr'))
        self.assert_(m.has_key('language'))
            
def test_suite():
    return TestSuite((makeSuite(LangTestCase), ))

if __name__=='__main__':
    main(defaultTest='test_suite')

