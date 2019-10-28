from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol


class LispTransformer(InlineTransformer):
	def start(self, expr): 
		return expr
		
	def list(self, *expr):
		return list(expr)
		
	def atom(self, token):
		try:
			return int(token)
		except ValueError:
			try:
				return float(token)
			except ValueError:
				if(str(token) == '#t'):
					return True
				if(str(token) == '#f'):
					return False
					
				if(token.type == 'STRING'):
					return r"{}".format(str(token)[1:-1])
					
				return Symbol(str(token))

def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()