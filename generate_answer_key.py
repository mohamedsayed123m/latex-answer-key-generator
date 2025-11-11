import re
import sys
from typing import List, Tuple, Optional
from pathlib import Path


class Answer:
    """Representa uma resposta de questão."""

    def __init__(self, question_number: int, answer: str) -> None:
        self.question_number = question_number
        self.answer = answer

    def __repr__(self) -> str:
        return f"Answer(q{self.question_number}, {self.answer})"

    def to_csv_line(self) -> str:
        """Converte a resposta para formato CSV."""
        return f"q{self.question_number},{self.answer}\n"


class LatexParser:
    """Parser para extrair respostas de arquivos LaTeX."""

    def __init__(self, content: str) -> None:
        self.content = content
        self.answers: List[Answer] = []

    def parse(self) -> List[Answer]:
        """Extrai todas as respostas do conteúdo LaTeX."""
        items = re.split(r'\\item\s+\\rtask', self.content)

        for question_number, item in enumerate(items[1:], start=1):
            answer = self._extract_answer_from_item(item, question_number)
            if answer:
                self.answers.append(answer)

        return self.answers

    def _extract_answer_from_item(self, item: str, question_number: int) -> Optional[Answer]:
        """Extrai a resposta de um item individual."""
        # Procura pelo bloco answerlist
        answerlist_match = re.search(
            r'\\begin\{answerlist\}.*?\\end\{answerlist\}',
            item,
            re.DOTALL
        )

        if answerlist_match:
            answerlist_content = answerlist_match.group(0)

            # Tenta extrair resposta V/F
            answer_text = self._extract_true_false_answer(answerlist_content)

            # Se não encontrou V/F, tenta múltipla escolha
            if not answer_text:
                answer_text = self._extract_multiple_choice_answer(answerlist_content)

            if answer_text:
                return Answer(question_number, answer_text)

        # Tenta método alternativo (comentário)
        answer_text = self._extract_comment_answer(item)
        if answer_text:
            return Answer(question_number, answer_text)

        print(f"Aviso: Não foi possível encontrar resposta para a questão {question_number}.")
        return None

    def _extract_true_false_answer(self, answerlist_content: str) -> Optional[str]:
        """Extrai resposta de questões Verdadeiro/Falso."""
        doneitem_match = re.search(r'\\doneitem\[([VF])[.\]]', answerlist_content)
        if doneitem_match:
            return doneitem_match.group(1)
        return None

    def _extract_multiple_choice_answer(self, answerlist_content: str) -> Optional[str]:
        """Extrai resposta de questões de múltipla escolha."""
        # Encontra todas as ocorrências de \ti ou \di
        lines = re.findall(r'\\(ti|di)(?:\s|\[)', answerlist_content)

        if lines:
            try:
                di_position = lines.index('di')
                # Converte posição para letra (A=0, B=1, C=2, etc)
                return chr(65 + di_position)
            except ValueError:
                pass

        return None

    def _extract_comment_answer(self, item: str) -> Optional[str]:
        """Extrai resposta de comentários (método alternativo)."""
        comment_match = re.search(r'%\s*([VF])\s*$', item, re.MULTILINE)
        if comment_match:
            return comment_match.group(1)
        return None


class CSVExporter:
    """Exportador de respostas para formato CSV."""

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def export(self, answers: List[Answer]) -> None:
        """Exporta as respostas para um arquivo CSV."""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                for answer in answers:
                    f.write(answer.to_csv_line())

            print(f"\nGabarito salvo com sucesso em: {self.output_path}")
            print(f"Total de questões processadas: {len(answers)}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            sys.exit(1)


class AnswerKeyGenerator:
    """Gerador principal de gabarito."""

    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_path = Path(input_file)
        self.output_path = Path(output_file)

    def run(self) -> None:
        """Executa o processo completo de geração do gabarito."""
        # Lê o arquivo LaTeX
        latex_content = self._read_latex_file()

        # Processa o conteúdo
        print("\nProcessando questões...")
        parser = LatexParser(latex_content)
        answers = parser.parse()

        if not answers:
            print("Nenhuma resposta foi encontrada no arquivo.")
            sys.exit(1)

        # Exporta para CSV
        exporter = CSVExporter(self.output_path)
        exporter.export(answers)

        # Exibe preview
        self._show_preview(answers)

    def _read_latex_file(self) -> str:
        """Lê o conteúdo do arquivo LaTeX."""
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.input_path}' não encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            sys.exit(1)

    def _show_preview(self, answers: List[Answer]) -> None:
        """Exibe um preview das respostas."""
        print("\nPreview das primeiras 10 respostas:")
        for answer in answers[:10]:
            print(f"  {answer.to_csv_line().strip()}")

        if len(answers) > 10:
            print(f"  ... e mais {len(answers) - 10} questões")


def get_user_input(prompt: str, default: str) -> str:
    """Solicita entrada do usuário com valor padrão."""
    user_input = input(f"{prompt} (padrão: {default}): ").strip()
    return user_input if user_input else default


def main() -> None:
    """Função principal."""
    # Solicita os caminhos dos arquivos
    input_file = get_user_input(
        "Digite o caminho do arquivo LaTeX",
        "P1A.tex"
    )

    output_file = get_user_input(
        "Digite o nome do arquivo CSV de saída",
        "P1A.csv"
    )

    # Executa o gerador
    generator = AnswerKeyGenerator(input_file, output_file)
    generator.run()


if __name__ == "__main__":
    main()
