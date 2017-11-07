/*
 * Copyright (c) 2018 Renata Hodovan, Akos Kiss.
 *
 * Licensed under the BSD 3-Clause License
 * <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
 * This file may not be copied, modified, or distributed except
 * according to those terms.
 */

/*
 * This test checks whether the labeled alternatives are handled correctly.
 *
 * Note:
 *  - Because this test generates multiple outputs files, it exercises both
 *    single-process (`-j 1`) and multi-process (`-j N`) modes of generator.
 */

// TEST-PROCESS: {grammar}.g4 -o {tmpdir}
// TEST-GENERATE: -p {grammar}Unparser -l {grammar}Unlexer -r start -j 1 -n 5 -o {tmpdir}/{grammar}S%d.txt
// TEST-GENERATE: -p {grammar}Unparser -l {grammar}Unlexer -r start -j 2 -n 5 -o {tmpdir}/{grammar}M%d.txt
// TEST-ANTLR: {grammar}.g4 -o {tmpdir}
// TEST-PARSE: -p {grammar}Parser -l {grammar}Lexer -r start {tmpdir}/{grammar}S%d.txt
// TEST-PARSE: -p {grammar}Parser -l {grammar}Lexer -r start {tmpdir}/{grammar}M%d.txt

grammar LabeledAlternatives;

start
    : Hello World           # HelloAlternative
    | Grammarinator Rulez   # GrammarinatorAlternative
    ;

Hello : 'hello' ;

World : 'world' ;

Grammarinator : 'grammarinator' ;

Rulez : 'rulez' ;
