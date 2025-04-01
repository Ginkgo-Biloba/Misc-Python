# coding=utf_8
"""
递归下降解析器
"""
import collections
import re

# 符号规则
NUM = r"(?P<NUM>\d+)"
PLUS = r"(?P<PLUS>\+)"
MINUS = r"(?P<MINUS>\-)"
TIMES = r"(?P<TIMES>\*)"
DIVIDE = r"(?P<DIVIDE>\/)"
LPAREN = r"(?P<LPAREN>\()"
RPAREN = r"(?P<RPAREN>\))"
WS = r"(?P<WS>\s+)"

masterPat = re.compile(
    "|".join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))
Token = collections.namedtuple("Token", ["Type", "Value"])


def genTokens(text):
	scanner = masterPat.scanner(text)
	for m in iter(scanner.match, None):
		tok = Token(m.lastgroup, m.group())
		if (tok.Type != "WS"):
			yield tok

# 解析器

class ExpressionEvaluator:
	"""
	递归下降解析器。
	每个方法实现单一的语法规则。
	使用 ._accept() 方法以测试并接受当前开头的符号。
	使用 ._expect() 方法以精确匹配并丢弃下一个符号（或者在不匹配时抛出 SyntaxError）。
	"""

	def parse(self, text):
		self.tokens = genTokens(text)
		self.tok = None  # 最后用掉的符号
		self.nextTok = None
		self._advance()  # 加载往前第一个符号
		return self.expr()

	def _advance(self):
		"取出一个符号（并前进）"
		self.tok = self.nextTok
		self.nextTok = next(self.tokens, None)

	def _accept(self, tokType):
		"测试并用掉下一个符号，如果它匹配 tokType 的话"
		if (self.nextTok and self.nextTok.Type == tokType):
			self._advance()
			return True
		else:
			return False

	def _expect(self, tokType):
		"用掉下一个符号，如果它匹配 tokType，否则抛出 SyntaxError"
		if not (self._accept(tokType)):
			raise SyntaxError("Expected " + tokType)

	# 各个语法规则

	def expr(self):
		"expression ::= term {('+' | '-') term}*"
		exprVal = self.term()
		while (self._accept("PLUS") or self._accept("MINUS")):
			op = self.tok.Type
			rhs = self.term()
			if (op == "PLUS"):
				exprVal += rhs
			elif (op == "MINUS"):
				exprVal -= rhs
		return exprVal

	def term(self):
		"term ::= factor {('*' | '/') factor}*"
		termVal = self.factor()
		while (self._accept("TIMES") or self._accept("DIVIDE")):
			op = self.tok.Type
			rhs = self.factor()
			if (op == "TIMES"):
				termVal *= rhs
			elif (op == "DIVIDE"):
				termVal /= rhs
		return termVal

	def factor(self):
		"factor ::= NUM | (expr)"
		if (self._accept("NUM")):
			return int(self.tok.Value)
		elif (self._accept("LPAREN")):
			exprVal = self.expr()
			self._expect("RPAREN")
			return exprVal
		else:
			raise SyntaxError("Excepted NUMBER or LPAREN")

# 测试
if (__name__ == "__main__"):
	e = ExpressionEvaluator()
	print(e.parse("2"))
	print(e.parse("2 + 3"))
	print(e.parse("2 * 3 + 4"))
	print(e.parse("2 + (3 + 4) / 5"))
	print(e.parse("2 *+ (3 + 4)"))
