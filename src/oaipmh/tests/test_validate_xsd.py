from unittest import TestCase, TestSuite, main, makeSuite
from fakeclient import FakeClient, GranularityFakeClient, TestError
import os
from datetime import datetime
from oaipmh import common, metadata, validation, error

directory = os.path.dirname(__file__)
fake1 = os.path.join(directory, 'fake6')
fakeclient = FakeClient(fake1)

fakeclient.getMetadataRegistry().registerReader(
    'oai_dc', metadata.oai_dc_reader)

class ClientTestCase(TestCase):

    def test_validate_xsd(self):
        #valid documents
        for i in range(7):
            test_document("../fake1/0000"+str(i)+".xml")
        #broken xml
        self.assertRaises(error.XMLSyntaxError,test_document,"00001.xml")
        #empty header
        self.assertRaises(error.XMLValidationError,test_document,"00002.xml")
        #no request tag
        self.assertRaises(error.XMLValidationError,test_document,"00000.xml")
        #no <datestamp> in header
        self.assertRaises(error.XMLValidationError,test_document,"00003.xml")

def test_document(filepath):
    xml = open(os.path.join(directory,"fake6/"+filepath))
    try:
        tree = fakeclient.parse(xml.read())
    except SyntaxError, e:
        raise error.XMLSyntaxError(e)
    xml.close()
    #check XSD validity
    try:
        fakeclient._xmlschema.assertValid(tree)
    except Exception, e:
        raise error.XMLValidationError    
                
def test_suite():
    return TestSuite((makeSuite(ClientTestCase), ))

if __name__=='__main__':
    main(defaultTest='test_suite')
