from unittest import TestCase, TestSuite, main, makeSuite
from fakeclient import FakeClient, GranularityFakeClient, TestError
import os
from datetime import datetime
from oaipmh import common, metadata, validation, error

directory = os.path.dirname(__file__)
fake43 = os.path.join(directory, 'fake43')
fakeclient = FakeClient(fake43)

fakeclient.getMetadataRegistry().registerReader(
    'oai_dc', metadata.oai_dc_reader)

class SetSpecTestCase(TestCase):
    """
    test_wSPwRT = test _w_ithout _s_et_S_pec, _w_ithout _r_esumption_T_oken
    test_SPRT = test with _s_et_S_pec, with _r_esumption_T_oken
    """
    def test_wSPwRT(self):
        records = fakeclient.listRecords(metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 200)
        self.assertEqual(records[0][0][1]._map['date'][0], u'2009')

    def test_wSPRT(self):
        records = fakeclient.listRecords(
                            resumptionToken=',,,oai_dc,100',
                            metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 100)
        self.assertEqual(records[0][0][1]._map['date'][0], u'2008')

    def test_SPwRT(self):
        records = fakeclient.listRecords(
                            setSpec='san:052:CULARB:02',
                            metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 200)
        self.assertEqual(records[0][0][1]._map['date'][0], u'2009')

    def test_SPRT(self):
        records = fakeclient.listRecords(
                            resumptionToken=',,san:052:CULARB:02,oai_dc,100',
                            metadataPrefix='oai_dc')
        records = list(records)
        self.assertEqual(len(records), 100)
        self.assertEqual(records[0][0][1]._map['date'][0], u'1974')

def test_suite():
    return TestSuite((makeSuite(SetSpecTestCase), ))

if __name__=='__main__':
    main(defaultTest='test_suite')


