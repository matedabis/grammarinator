#!/usr/bin/env python3

import sys
import os
import subprocess
import glob
import re
import datetime

# Local imports
import argparse
import runtests
from colors import _bcolors

# Class for generating grammar based tests
class GenerateTests:
    def __init__(self):
        self.fail_count = 0
        self.pass_count = 0
        self.fuzzer_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.normpath(os.path.join(self.fuzzer_dir, "..", ".."))
        self.test_folder = os.path.normpath(os.path.join(self.project_dir, "examples", "tests"))
        self.failed_folder = os.path.normpath(os.path.join(self.project_dir, "examples", "failed"))

    # Getting the arguments
    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--grammar-files", help = "the location of the grammar file(s)", required = True)
        parser.add_argument("--starter-element", help = "Element(s) of grammar to generate", nargs = '+',
        required = True)
        parser.add_argument("--test-count", help = "Number of tests to generate per starter element", type = int,
        default = 50)
        parser.add_argument("--depth-count", help = "Number of tests to generate", type = int,
        default = 20)
        parser.add_argument("--unlex-unpar-loc", help = "the folder to unlexer and unparser",
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

    # Run grammarinator process (generate unlexer and unparser)
    def run_grammarinator_process(self, options):
        self.debug(options.grammar_files, options)
        options.grammar_files = os.path.abspath(options.grammar_files)
        # Variables
        self.debug("\n" + options.grammar_files + "\n", options)
        self.grammar_name = options.grammar_files.split(".g4")[0].split("/")[-1]
        self.unlexer = os.path.join(self.fuzzer_dir, "%sUnlexer.py" % (self.grammar_name))
        self.debug("\n" + self.unlexer + "\n", options)
        self.unparser = os.path.join(self.fuzzer_dir, "%sUnparser.py" % (self.grammar_name))

        # Generating unlexer and unparser
        self.bash_command = "grammarinator-process %s -o %s" % (options.grammar_files, options.unlex_unpar_loc)
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

    # Run grammarinator generate (generate grammarinator tests)
    def run_grammarinator_generate(self, options):
        # Generating test cases
        for start_element in options.starter_element:
            self.bash_command = "grammarinator-generate -l %s -p %s -r %s -d %d" % (self.unlexer, self.unparser,
            start_element, options.depth_count)
            self.bash_command += " -o %s/grammarinator_tests_%%d.js -n %d" % (self.test_folder, options.test_count)
            self.debug("\n" + self.bash_command + "\n", options)
            self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
            self.process.communicate() # Waiting for process to terminate

    # Create test cases for V8 with print statements
    def make_print_statements(self, options):
        test_count = 0 # Counter for v8_test filename
        # For all the files in the test folder if it is a grammarinator generated test
        for file in os.listdir(self.test_folder):
             filename = os.fsdecode(file)
             if filename.startswith("grammarinator_tests_"):
                 test_count += 1
                 # Open grammarinator generated test
                 with open (os.path.join(self.test_folder, file)) as grammarinator_testfile:
                    data = grammarinator_testfile.read()
                    # Write first half of JerryScript tests
                    with open (os.path.join(self.test_folder, "jerry_test_%d.js" % test_count), "w") as jerry_test:

                         jerry_test.write("assert((")
                    # # Write V8 testfile
                    # v8_testfile = os.path.join(self.test_folder, "v8_test_%d.js" % test_count)
                    # with open (v8_testfile, "w") as v8_test:
                    #     v8_test.write("print(%s);" % data)

    def validate(self, options):
        test_count = 0 # Counter for jerry_test filename
        # For all the files in the test folder if it is a grammarinator generated test
        # Change to test directory
        os.chdir(self.test_folder)

        v8_test_files = glob.glob("grammarinator_tests_*.js") # Files to test
        v8_test_files.sort(key = runtests.natural_keys)

        # Change back to project directory
        os.chdir(self.project_dir)

        for file in v8_test_files:
             test_count += 1
             with open (os.path.join(self.test_folder, "jerry_test_%d.js" % test_count), "a") as jerry_test:

                 # Calculate in v8
                 self.bash_command = "%s %s" % (options.v8_location, os.path.join(self.test_folder, file))
                 self.debug("\n" + self.bash_command + "\n", options)
                 result_v8 = subprocess.check_output(self.bash_command.split()) # Executing the command

                 # Calculate in JerryScript
                 self.bash_command = "%s %s" % (options.jerry_location, os.path.join(self.test_folder, file))
                 self.debug("\n" + self.bash_command + "\n", options)
                 result_jerry = subprocess.check_output(self.bash_command.split()) # Executing the command
                 jerry_test.write("%s" % result_jerry.decode('utf-8').strip())
                 if result_v8.decode('utf-8').strip() == "NaN":
                     jerry_test.write(") !== ")
                 else:
                     jerry_test.write(") === ")
                 jerry_test.write("%s);" % result_v8.decode('utf-8').strip())
                 self.debug(result_v8.decode('utf-8').strip(), options)
                 self.debug(result_jerry.decode('utf-8').strip(), options)

    def run_tests_in_jerry_and_collect_failed_tests(self, options):
        # Run tests in JerryScript
        run_data = runtests.run_tests(options)
        failed_filenames = run_data["failed_filenames"]
        # If there are failed tests
        if len(failed_filenames):
            # If there is no failed folder, create one
            if not os.path.isdir(self.failed_folder):
                os.makedirs(self.failed_folder)

            file_count = 0
            # Iterate trough files
            for file in os.listdir(self.test_folder):
                file_count += 1
                filename = os.fsdecode(file)
                # If it is a failed test
                if filename in failed_filenames:
                    # Open it and read data
                    with open (os.path.join(self.test_folder, filename), "r") as failed:
                        data = failed.read()
                        # And copy it to a time marked .js file
                        with open (os.path.join(self.failed_folder,
                        "%s.js") % datetime.datetime.now().isoformat(), "w") as failed_test:
                            failed_test.write(data)
        # Return pass and fail count
        return [run_data["pass"], run_data["fail"]]

    def remove_test_dir(self, options):
        # Remove test directory
        self.debug(self.test_folder, options)
        self.bash_command = "rm -r %s" % os.path.abspath(self.test_folder)
        self.debug(self.bash_command.split(), options)
        self.process = subprocess.Popen(self.bash_command.split()) # Executing the command
        self.process.communicate() # Waiting for process to terminate

    # Generate tests
    def generate_tests(self, options):
        # While all tests pass
        loop_count = 0
        # Generate unlexer and unparser
        self.run_grammarinator_process(options)
        # The process runs as long as we want it to run
        while True:
            loop_count += 1
            # Generate grammarinator tests
            self.run_grammarinator_generate(options)
            # Make print statements to make V8 output capturable
            self.make_print_statements(options)
            # Evaluate tests in v8, and create JerryScript tests according to the output
            self.validate(options)
            # Run the generated tests in JerryScript and update counters
            test_counts = self.run_tests_in_jerry_and_collect_failed_tests(options)
            self.pass_count += test_counts[0]
            self.fail_count += test_counts[1]
            # Remove test directory
            self.remove_test_dir(options)
            # Print information about completed tests
            print("\n%sTest count:\t%d%s" % (_bcolors.okblue, self.pass_count + self.fail_count, _bcolors.endc))
            pass_percentage = (self.pass_count * 100.0) / (self.pass_count + self.fail_count)
            fail_percentage = (self.fail_count * 100.0) / (self.pass_count + self.fail_count)
            print("%sPass count:\t%d\t%f %%%s" % (_bcolors.okgreen, self.pass_count, pass_percentage, _bcolors.endc))
            print("%sFail count:\t%d\t%f %%%s" % (_bcolors.fail, self.fail_count, fail_percentage, _bcolors.endc))


def main():
    generator = GenerateTests()
    generator.generate_tests(generator.get_arguments())

if __name__ == '__main__':
    main()
