import re

class JackTokenizer:

	def __init__(self, ifilename):

		try:
			self.ifile = open(ifilename, 'r')
		except:
			print ("Error opening %s for reading" %ifilename)
			exit (1)

		ifilename = re.sub('.jack', '', ifilename)
		ofilename = ifilename + "Tm.xml"

		try:
			self.ofile = open(ofilename, 'w+')
		except:
			print ("Error opening %s for writing" %ofilename)
			exit (1)

		self.filestring = self.ifile.read()
		self.token = ""

		self.keywords = 'class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return'

		self.symbols = '\\{|\\}|\\(|\\)|\\[|\\]|\\.|\\,|\\;|\\+|\\-|\\*|\\/|\\&|\\||\\<|\\>|\\=|\\~'

		self.int_const = '[0-9]+[^0-9]'

		self.string_const = '\\".*\\"'

		self.identifiers = '^[A-Za-z_][0-9A-Za-z_]*[^0-9A-Za-z_]'

	def has_more_tokens(self):
		if ( len(self.filestring) > 0 ):
			return True
		return False

	def advance(self):
		self.token = ""
		while (not self.is_token(self.token) and (len(self.filestring) > 0)):
			self.token = self.token + self.filestring[0]
			self.filestring = self.filestring[1:]
			self.token = self.token.lstrip(' \n\t\r')

	def token_type(self):
		if (re.search(self.keywords, self.token)):
			return "KEYWORD"
		elif (re.search(self.int_const, self.token)):
			return "INT_CONST"
		elif (re.search(self.symbols, self.token)):
			return "SYMBOL"
		elif (re.search(self.string_const, self.token)):
			return "STRING_CONST"
		else:
			return "IDENTIFIER"

	def keyword(self):
		string = self.token
		if (re.search('class', string)):
			return "CLASS"
		elif (re.search('method', string)):
			return "METHOD"
		elif (re.search('function', string)):
			return "FUNCTION"
		elif (re.search('constructor', string)):
			return "CONSTRUCTOR"
		elif (re.search('int', string)):
			return "INT"
		elif (re.search('boolean', string)):
			return "BOOLEAN"
		elif (re.search('char', string)):
			return "CHAR"
		elif (re.search('void', string)):
			return "VOID"
		elif (re.search('var', string)):
			return "VAR"
		elif (re.search('static', string)):
			return "STATIC"
		elif (re.search('field', string)):
			return "FIELD"
		elif (re.search('let', string)):
			return "LET"
		elif (re.search('do', string)):
			return "DO"
		elif (re.search('if', string)):
			return "IF"
		elif (re.search('else', string)):
			return "ELSE"
		elif (re.search('while', string)):
			return "WHILE"
		elif (re.search('return', string)):
			return "RETURN"
		elif (re.search('true', string)):
			return "TRUE"
		elif (re.search('false', string)):
			return "FALSE"
		elif (re.search('null', string)):
			return "NULL"
		elif (re.search('this', string)):
			return "THIS"
		return "ERROR"

	def symbol(self):
		return self.token

	def identifier(self):
		return self.token

	def int_val(self):
		return self.token

	def string_val(self):
		return self.token

	def is_token(self, string):
		if (re.search(self.keywords, string)):
			return True
		elif (re.search(self.identifiers, string)):
			self.filestring = self.token[len(self.token) - 1] + self.filestring
			self.token = self.token[0:len(self.token)-1]
			return True
		elif (re.search(self.int_const, string)):
			self.filestring = self.token[len(self.token) - 1] + self.filestring
			return True
		elif (re.search(self.symbols, string)):
			return True
		elif (re.search(self.string_const,string)):
			return True

		return False

	def write_token_to_xml(self):
		tok = self.token
		tok_type = self.token_type().lower()

		tok = re.sub('"', '', tok)

		if (tok_type == "string_const"):
			tok_type = "stringConstant"
		elif (tok_type == "int_const"):
			tok_type = "integerConstant"
			tok = re.sub('[^0-9]', '', tok)

		if (tok == ""):
			return None
		elif (tok == '>'):
			tok = "&gt;"
		elif (tok == '<'):
			tok = "&lt;"
		elif (tok == '&'):
			tok = "&amp;"
		elif (tok == "print"):
			self.advance()
			tok = "print" + self.token
			tok_type = "identifier"

		self.ofile.write("<%s> %s </%s>\n" %(tok_type, tok, tok_type))


	# http://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
	def remove_comments(self, string):
		string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", string)
		string = re.sub(re.compile("//.*?\n"), "", string)
		return string


	def tokenize(self):
		self.filestring = self.remove_comments(self.filestring)

		self.ofile.write("<tokens>\n")
		while (self.has_more_tokens()):
			self.advance()
			self.write_token_to_xml()
		self.ofile.write("</tokens>\n")
		self.ofile.close()

