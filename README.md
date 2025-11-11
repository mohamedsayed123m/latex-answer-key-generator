# 📝 Gerador de Gabarito LaTeX para CSV

Código para extração de gabaritos de provas escritas em LaTeX e exportá-los em formato CSV para ser usado como input em sistema OMR (_e.g._, https://github.com/Udayraj123/OMRChecker/). Desenvolvido com **Orientação a Objetos** e **Type Hints** completos.

## 🎯 Funcionalidades

- ✅ **Extração automática** de respostas de arquivos LaTeX.
- ✅ **Suporte a múltiplos formatos** de questões:
  - Múltipla escolha (A, B, C, D, E)
  - Verdadeiro/Falso (V/F)
- ✅ **Exportação em CSV** para fácil integração com sistemas de correção.
- ✅ **Interface interativa** com valores padrão.
- ✅ **Arquitetura OOP** com separação de responsabilidades.
- ✅ **Type Hints** completos para melhor manutenção.
- ✅ **Preview automático** das respostas extraídas.

## 📋 Pré-requisitos

- Python 3.7 ou superior.
- Nenhuma dependência externa necessária (usa apenas biblioteca padrão).

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/latex-answer-key-generator.git

# Acesse o diretório
cd latex-answer-key-generator

# Execute o código
python3 generate_answer_key.py
```

## 📖 Como Usar

### Uso Básico

```bash
python3 generate_answer_key.py
```

O programa solicitará:
1. **Arquivo LaTeX de entrada** (padrão: `P1A.tex`).
2. **Arquivo CSV de saída** (padrão: `P1A.csv`).

Pressione `Enter` para usar os valores padrão ou digite caminhos personalizados. O arquivo P1A.tex pode ser gerado conforme código disponível em https://github.com/wyllianbs/carderno_prova.

### Exemplo de Execução

```bash
$ python3 generate_answer_key.py
Digite o caminho do arquivo LaTeX (padrão: P1A.tex):
Digite o nome do arquivo CSV de saída (padrão: P1A.csv):

Processando questões...

Gabarito salvo com sucesso em: P1A.csv
Total de questões processadas: 10

Preview das primeiras 10 respostas:
  q1,V
  q2,C
  q3,C
  q4,E
  q5,A
  q6,F
  q7,B
  q8,F
  q9,B
  q10,F
```

## 📄 Formato do Arquivo LaTeX

### Questões de Múltipla Escolha

O código identifica questões de múltipla escolha através dos comandos `\ti` e `\di`:

```latex
\item \rtask \ponto{\pt} Qual é a capital do Estado do Paraná?

\begin{answerlist}[label={\texttt{\Alph*}.},leftmargin=*]
  \ti São Paulo.
  \ti Rio de Janeiro.
  \di Curitiba.  % Resposta correta (posição C)
  \ti Florianópolis.
  \ti Belo Horizonte.
\end{answerlist}
```

**Resultado:** `q1,C`

### Questões Verdadeiro/Falso

O código identifica questões V/F através do comando `\doneitem`:

```latex
\item \rtask \ponto{\pt} Python é uma linguagem de programação.

% V
{\setlength{\columnsep}{0pt}\renewcommand{\columnseprule}{0pt}
\begin{multicols}{2}
  \begin{answerlist}[label={\texttt{\Alph*}.},leftmargin=*]
    \ifnum\gabarito=1\doneitem[V.]\else\ti[V.]\fi % Resposta correta (V)
    \ti[F.]
  \end{answerlist}
\end{multicols}
}
```

**Resultado:** `q1,V`

## 🏗️ Arquitetura

O projeto segue princípios de **Clean Code** e **SOLID**:

```
generate_answer_key.py
├── Answer              # Modelo de dados para resposta
├── LatexParser         # Parser de arquivos LaTeX
├── CSVExporter         # Exportador para formato CSV
├── AnswerKeyGenerator  # Orquestrador principal
└── main()              # Ponto de entrada
```

### Classes Principais

#### `Answer`
Representa uma resposta individual com número da questão e alternativa.

```python
answer = Answer(question_number=1, answer="C")
print(answer.to_csv_line())  # "q1,C\n"
```

#### `LatexParser`
Responsável por extrair respostas do conteúdo LaTeX.

```python
parser = LatexParser(latex_content)
answers = parser.parse()
```

#### `CSVExporter`
Gerencia a exportação das respostas para CSV.

```python
exporter = CSVExporter(Path("gabarito.csv"))
exporter.export(answers)
```

#### `AnswerKeyGenerator`
Coordena todo o processo de geração do gabarito.

```python
generator = AnswerKeyGenerator("prova.tex", "gabarito.csv")
generator.run()
```

## 📊 Formato de Saída

O arquivo CSV gerado segue o formato:

```csv
q1,V
q2,C
q3,F
q4,E
q5,A
q6,B
```

em que:
- **Primeira coluna**: Identificador da questão (`q1`, `q2`, ...).
- **Segunda coluna**: Resposta (`A`-`E` para múltipla escolha, `V`/`F` para verdadeiro/falso).

O arquivo de saída CSV poderá ser usado em um sistema OMR (_Optical Mark Reader_), _e.g._, https://github.com/Udayraj123/OMRChecker/.

## 🎨 Exemplo Completo

Veja o arquivo [`P1A.tex`](P1A.tex) (https://github.com/wyllianbs/carderno_prova) incluído no repositório para um exemplo completo de prova LaTeX compatível com o gerador.

### Estrutura do P1A.tex

```latex
\begin{enumerate}[resume=*questions,label={\arabic*.},leftmargin=*]
  \setcounter{rtaskno}{0}
  
  % Questão 1 - Verdadeiro/Falso
  \item \rtask \ponto{\pt} Lorem ipsum...
  % V
  {\setlength{\columnsep}{0pt}
  \begin{multicols}{2}
    \begin{answerlist}[label={\texttt{\Alph*}.},leftmargin=*]
      \ifnum\gabarito=1\doneitem[V.]\else\ti[V.]\fi
      \ti[F.]
    \end{answerlist}
  \end{multicols}
  }
  
  % Questão 2 - Múltipla Escolha
  \item \rtask \ponto{\pt} Lorem ipsum...
  \begin{answerlist}[label={\texttt{\Alph*}.},leftmargin=*]
    \ti Opção A
    \ti Opção B
    \di Opção C  % Resposta correta
    \ti Opção D
    \ti Opção E
  \end{answerlist}
  
\end{enumerate}
```

## 🔧 Personalização

### Modificando Padrões

Edite as funções `get_user_input()` para alterar valores padrão:

```python
def main() -> None:
    input_file = get_user_input(
        "Digite o caminho do arquivo LaTeX",
        "minha_prova.tex"  # Novo padrão
    )
    
    output_file = get_user_input(
        "Digite o nome do arquivo CSV de saída",
        "meu_gabarito.csv"  # Novo padrão
    )
```

### Adicionando Novos Formatos

Para suportar novos tipos de questões, estenda a classe `LatexParser`:

```python
class LatexParser:
    def _extract_custom_answer(self, content: str) -> Optional[str]:
        # Implemente sua lógica aqui
        pass
```

## 🐛 Tratamento de Erros

O programa valida:
- ✅ Existência do arquivo LaTeX especificado.
- ✅ Formato correto do arquivo LaTeX.
- ✅ Presença de questões no documento.
- ✅ Permissões de escrita no diretório de saída.
- ✅ Codificação UTF-8 dos arquivos.

### Mensagens de Erro Comuns

```bash
# Arquivo não encontrado
Erro: Arquivo 'prova.tex' não encontrado.

# Nenhuma resposta detectada
Aviso: Não foi possível encontrar resposta para a questão 5.

# Sem questões no arquivo
Nenhuma resposta foi encontrada no arquivo.
```

## 🧪 Testando

### Teste Manual

```bash
# Use o arquivo de exemplo incluído
python3 generate_answer_key.py
# Pressione Enter duas vezes para usar P1A.tex
```

### Validação do CSV

```bash
# Visualize o gabarito gerado
cat P1A.csv

# Conte o número de questões
wc -l P1A.csv
```

## 📚 Requisitos Técnicos

### Type Hints

O código utiliza type hints completos para melhor IDE support:

```python
def extract_answers(latex_content: str) -> List[Answer]:
    ...

def save_to_csv(answers: List[Answer], output_file: Path) -> None:
    ...
```

### Orientação a Objetos

Princípios aplicados:
- **Single Responsibility Principle**: Cada classe tem uma responsabilidade única.
- **Open/Closed Principle**: Fácil extensão sem modificação.
- **Dependency Inversion**: Dependência de abstrações, não implementações.


## 📜 Licença

Este projeto está licenciado sob a Licença [GNU General Public License v3.0](LICENSE).

## 👤 Autor

**Prof. Wyllian B. da Silva**  
Departamento de Informática e Estatística (INE)  
Universidade Federal de Santa Catarina (UFSC)

---

**Nota**: Este projeto foi desenvolvido especificamente para uso na UFSC, mas pode ser facilmente adaptado para outras instituições de ensino.
