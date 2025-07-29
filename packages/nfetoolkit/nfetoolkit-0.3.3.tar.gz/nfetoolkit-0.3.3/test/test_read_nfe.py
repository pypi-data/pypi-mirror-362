import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit.handler import NFeHandler

class TestReadNFe(unittest.TestCase):
           
    def test_read_nfe(self):
        
        nfeProc = NFeHandler.nfe_from_path("nfe.xml")
        print(f"NFe Id: {nfeProc.NFe.infNFe.Id}")
        self.assertIsNotNone(nfeProc)
        
        nfecanc = NFeHandler.evento_canc_from_path("canc.xml")
        print(f"Motivo cancelamento: {nfecanc.evento.infEvento.detEvento.xJust}")
        self.assertIsNotNone(nfecanc)
        
        cce = NFeHandler.evento_cce_from_path("cce.xml")
        print(f"Correção CCe: {cce.evento.infEvento.detEvento.xCorrecao}")
        self.assertIsNotNone(cce)
        
if __name__ == '__main__':
    unittest.main()


