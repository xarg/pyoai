from unittest import TestCase, TestSuite, main, makeSuite
from fakeclient import FakeClient, GranularityFakeClient, TestError
import os
from datetime import datetime
from oaipmh import common, metadata, validation, error

directory = os.path.dirname(__file__)
fake42 = os.path.join(directory, 'fake42')
fakeclient = FakeClient(fake42)

fakeclient.getMetadataRegistry().registerReader(
    'oai_dc', metadata.oai_dc_reader)

class ResumptionTestCase(TestCase):
    def test_withoutToken(self):
        records = fakeclient.listRecords(metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 49)

    def test_withToken(self):
        records = fakeclient.listRecords(resumptionToken='84c35167b99e79',
                                         metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 25)

def test_suite():
    return TestSuite((makeSuite(ResumptionTestCase), ))

if __name__=='__main__':
    main(defaultTest='test_suite')

