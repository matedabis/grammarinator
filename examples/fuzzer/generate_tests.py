#!/usr/bin/env python3

#!/usr/bin/env python
import sys
import os
import argparse
import subprocess
import glob

# Class for generating grammar based tests
class GenerateTests:

    # Getting the arguments
    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--grammar-files", help = "the location of the grammar file(s)", required = True)
        parser.add_argument("--starter-element", help = "Element of grammar to generate", required = True)
        parser.add_argument("--test-count", help = "Number of tests to generate", type = int,
        default = 50)
        parser.add_argument("--depth-count", help = "Number of tests to generate", type = int,
        default = 20)
        parser.add_argument("--unlex-unpar-loc", help = "the folder to unlexer and unparser",
        required = True)
        parser.add_argument("--test-folder", help = "the folder to generate tests",
        required = True)
        parser.add_argument("--v8-location", help = "the location of the V8 engine",
        required = True)
        parser.add_argument("--jerry-location", help = "the location of the JerryScript project folder",
        required = True)
        parser.add_argument("-q", help = "Does not print any output", action='store_true')

        # If no arguments given print help and exit
        if len(sys.argv) <= 1:
            parser.print_help()
            sys.exit(1)

        return parser.parse_args()

    # Printing debug messages
    def debug(self, message, options):
        if (not options.q):
            print(message)

    # Run grammarinator
    def run_grammarinator(self, options):

        # Variables
        print("\n" + options.grammar_files + "\n")
        self.this_dir = (os.path.dirname(os.path.realpath(__file__)))
        self.grammar_name = options.grammar_files.split(".g4")[0].split("/")[-1]
        self.unlexer = os.path.join(self.this_dir, "%sUnlexer.py" % (self.grammar_name))
        print("\n" + self.unlexer + "\n")
        self.unparser = os.path.join(self.this_dir, "%sUnparser.py" % (self.grammar_name))

        # Generating unlexer and unparser
        self.bash_command = "grammarinator-process %s -o %s --no-actions" % (options.grammar_files, options.unlex_unpar_loc)
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

        # Generating test cases
        self.bash_command = "grammarinator-generate -l %s -p %s -r %s -d %d" % (self.unlexer, self.unparser,
        options.starter_element, options.depth_count)
        self.bash_command += " -o ./examples/tests/grammarinator_tests_%%d.js -n %d" % (options.test_count)
        print("\n" + self.bash_command + "\n")
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

    # Generate tests
    def generate_tests(self, options):
        # Building JerryScript if needed
        self.run_grammarinator(options)


def main():
    generator = GenerateTests()
    generator.generate_tests(generator.get_arguments())

if __name__ == '__main__':
    main()
