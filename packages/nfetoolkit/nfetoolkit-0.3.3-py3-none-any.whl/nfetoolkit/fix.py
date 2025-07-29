import xml.etree.ElementTree as ET
import json
from typing import Optional


class NFeFix:
    """
    Corrige XMLs de NF-e com base em regras definidas em um arquivo JSON.

    Cada regra contém:
    - namespace: mapa de prefixo para URI
    - path: caminho XPath até o elemento raiz da regra
    - tag: subelemento a ser alterado
    - condition: dicionário de caminhos + valores esperados
    - new_value: novo valor para a tag alvo
    """

    def __init__(self, config_file: str):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            raise ValueError(f"Erro ao carregar o arquivo de configuração: {e}")

    def apply(self, xml_content: str) -> str:
        """
        Aplica as regras de correção ao conteúdo XML fornecido.

        Args:
            xml_content (str): conteúdo XML em string

        Returns:
            str: conteúdo XML corrigido
        """
        try:
            ET.register_namespace('', 'http://www.portalfiscal.inf.br/nfe')
            tree = ET.ElementTree(ET.fromstring(xml_content))
            self.root = tree.getroot()
        except Exception as e:
            raise ValueError(f"Erro ao carregar XML: {e}")

        for rule in self.config.get("rules", []):
            namespace = rule.get("namespace", {})
            path = rule.get("path")
            target_tag_path = rule.get("tag")
            condition = rule.get("condition", {})
            new_value = rule.get("new_value")

            self.__apply_rule(path, namespace, target_tag_path, condition, new_value)

        return ET.tostring(self.root, encoding='unicode', xml_declaration=False)

    def __apply_rule(self, path: str, namespace: dict, target_tag_path: str, condition: dict, new_value: str):
        """
        Aplica uma regra a um conjunto de elementos XML.

        Altera o valor do elemento indicado em `tag` se todas as condições forem satisfeitas.
        """
        for elem in self.root.findall(path, namespace):
            if self.__match_conditions(elem, condition, namespace):
                target = elem.find(target_tag_path, namespace)
                if target is not None:
                    target.text = new_value
                    # print(f"Corrigido: {target_tag_path} => {new_value}")

    def __match_conditions(self, element: ET.Element, condition: dict, namespace: dict) -> bool:
        """
        Verifica se todas as condições são atendidas para um dado elemento.

        Args:
            element (ET.Element): o elemento base
            condition (dict): mapa de caminho => valor esperado
            namespace (dict): mapeamento de prefixos

        Returns:
            bool: True se todas as condições forem satisfeitas
        """
        for cond_path, expected_value in condition.items():
            cond_elem = element.find(cond_path, namespace)
            if cond_elem is None or cond_elem.text != expected_value:
                return False
        return True
