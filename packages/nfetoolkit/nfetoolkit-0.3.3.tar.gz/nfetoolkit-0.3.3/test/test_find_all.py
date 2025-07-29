import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit.organizer import NFeOrganizer

class TestNFeToolkit(unittest.TestCase):

    def test_organize_xmls(self):

        nfe_organizer = NFeOrganizer()
        xml_list = nfe_organizer.find_all(os.getcwd())
        
        self.assertEqual(xml_list[0].name, 'canc.xml')

if __name__ == '__main__':
    unittest.main()