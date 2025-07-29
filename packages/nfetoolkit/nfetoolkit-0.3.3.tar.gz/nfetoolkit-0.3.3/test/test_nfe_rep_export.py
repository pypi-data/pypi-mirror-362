import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit.handler import NFeHandler
from nfetoolkit.repository import NFeRepository
from nfetoolkit.organizer import NFeOrganizer

class TestNFeRepExport(unittest.TestCase):
           
    def test_rep(self):
        
        nfe_rep = NFeRepository()
        
        for xml in NFeOrganizer.find_all("."):
            
            match (NFeHandler.xml_type(xml)):
                case 'nfe_type':
                    nfe_rep.store_nfe(NFeHandler.nfe_from_path(xml))
                case 'canc_type':
                    nfe_rep.store_evt(NFeHandler.evento_canc_from_path(xml))
                case 'cce_type':
                    nfe_rep.store_evt(NFeHandler.evento_cce_from_path(xml))

        with open('nfe_data.txt', 'w') as file:
            nfe_rep.write_to(file)
            
        self.assertIsNotNone(str(nfe_rep))
        
if __name__ == '__main__':
    unittest.main()