import os
import warnings
import inspect
import xml.etree.ElementTree as ET
from typing import Optional, List, Any

from lxml import etree
from xsdata import __version__ as xsdata_version
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from nfelib.nfe_evento_cancel.bindings.v1_0 import ProcEventoNfe as CancNFe
from nfelib.nfe_evento_cce.bindings.v1_0.proc_cce_nfe_v1_00 import ProcEventoNfe as CCe


class NFeHandler:
    """
    NFeHandler fornece métodos para lidar com documentos XML de NF-e:
    parsing, serialização, validação, assinatura e geração de DANFE (PDF).
    """
    
    _parser = XmlParser()

    # --- PARSE ---
    @staticmethod
    def nfe_from_path(path: str) -> NfeProc:
        return NFeHandler._parser.parse(path, NfeProc)

    @staticmethod
    def evento_canc_from_path(path: str) -> CancNFe:
        return NFeHandler._parser.parse(path, CancNFe)

    @staticmethod
    def evento_cce_from_path(path: str) -> CCe:
        return NFeHandler._parser.parse(path, CCe)

    @staticmethod
    def from_path(path: str) -> Optional[Any]:
        for method in [
            NFeHandler.nfe_from_path,
            NFeHandler.evento_canc_from_path,
            NFeHandler.evento_cce_from_path,
        ]:
            try:
                return method(path)
            except Exception:
                continue
        return None

    # --- SERIALIZAÇÃO XML ---
    @staticmethod
    def to_xml(
        clazz,
        indent: str = "  ",
        ns_map: Optional[dict] = None,
        pkcs12_data: Optional[bytes] = None,
        pkcs12_password: Optional[str] = None,
        doc_id: Optional[str] = None,
        pretty_print: Optional[str] = None,
    ) -> str:
        """Serializa o objeto xsdata para XML, com suporte a assinatura digital."""
        major_version = xsdata_version.split(".")[0]
        if major_version in ("20", "21", "22", "23"):
            serializer = XmlSerializer(config=SerializerConfig(pretty_print=pretty_print))
        else:
            if pretty_print:
                warnings.warn("`pretty_print` está obsoleto, use `indent`.")
                indent = "  "
            serializer = XmlSerializer(config=SerializerConfig(indent=indent))

        if ns_map is None:
            if hasattr(clazz.Meta, "namespace"):
                ns_map = {None: clazz.Meta.namespace}
            else:
                package = clazz._get_package()
                ns_map = {None: f"http://www.portalfiscal.inf.br/{package}"}

        xml = serializer.render(obj=clazz, ns_map=ns_map)

        if pkcs12_data:
            return NFeHandler.sign_xml(xml, pkcs12_data, pkcs12_password, doc_id)

        return xml

    @staticmethod
    def nfe_to_xml(nfeproc: NfeProc) -> str:
        return NFeHandler.to_xml(nfeproc)

    @staticmethod
    def evento_canc_to_xml(nfecanc: CancNFe) -> str:
        return NFeHandler.to_xml(nfecanc)

    @staticmethod
    def evento_cce_to_xml(cce: CCe) -> str:
        return NFeHandler.to_xml(cce)

    # --- ASSINATURA DIGITAL ---
    @classmethod
    def sign_xml(
        cls,
        xml: str,
        pkcs12_data: Optional[bytes] = None,
        pkcs12_password: Optional[str] = None,
        doc_id: Optional[str] = None,
    ) -> str:
        try:
            from erpbrasil.assinatura import certificado as cert
            from erpbrasil.assinatura.assinatura import Assinatura
        except ImportError as e:
            raise RuntimeError("erpbrasil.assinatura não está instalado!") from e

        certificate = cert.Certificado(
            arquivo=os.environ.get("CERT_FILE", pkcs12_data),
            senha=os.environ.get("CERT_PASSWORD", pkcs12_password),
        )
        xml_etree = etree.fromstring(xml.encode("utf-8"))
        return Assinatura(certificate).assina_xml2(xml_etree, doc_id)

    # --- VALIDAÇÃO ---
    @staticmethod
    def validate_xml(obj_xml: Any, schema_path: Optional[str] = None) -> List[str]:
        xml = NFeHandler.to_xml(obj_xml)
        return NFeHandler._schema_validation(obj_xml, xml, schema_path)

    @staticmethod
    def _schema_validation(obj_xml: Any, xml: str, schema_path: Optional[str] = None) -> List[str]:
        messages = []
        doc_etree = etree.fromstring(xml.encode("utf-8"))
        if not schema_path:
            schema_path = NFeHandler._get_schema_path(obj_xml)

        xmlschema_doc = etree.parse(schema_path)
        parser = etree.XMLSchema(xmlschema_doc)
        if not parser.validate(doc_etree):
            messages.extend(error.message for error in parser.error_log)
        return messages

    @classmethod
    def _get_schema_path(cls, obj_xml: Any) -> str:
        package = inspect.getmodule(obj_xml).__name__

        base = os.path.dirname(os.path.dirname(__file__))
        if package.startswith("nfelib.nfe"):
            return os.path.join(base, "nfe", "schemas", "v4_0", "procNFe_v4.00.xsd")
        if package.startswith("nfelib.nfe_evento_cce"):
            return os.path.join(base, "cce", "schemas", "v1_0", "procCCeNFe_v1.00.xsd")
        if package.startswith("nfelib.nfe_evento_cancel"):
            return os.path.join(base, "nfecanc", "schemas", "v1_0", "procEventoCancNFe_v1.00.00.xsd")
        return "undef"

    # --- DANFE ---
    @staticmethod
    def nfe_to_pdf(nfeProc: NfeProc, pdf_filename: str):
        pdf_bytes = nfeProc.to_pdf()
        with open(pdf_filename, 'wb') as f:
            f.write(pdf_bytes)

    # --- TIPO DE XML ---
    @staticmethod
    def xml_type(xml_file: str) -> str:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        tag = root.tag
        if tag == '{http://www.portalfiscal.inf.br/nfe}nfeProc':
            return 'nfe_type'
        elif tag == '{http://www.portalfiscal.inf.br/nfe}procEventoNFe':
            tipo_evt = root.find('.//nfe:tpEvento', ns)
            if tipo_evt is not None:
                codigo = tipo_evt.text
                return {
                    '110111': 'canc_type',        # Cancelamento
                    '110110': 'cce_type',         # Carta de Correção
                    '210200': 'conf_op_type',   # Confirmação da Operação
                    '210210': 'cienc_op_type',     # Ciência da Operação
                    '210220': 'desc_op_type',    # Desconhecimento da Operação
                    '210240': 'op_nr_type',      # Operação Não Realizada
                }.get(codigo, 'undefined')
        elif tag == '{http://www.portalfiscal.inf.br/nfe}retInutNFe':
            return 'inut_type'

        return 'unknown_type'
