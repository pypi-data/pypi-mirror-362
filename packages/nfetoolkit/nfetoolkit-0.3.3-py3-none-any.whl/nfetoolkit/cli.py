import argparse
from pathlib import Path
from tqdm import tqdm

from nfetoolkit.organizer import NFeOrganizer
from nfetoolkit.handler import NFeHandler
from nfetoolkit.repository import NFeRepository
from nfetoolkit.fix import NFeFix


def cmd_organize(args):
    try:
        verbose = not getattr(args, 'no_verbose', False)

        source_path = Path(args.source)
        dest_path = Path(args.dest) if args.dest else source_path / "xmls_organizados"

        NFeOrganizer.organize_xmls(str(source_path), str(dest_path), verbose=verbose)
        print(f"[OK] XMLs organizados de {source_path} para {dest_path}")
    except Exception as e:
        print(f"[ERRO] Falha ao organizar XMLs: {e}")


def cmd_export(args):
    try:
        verbose = not getattr(args, 'no_verbose', False)
        nfe_rep = NFeRepository()
        xml_paths = NFeOrganizer.find_all(args.path)
        iterator = tqdm(xml_paths, desc="Exportando NF-es", unit="xml") if verbose else xml_paths

        for xml in iterator:
            tipo = NFeHandler.xml_type(xml)
            match tipo:
                case 'nfe_type':
                    nfe_rep.store_nfe(NFeHandler.nfe_from_path(xml))
                case 'canc_type':
                    nfe_rep.store_evt(NFeHandler.evento_canc_from_path(xml))
                case 'cce_type':
                    nfe_rep.store_evt(NFeHandler.evento_cce_from_path(xml))

        output_file = Path(args.output) if args.output else Path.cwd() / "nfe_data.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            nfe_rep.write_to(file)

        print(f"[OK] Dados exportados para: {output_file}")
    except Exception as e:
        print(f"[ERRO] Falha na exportação: {e}")


def cmd_fix(args):
    try:
        verbose = not getattr(args, 'no_verbose', False)
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir) if args.output_dir else input_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        fix = NFeFix(args.config)
        xml_files = list(input_dir.rglob("*.xml"))
        iterator = tqdm(xml_files, desc="Corrigindo XMLs", unit="xml") if verbose else xml_files

        for xml_file in iterator:
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                fixed_xml = fix.apply(content)

                output_file = output_dir / xml_file.name
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_xml)
            except Exception as inner_e:
                print(f"[ERRO] {xml_file.name}: {inner_e}")

        print(f"[OK] Correções aplicadas em {len(xml_files)} arquivos.")
    except Exception as e:
        print(f"[ERRO] Falha ao aplicar correções em lote: {e}")


def cmd_danfe(args):
    try:
        nfeProc = NFeHandler.nfe_from_path(args.xml)
        NFeHandler.nfe_to_pdf(nfeProc, args.output)
        print(f"[OK] PDF gerado em: {args.output}")
    except Exception as e:
        print(f"[ERRO] Falha ao gerar PDF: {e}")


def main():
    parser = argparse.ArgumentParser(description="nfetoolkit - ferramenta de gerenciamento de NF-e")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # organize
    parser_organize = subparsers.add_parser('organize', help='Organiza os XMLs em subpastas por tipo')
    parser_organize.add_argument('source', help='Diretório de origem')
    parser_organize.add_argument('--dest', help='Diretório de destino (padrão: <source>/xmls_organizados)')
    parser_organize.add_argument('--no-verbose', action='store_true', help='Oculta barra de progresso')
    parser_organize.set_defaults(func=cmd_organize)

    # export
    parser_export = subparsers.add_parser('export', help='Exporta dados estruturados das NF-es')
    parser_export.add_argument('path', help='Caminho com XMLs da NF-e')
    parser_export.add_argument('--output', help='Arquivo de saída (padrão: ./nfe_data.txt)')
    parser_export.add_argument('--no-verbose', action='store_true', help='Oculta a barra de progresso')
    parser_export.set_defaults(func=cmd_export)

    # fix
    parser_fix = subparsers.add_parser('fix', help='Corrige um lote de XMLs conforme configuração')
    parser_fix.add_argument('input_dir', help='Diretório com arquivos XML a corrigir')
    parser_fix.add_argument('config', help='Arquivo de configuração JSON')
    parser_fix.add_argument('--output_dir', help='Diretório destino dos XMLs corrigidos (padrão: mesmo do original)')
    parser_fix.add_argument('--no-verbose', action='store_true', help='Oculta a barra de progresso')
    parser_fix.set_defaults(func=cmd_fix)

    # danfe
    parser_read = subparsers.add_parser('danfe', help='Gera DANFE (PDF) a partir de uma NF-e')
    parser_read.add_argument('xml', help='Caminho do XML da NF-e')
    parser_read.add_argument('--output', default='nfe.pdf', help='Caminho do PDF gerado')
    parser_read.set_defaults(func=cmd_danfe)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
