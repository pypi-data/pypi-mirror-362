from datetime import datetime
from typing import Union

from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from nfelib.nfe_evento_cancel.bindings.v1_0 import ProcEventoNfe as CancNFe
from nfelib.nfe_evento_cce.bindings.v1_0.proc_cce_nfe_v1_00 import ProcEventoNfe as CCe
from sped.nfe.arquivos import ArquivoDigital
from sped.nfe.registros import RegistroN100, RegistroN140, RegistroN141, RegistroN170, RegistroZ100


class NFeRepository(ArquivoDigital):
    """
    Repositório para armazenar dados estruturados de NF-e (modelo SPED) a partir de XMLs da SEFAZ.
    """

    def store_evt(self, evt: Union[CancNFe, CCe]):
        inf = evt.retEvento.infEvento
        z100 = RegistroZ100()
        z100.CNPJ = self.__format_CNPJ(inf.CNPJDest)
        z100.CPF = self.__format_CPF(inf.CPFDest)
        z100.CHAVE_NFE = inf.chNFe
        z100.DATA_EVENTO = self.__format_date(inf.dhRegEvento)
        z100.TIPO_EVENTO = inf.tpEvento
        z100.MOTIVO = inf.xMotivo.replace("|", "&p") # escape pipes
        z100.PROTOCOLO = inf.nProt
        z100.DESC_EVENTO = inf.xEvento.replace("|", "&p") # escape pipes
        self.blocoZ.add(z100)

    def store_nfe(self, nfeProc: NfeProc):
        ide = nfeProc.NFe.infNFe.ide
        emit = nfeProc.NFe.infNFe.emit
        dest = nfeProc.NFe.infNFe.dest

        # Cabeçalho
        n100 = RegistroN100()
        n100.CNPJ_EMIT = emit.CNPJ
        n100.NOME_EMIT = emit.xNome
        n100.NUM_NFE = ide.nNF
        n100.SERIE = ide.serie

        # Data de emissão e MES_ANO
        try:
            dt_emissao = datetime.strptime(ide.dhEmi[:10], "%Y-%m-%d").date()
        except Exception:
            dt_emissao = None

        n100.DT_EMISSAO = dt_emissao
        n100.MES_ANO = dt_emissao.strftime('%m_%Y') if dt_emissao else ""

        n100.TIPO_NFE = {'0': "ENTRADA", '1': "SAIDA"}.get(ide.tpNF.value, "UNKNOWN")
        n100.CHAVE_NFE = nfeProc.protNFe.infProt.chNFe

        # Destinatário
        n100.CNPJ_DEST = self.__format_CNPJ(getattr(dest, 'CNPJ', '') or '')
        n100.CPF_DEST = self.__format_CPF(getattr(dest, 'CPF', '') or '')
        n100.NOME_DEST = getattr(dest, 'xNome', '') or ''
        
        uf_raw = getattr(getattr(dest, 'enderDest', None), 'UF', None)
        n100.UF = uf_raw.value if hasattr(uf_raw, 'value') else uf_raw or ''
        
        n100.VALOR_NFE = self.__check_float(nfeProc.NFe.infNFe.total.ICMSTot.vNF)

        # Datas e status    
        n100.DATA_IMPORTACAO = datetime.today().date()
        n100.STATUS_NFE = "AUTORIZADA"

        self.blocoN.add(n100)

        self.__processar_fatura(nfeProc)
        self.__processar_itens(nfeProc, n100)

    def __processar_fatura(self, nfeProc: NfeProc):
        cobr = nfeProc.NFe.infNFe.cobr
        if not cobr:
            return

        if fat := cobr.fat:
            n140 = RegistroN140()
            n140.NUM_FAT = fat.nFat
            n140.VLR_ORIG = self.__check_float(fat.vOrig)
            n140.VLR_DESC = self.__check_float(fat.vDesc)
            n140.VLR_LIQ = self.__check_float(fat.vLiq)
            self.blocoN.add(n140)

        for dup in cobr.dup:
            n141 = RegistroN141()
            n141.NUM_DUP = dup.nDup
            n141.DT_VENC = self.__format_date(dup.dVenc)
            n141.VLR_DUP = self.__check_float(dup.vDup)
            self.blocoN.add(n141)

    def __processar_itens(self, nfeProc: NfeProc, n100: RegistroN100):
        for i, item in enumerate(nfeProc.NFe.infNFe.det, start=1):
            n170 = RegistroN170()
            n170.NUM_ITEM = i
            n170.COD_PROD = item.prod.cProd.replace("|", "&p") # escape pipes
            n170.DESC_PROD = item.prod.xProd.replace("|", "&p") # escape pipes
            n170.NCM = item.prod.NCM
            n170.CEST = item.prod.CEST
            n170.CFOP = item.prod.CFOP
            n170.VLR_UNIT = self.__check_float(item.prod.vUnCom)
            n170.QTDE = self.__check_float(item.prod.qCom)
            n170.UNID = item.prod.uCom
            n170.VLR_PROD = self.__check_float(item.prod.vProd)
            n170.VLR_FRETE = self.__check_float(getattr(item.prod, 'vFrete', 0.0))
            n170.VLR_SEGURO = self.__check_float(getattr(item.prod, 'vSeg', 0.0))
            n170.VLR_DESC = self.__check_float(getattr(item.prod, 'vDesc', 0.0))
            n170.VLR_OUTROS = self.__check_float(getattr(item.prod, 'vOutro', 0.0))
            n170.VLR_ITEM = n170.VLR_PROD + n170.VLR_FRETE + n170.VLR_SEGURO - n170.VLR_DESC + n170.VLR_OUTROS

            icms_data = self.__extract_icms_data(item.imposto.ICMS)
            ipi_data = self.__extract_ipi_data(item.imposto.IPI)
            pis_data = self.__extract_pis_data(item.imposto.PIS)
            cofins_data = self.__extract_cofins_data(item.imposto.COFINS)
            # ORIGEM, CST_ICMS, BC_ICMS, ALQ_ICMS, VLR_ICMS, ALQ_ICMSST, MVA, BC_ICMSST, ICMSST
            (
                n170.ORIGEM, n170.CST_ICMS, n170.BC_ICMS, n170.ALQ_ICMS,
                n170.VLR_ICMS, n170.ALQ_ICMSST, n170.MVA, n170.BC_ICMSST, n170.ICMSST
            ) = icms_data

            (n170.CST_IPI, n170.BC_IPI, n170.ALQ_IPI, n170.VLR_IPI) = ipi_data
            (n170.CST_PIS, n170.BC_PIS, n170.ALQ_PIS, n170.VLR_PIS) = pis_data
            (n170.CST_COFINS, n170.BC_COFINS, n170.ALQ_COFINS, n170.VLR_COFINS) = cofins_data
            self.blocoN.add(n170)

    def __extract_icms_data(self, ICMS):
        def fill_list(data, size, fill=0.0):
            return data + [fill] * (size - len(data))

        icms_map = {
            'ICMS00': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
            'ICMS10': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMS20': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
            'ICMS30': ('orig.value', 'CST.value', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMS40': ('orig.value', 'CST.value'),
            'ICMS51': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
            'ICMS60': ('orig.value', 'CST.value'),
            'ICMS70': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMS90': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMSSN101': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN'),
            'ICMSSN102': ('orig.value', 'CSOSN.value'),
            'ICMSSN201': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMSSN202': ('orig.value', 'CSOSN.value', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
            'ICMSSN500': ('orig.value', 'CSOSN.value'),
            'ICMSSN900': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST')
        }

        for tipo, attrs in icms_map.items():
            icms = getattr(ICMS, tipo, None)
            if icms:
                values = [self.__resolve_attr_path(icms, attr, 0.0) for attr in attrs]
                # ORIGEM, CST_ICMS, BC_ICMS, ALQ_ICMS, VLR_ICMS, ALQ_ICMSST, MVA, BC_ICMSST, ICMSST
                return fill_list(values, 9)
        return ["0", "00", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def __extract_ipi_data(self, IPI):
        if IPI:
            if IPITrib := getattr(IPI, 'IPITrib', None):
                return [IPITrib.CST.value, IPITrib.vBC, IPITrib.pIPI, IPITrib.vIPI]
            elif IPINT := getattr(IPI, 'IPINT', None):
                return [IPINT.CST.value, 0.0, 0.0, 0.0]
        return ["99", 0.0, 0.0, 0.0]
    
    def __extract_pis_data(self, PIS):
        if PIS:
            if PISAliq := getattr(PIS, 'PISAliq', None):
                return [PISAliq.CST.value, PISAliq.vBC, PISAliq.pPIS, PISAliq.vPIS]
            elif PISOutr := getattr(PIS, 'PISOutr', None):
                return [PISOutr.CST.value, PISOutr.vBC, PISOutr.pPIS, PISOutr.vPIS]
            elif PISNT := getattr(PIS, 'PISNT', None):
                return [PISNT.CST.value, 0.0, 0.0, 0.0]
        return ["99", 0.0, 0.0, 0.0]
    
    def __extract_cofins_data(self, COFINS):
        if COFINS:
            if COFINSAliq := getattr(COFINS, 'COFINSAliq', None):
                return [COFINSAliq.CST.value, COFINSAliq.vBC, COFINSAliq.pCOFINS, COFINSAliq.vCOFINS]
            elif COFINSOutr := getattr(COFINS, 'COFINSOutr', None):
                return [COFINSOutr.CST.value, COFINSOutr.vBC, COFINSOutr.pCOFINS, COFINSOutr.vCOFINS]
            elif COFINSNT := getattr(COFINS, 'COFINSNT', None):
                return [COFINSNT.CST.value, 0.0, 0.0, 0.0]
        return ["99", 0.0, 0.0, 0.0]

    @staticmethod
    def __format_CNPJ(cnpj):
        if not cnpj or len(cnpj) != 14 or not cnpj.isdigit():
            return ""
        try:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
        except Exception:
            return ""

    @staticmethod
    def __format_CPF(cpf):
        cpf = ''.join(filter(str.isdigit, str(cpf)))
        if len(cpf) != 11:
            return ""
        try:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        except Exception:
            return ""

    @staticmethod
    def __check_float(var):
        try:
            return float(var or 0.0)
        except Exception:
            return 0.0

    @staticmethod
    def __format_date(date_str):
        """Formata datas no padrão ddmmaaaa."""
        return f'{date_str[8:10]}{date_str[5:7]}{date_str[:4]}'

    @staticmethod
    def __resolve_attr_path(obj, path, default=None):
        parts = path.split(".")
        val = obj
        for part in parts:
            val = getattr(val, part, None)
            if val is None:
                return default
        return val