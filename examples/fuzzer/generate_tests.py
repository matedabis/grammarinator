#!/usr/bin/env python3

#!/usr/bin/env python
import sys
import os
import argparse
import subprocess
import glob
import re

# Utility function for sorting
def natural_keys(text):
    return [ convert_if_int(c) for c in re.split('(\d+)', text) ]

def convert_if_int(text):
    return int(text) if text.isdigit() else text


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
        self.bash_command += " -o %s/grammarinator_tests_%%d.js -n %d" % (options.test_folder, options.test_count)
        print("\n" + self.bash_command + "\n")
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

    # Create test cases for V8 with print statements
    def make_print_statements(self, options):
        test_count = 0 # Counter for v8_test filename
        # For all the files in the test folder if it is a grammarinator generated test
        for file in os.listdir(options.test_folder):
             filename = os.fsdecode(file)
             if filename.startswith("grammarinator_tests_"):
                 test_count += 1
                 # Open grammarinator generated test
                 with open (os.path.join(options.test_folder, file)) as grammarinator_testfile:
                    data = grammarinator_testfile.read()
                    # Write first half of JerryScript tests
                    with open (os.path.join(options.test_folder, "jerry_test_%d.js" % test_count), "w") as jerry_test:

                         jerry_test.write("assert((%s" % data)
                    # Write V8 testfile
                    v8_testfile = os.path.join(options.test_folder, "v8_test_%d.js" % test_count)
                    with open (os.path.join(v8_testfile), "w") as v8_test:
                        v8_test.write("print(%s);" % data)

    def validate_in_v8(self, options):
        test_count = 0 # Counter for v8_test filename
        # For all the files in the test folder if it is a grammarinator generated test
        os.chdir(options.test_folder)
        v8_test_files = glob.glob("v8_test_*.js") # Files to test
        v8_test_files.sort(key = natural_keys)
        print(v8_test_files)
        os.chdir(os.path.join(self.this_dir, "../.."))
        for file in v8_test_files:
             test_count += 1
             with open (os.path.join(options.test_folder, "jerry_test_%d.js" % test_count), "a") as jerry_test:
                 self.bash_command = "%s %s" % (options.v8_location, os.path.join(options.test_folder, file))
                 # os.path.join(options.test_folder, "jerry_test_%d.js" % test_count)
                 print("\n" + self.bash_command + "\n")
                 result = subprocess.check_output(self.bash_command.split()) # Executing the command
                 if result.decode('utf-8').strip() == "NaN":
                     jerry_test.write(") !== ")
                 else:
                     jerry_test.write(") === ")
                 jerry_test.write("%s);" % result.decode('utf-8').strip())
                 print(result.decode('utf-8').strip())




    def run_tests_in_jerry(self, options):
        self.runtestpy = os.path.join(self.this_dir, "runtests.py")
        self.bash_command = "%s --engine-location %s --test-folder %s" % (self.runtestpy, options.jerry_location,
        options.test_folder)
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

    # Generate tests
    def generate_tests(self, options):
        # Generate grammarinator tests
        self.run_grammarinator(options)
        # Make print statements to make V8 output capturable
        self.make_print_statements(options)
        # Evaluate tests in v8, and create JerryScript tests according to the output
        self.validate_in_v8(options)
        # Run the generated tests in JerryScript
        self.run_tests_in_jerry(options)

def main():
    generator = GenerateTests()
    generator.generate_tests(generator.get_arguments())

if __name__ == '__main__':
    main()