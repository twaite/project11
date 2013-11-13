import re

class CompilationEngine:

	def __init__(self, ifilename, ofilename):

		try:
			self.ifile = open(ifilename, 'r')
		except:
			print ("Error opening %s for reading" %ifilename)
			exit (1)

		try:
			self.ofile = open(ofilename, 'w+')
		except:
			print ("Error opening %s for writing" %ofilename)
			exit (1)

		self.token_string = self.ifile.read()
		self.token = ""
		self.tag = ""
		self.tab_amount = 0;

	def advance(self):
		self.token = ""
		while ( not re.search('\n', self.token, re.DOTALL) ):
			self.token = self.token + self.token_string[0]
			self.token_string = self.token_string[1:len(self.token_string)]

		self._separate_tag_and_token()
		self.token = re.sub('\n', '', self.token)

	def compile_class(self):

		#tokens
		self.advance()
		self._write_open_tag("class")
		self._tab_inc()

		#class keyword
		self.advance()
		self._write_token()

		#Write class name
		self.advance()
		self._write_token()

		#write opening bracket
		self.advance()
		self._write_token()

		# print("before check")

		#write subroutine or class vars
		while ( True ):
			self.advance()

			if (self.token == "function" 
				or self.token == "constructor"
				or self.token == "method"):
				self.compile_subroutine()

			elif (self.token == "field"):
				self.compile_class_var_dec()

			else:
				break;

		# print("after check"

		#close bracket
		self._write_token()

		self._tab_dec()
		self._write_close_tag("class")

	def compile_class_var_dec(self):

		self._write_open_tag("classVarDec")
		self._tab_inc()

		while (self.token != ';'):
			self._write_token()
			self.advance()

		self._write_token()

		self._tab_dec()
		self._write_close_tag("classVarDec")

	def compile_subroutine(self):

		self._write_open_tag("subroutineDec")
		self._tab_inc()

		#function keyword
		self._write_token()

		#return type
		self.advance()
		self._write_token()

		#name
		self.advance()
		self._write_token()

		#open parenthesis
		self.advance()
		self._write_token()

		#compile the parameters
		self.advance()
		self.compile_parameter_list()

		#close the parenthesis
		self._write_token()

		#subroutine body
		self._write_open_tag("subroutineBody")
		self._tab_inc()

		#write open bracket
		self.advance()
		self._write_token()

		#compile the var declarations
		self.advance()
		while (self.token == "var"):
			self.compile_var_dec()
			self.advance()

		#compile the statements
		self.compile_statements()

		#close the bracket
		self.advance()
		self._write_token()

		self._tab_dec()
		self._write_close_tag("subroutineBody")

		self._tab_dec()
		self._write_close_tag("subroutineDec")

	def compile_parameter_list(self):
		self._write_open_tag("parameterList")
		self._tab_inc()

		while (self.token != ")"):
			self._write_token()
			self.advance()

		self._tab_dec()
		self._write_close_tag("parameterList")

	def compile_var_dec(self):
		self._write_open_tag("varDec")
		self._tab_inc()

		# print self.token

		while (self.token != ";"):
			self._write_token()
			self.advance()

		self._write_token()

		self._tab_dec()
		self._write_close_tag("varDec")

	def compile_statements(self):

		self._write_open_tag("statements")
		self._tab_inc()

		while (self.token != "return"):

			if (self.token == "}"):
				break;

			if (self.token == "do"):
				self.compile_do()

			if (self.token == "let"):
				self.compile_let()

			if (self.token == "if"):
				self.compile_if()

			if (self.token == "while"):
				self.compile_while()

			self.advance()

		if (self.token == "return"):
			self.compile_return()

		self._tab_dec()
		self._write_close_tag("statements")

	def compile_while(self):

		self._write_open_tag("whileStatement")
		self._tab_inc()

		while (self.token != ";"):
			self._write_token()
			self.advance()

			if (self.token == "("):
				self._write_token()
				self.advance()
				self.compile_expression()

			if (self.token == "{"):
				self._write_token()
				self.advance()
				self.compile_statements()

			if (self.token == "}"):
				self._write_token()
				break;

		self._tab_dec()
		self._write_close_tag("whileStatement")

	def compile_if(self):

		self._write_open_tag("ifStatement")
		self._tab_inc()

		while (self.token != ";"):
			self._write_token()
			self.advance()

			if (self.token == "("):
				self._write_token()
				self.advance()
				self.compile_expression()

			if (self.token == "{"):
				self._write_token()
				self.advance()
				self.compile_statements()

			if (self.token == "}"):
				self._write_token()
				break;

		self._tab_dec()
		self._write_close_tag("ifStatement")

	def compile_do(self):

		self._write_open_tag("doStatement")
		self._tab_inc()

		while (self.token != ";"):
			self._write_token()
			self.advance()

			if (self.token == "("):
				self._write_token()
				self.advance()
				self.compile_expression_list()
		#write semicolon
		self._write_token()

		self._tab_dec()
		self._write_close_tag("doStatement")

	def compile_let(self):

		self._write_open_tag("letStatement")
		self._tab_inc()

		while (self.token != ";"):
			self._write_token()
			self.advance()

			if (self.token == "["):
				self._write_token()
				self.advance()
				self.compile_expression()

			if (self.token == "="):
				self._write_token()
				self.advance()
				self.compile_expression()

		self._write_token()

		self._tab_dec()
		self._write_close_tag("letStatement")

	def compile_expression(self):

		self._write_open_tag("expression")
		self._tab_inc()

		#print (self.token)
		while (True):
			if (self.token == ";"):
				break;
			elif (self.token == ","):
				break;
			elif (self.token == ")"):
				break;
			elif (self.token == "]"):
				break;
			elif (self.token == "+" 
					or self.token == "-"
					or self.token == "&gt;"
					or self.token == "&lt;"
					or self.token == "&amp;"
					or self.token == "="):
				self._write_token()
				self.advance()
			else:
				self.compile_term()

		#print (self.token)

		self._tab_dec()
		self._write_close_tag("expression")

	def compile_term(self):

		self._write_open_tag("term")
		self._tab_inc()

		if (self.token != "("
				and self.token != "~"
				and self.token != "["):
			self._write_token()
			self.advance()

		if (self.token == "."):
			while (self.token != ";"):
				self._write_token()
				self.advance()

				if (self.token == "("):
					self._write_token()
					self.advance()
					self.compile_expression_list()

				if (self.token == "+"):
					return None

		if (self.token == "("
			or self.token == "["):
			self._write_token()
			self.advance()
			self.compile_expression()
			self._write_token()
			self.advance()

		if (self.token == "~"):
			self._write_token()
			self.advance()
			self.compile_term()

		self._tab_dec()
		self._write_close_tag("term")

	def compile_return(self):

		self._write_open_tag("returnStatement")
		self._tab_inc()

		#write return
		self._write_token()
		self.advance()

		if (self.token != ';'):
			self.compile_expression()

		self._write_token()

		self._tab_dec()
		self._write_close_tag("returnStatement")

	def compile_expression_list(self):

		self._write_open_tag("expressionList")
		self._tab_inc()

		while (self.token != ")"):
			if (self.token == ","):
				self._write_token()
				self.advance()
			else:
				self.compile_expression()

		self._tab_dec()
		self._write_close_tag("expressionList")

	def _write_tabs(self):
		for i in range(self.tab_amount):
			self.ofile.write("  ")

	def _tab_inc(self):
		self.tab_amount = self.tab_amount + 1

	def _tab_dec(self):
		self.tab_amount = self.tab_amount - 1

	def _write_open_tag(self, tag):
		self._write_tabs()
		self.ofile.write("<%s>\n" % tag)

	def _write_close_tag(self, tag):
		self._write_tabs()
		self.ofile.write("</%s>\n" % tag)

	def _separate_tag_and_token(self):
		self.tag = self.token[1:self.token.index('>')]

		if (self.tag == "tokens"):
			return None

		tok_i_one = self.token.index('>') + 2
		tok_i_two = self.token.index('/') - 2
		self.token = self.token[tok_i_one:tok_i_two]

	def _write_token(self):
		self._write_tabs()
		self.ofile.write("<%s> %s </%s>\n" % (self.tag, self.token, self.tag))
