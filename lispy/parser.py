from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol

class LispTransformer(InlineTransformer):
	def start(self, *args):
		if(len(args) == 1):
			return args[0]
		return [Symbol.BEGIN, *args]
		
	def value(self, *args):
		return list(args)
		
	def conditional(self, test, conseq, alt):
		return [test,  conseq, alt]
		
	def test(self, comparison, atom1, atom2):
		return [comparison, atom1, atom2]
		
	def definition(self, asymbol, exp):
		return ['define', asymbol, exp]
		
	def procedure(self, proc, *args):
		if(str(proc) in ('+', '-', '/', '*')):
			return [self.atom(proc), args[0], args[1]]
		return [self.atom(proc), list(args)]
		
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