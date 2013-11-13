import sys, os, re
import JackTokenizer
import CompilationEngine

class JackAnalyzer():

	def __init__(self):
		self.filename = sys.argv[1]

	def parseFiles(self):

		if (os.path.isdir(self.filename)):

			for filename in os.listdir(self.filename):

				if ( re.search('.jack', filename) ):
					tokenizer = JackTokenizer.JackTokenizer(self.filename + '/' + filename)
					tokenizer.tokenize()

				if ( re.search('Tm.xml', filename) ):
					ifilename = self.filename + '/' + filename
					parser = CompilationEngine.CompilationEngine(ifilename, self.get_xml_filename(ifilename))
					parser.compile_class()

		elif ( re.search('.jack', self.filename) ):

			tokenizer = JackTokenizer.JackTokenizer(self.filename)
			tokenizer.tokenize()

			tok_file_name = re.sub('.jack', 'Tm.xml', self.filename)

			parser = CompilationEngine.CompilationEngine(self.filename, self.get_xml_filename(self.filename))
			parser.compile_class()

		else:

			print ("Not a valid file or directory")

	def get_xml_filename(self, filename):
		return re.sub('Tm.xml', 'm.xml', filename)

def main():
	jack = JackAnalyzer()
	jack.parseFiles()

main()