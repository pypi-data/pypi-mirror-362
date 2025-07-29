import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit.fix import NFeFix

class TestFixNFe(unittest.TestCase):
           
    def test_fix_nfe(self):
        
        # Arquivo JSON de configuração
      config_file = 'nfe_fix.json'

      # XML de exemplo
      xml = 'nfe.xml'
      with open(xml, 'r') as file:
        xml_content = file.read()

      # Instancia o corretor e aplica as correções
      fix = NFeFix(config_file)
      modified_xml = fix.apply(xml_content)

      # Obtém o XML modificado

      print(modified_xml)
      with open('modified.xml', 'w') as f:
          f.write(modified_xml)
    
if __name__ == '__main__':
    unittest.main()

