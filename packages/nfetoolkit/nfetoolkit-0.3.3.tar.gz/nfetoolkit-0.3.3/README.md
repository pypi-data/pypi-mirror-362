# nfetoolkit

Ferramenta de linha de comando para organizar, corrigir, ler e exportar arquivos XML de Nota Fiscal Eletrônica (NF-e).

---

## 📦 Instalação de dependências

Certifique-se de ter o Python 3.9+ instalado.

Instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como usar

Execute a ferramenta com o comando:

```bash
python manage.py <comando> [opções]
```

---

## 🔁 Comandos disponíveis

### 🗂️ `organize`

Organiza os arquivos XML em subpastas por tipo: `nfe`, `canc`, `cce`, `inut`.

```bash
python manage.py organize <source_dir> <dest_dir> [--no-verbose]
```

**Exemplo:**

```bash
python manage.py organize C:\xmls_originais C:\xmls_organizados
```

---

### 📤 `export`

Exporta os dados estruturados dos XMLs encontrados para um arquivo `.txt`.

```bash
python manage.py export <xml_dir> [--output <arquivo_saida>] [--no-verbose]
```

**Exemplo:**

```bash
python manage.py export C:\xmls_organizados --output export.txt
```

Se não especificar `--output`, será gerado `./nfe_data.txt` no diretório atual.

---

### 🛠️ `fix`

Aplica correções definidas em um arquivo `config.json` a todos os XMLs de um diretório.

```bash
python manage.py fix <input_dir> <config.json> [--output_dir <destino>] [--no-verbose]
```

**Exemplo:**

```bash
python manage.py fix C:\xmls_organizados config.json --output_dir C:\xmls_corrigidos
```

Se `--output_dir` não for informado, os arquivos corrigidos serão salvos no mesmo diretório de origem.

---

### 📄 `read`

Gera o DANFE (arquivo PDF) de uma NF-e.

```bash
python manage.py read <xml_file> [--output <arquivo_pdf>]
```

**Exemplo:**

```bash
python manage.py read nfe.xml --output nota.pdf
```

---

## 🔧 Exemplo de `config.json` para o comando `fix`

```json
{
  "rules": [
    {
      "namespace": {
        "ns": "http://www.portalfiscal.inf.br/nfe"
      },
      "path": ".//ns:det",
      "tag": ".//ns:imposto/ns:ICMS/ns:ICMS00/ns:orig",
      "condition": {
        ".//ns:prod/ns:NCM": "85142011",
        ".//ns:imposto/ns:ICMS/ns:ICMS00/ns:orig": "0"
      },
      "new_value": "2"
    }
  ]
}
```

---

## 📌 Observações

- O padrão é exibir barra de progresso (`verbose=True`). Use `--no-verbose` se quiser ocultar.
- A estrutura esperada dos XMLs segue o padrão da SEFAZ.
- Os dados exportados seguem o layout dos blocos SPED (`RegistroN100`, `N170`, `Z100`, etc.).

---

## 📁 Estrutura recomendada do projeto

```
nfetoolkit/
├── core/
│   ├── handler.py
│   ├── fix.py
│   ├── organizer.py
│   ├── repository.py
├── manage.py
├── config.json
├── requirements.txt
```

---

## 🔗 Licença

Este projeto é distribuído sob a licença MIT.