import zipfile
import random
import string
import shutil
from pathlib import Path
from .handler import NFeHandler
from tqdm import tqdm


class NFeOrganizer:
    @staticmethod
    def organize_xmls(source_dir_fd: str, dest_dir_fd: str, folders_map=None, verbose: bool = False):
        """
        Organiza os arquivos XML em subpastas do diretório de destino, com barra de progresso opcional.
        """
        if folders_map is None:
            folders_map = {
                'nfe_type': 'nfe',
                'canc_type': 'canc',
                'cce_type': 'cce',
                'inut_type': 'inut',
            }

        NFeOrganizer.create_dest_folders(dest_dir_fd, folders_map)

        all_files = list(Path(source_dir_fd).rglob('*'))

        iterator = tqdm(all_files, desc="Organizando XMLs", unit="arquivo") if verbose else all_files

        for file_path in iterator:
            if file_path.is_file():
                if file_path.suffix == '.zip':
                    NFeOrganizer.extract_xmls(file_path, dest_dir_fd, verbose=verbose)
                elif file_path.suffix == '.xml':
                    try:
                        xml_type = NFeHandler.xml_type(file_path)
                        if xml_type == 'unknown_type':
                            print(f"[AVISO] Tipo desconhecido: {file_path.name}")
                        else:
                            destino = Path(dest_dir_fd) / folders_map[xml_type] / file_path.name
                            shutil.move(str(file_path), str(destino))
                    except Exception as e:
                        print(f"[ERRO] Falha ao processar {file_path.name}: {e}")

    @staticmethod
    def extract_xmls(zip_file: Path, dest_dir_fd: str, verbose: bool = False):
        """
        Extrai arquivos XML de um arquivo ZIP e organiza no diretório destino.
        """
        temp_folder = Path.cwd() / ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        temp_folder.mkdir(parents=True)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        NFeOrganizer.organize_xmls(source_dir_fd=temp_folder, dest_dir_fd=dest_dir_fd, verbose=verbose)
        shutil.rmtree(temp_folder)

    @staticmethod
    def create_dest_folders(base_path: str, dest_fds_map: dict):
        """
        Cria pastas de destino conforme o mapa de tipos.
        """
        base = Path(base_path)
        base.mkdir(parents=True, exist_ok=True)
        for folder in dest_fds_map.values():
            (base / folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def find_all(from_path: str, xml_types: list = None):
        """
        Retorna lista de arquivos XML do tipo informado a partir de um diretório.

        Args:
            from_path (str): Caminho base para varredura.
            xml_types (list, opcional): Lista de tipos (ex: ['nfe_type', 'cce_type']).

        Returns:
            list[Path]: Lista de arquivos XML encontrados.
        """
        xml_types = xml_types or [
            'nfe_type', 
            'canc_type', 
            'cce_type', 
            'inut_type',
            'conf_op_type',
            'cienc_op_type',
            'desc_op_type',
            'op_nr_type'
        ]
        files = []

        for file_path in Path(from_path).rglob('*.xml'):
            try:
                xml_type = NFeHandler.xml_type(file_path)
                if xml_type in xml_types:
                    files.append(file_path)
            except Exception as e:
                print(f"[ERRO] Erro ao classificar {file_path}: {e}")
        return files
