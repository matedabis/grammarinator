grammar assignmentSequence;

@header {
import random
random.seed(1)
}

@lexer::header {
import random
random.seed(1)
}

@parser::member {
var_idx = 0

def get_varname(self):
    self.var_idx += 1
    return 'var_%d' % self.var_idx

}

@lexer::member {
call_count = 0
loop_count = 0

def get_varname_lefthand(self):
    return 'var_%d' % random.randint(1, 5)

def get_loop_varname(self):
    if self.call_count % 3 == 0:
      self.loop_count += 1
    self.call_count += 1
    return 'loop_count_%d' % self.loop_count
}

assignmentSequence
: declaration declaration declaration declaration declaration 'print(' AssignmentExpression ');'
;

AssignmentExpression
 : 'Math.round(' LeftHandSideExpression AssignmentOperator '(' AssignmentExpression '))'
 | 'Math.round(' LeftHandSideExpression AssignmentOperator DecimalIntegerLiteral ')'
 ;

LeftHandSideExpression
 : {current += self.create_node(UnlexerRule(name='varname', src=self.get_varname_lefthand()))}
 ;

AssignmentOperator
 : '*='
 | '/='
 | '%='
 | '+='
 | '-='
 | '<<='
 | '>>='
 | '>>>='
 | '&='
 | '^='
 | '|='
 | '='
 ;

declaration: 'var ' {current += self.create_node(UnlexerRule(name='varname', src=self.get_varname()))} assignment? ';' '\n' ;
declaration_wo_semicolon_o_var: {current += self.create_node(UnlexerRule(name='varname', src=self.get_varname()))} assignment?;
assignment : '=' singleExpression ;

singleExpressionTest
 : 'print(' singleExpression ');'
 ;

DecimalIntegerLiteralTest
 : 'print(' DecimalIntegerLiteral ');'
 ;

 singleExpression
 : {5}? singleExpression '+' singleExpression
 | {5}? singleExpression '-' singleExpression
 | {5}? '(' '~' singleExpression ')'
 | {5}? '(' '!' singleExpression ')'
 | {5}? singleExpression '*' singleExpression
 | {5}? 'Math.round(' singleExpression '/' singleExpression ')'
 | {5}? 'Math.round(' singleExpression '%' singleExpression ')'
 | {5}? singleExpression '+' singleExpression
 | {5}? singleExpression '-' singleExpression
 | {5}? singleExpression '<<' singleExpression
 | {5}? singleExpression '>>' singleExpression
 | {5}? singleExpression '>>>' singleExpression
 | {5}? singleExpression '<'  singleExpression
 | {5}? singleExpression '>'  singleExpression
 | {5}? singleExpression '<=' singleExpression
 | {5}? singleExpression '>=' singleExpression
 | {5}? singleExpression '==' singleExpression
 | {5}? singleExpression '!=' singleExpression
 | {5}? singleExpression '===' singleExpression
 | {5}? singleExpression '!==' singleExpression
 | {5}? singleExpression '&' singleExpression
 | {5}? singleExpression '^' singleExpression
 | {5}? singleExpression '|' singleExpression
 | {5}? singleExpression '&&' singleExpression
 | {5}? singleExpression '||' singleExpression
 | {5}? '(' singleExpression ')'
 | {10}? DecimalIntegerLiteral
 | {1}? 'null'
 | {1}? 'true'
 | {1}? 'false'
 | {1}? 'undefined'
 ;

 fragment DecimalIntegerLiteral
 : '0'
 | [1-9] DecimalDigit*
 ;

 fragment DecimalDigit
 : [0-9]
 ;


 expressionSequence
  : singleExpression
  ;

 statement
  : expressionStatement
  | declaration
  | ifStatement
  | iterationStatement
  | variableStatement
  | ';'
  ;

ifStatement
 : If '(' expressionSequence ')' '{' statement '}\n' ( ' ' Else ' {' statement '}' )?
 ;

variableStatement
 : Var ' ' (declaration_wo_semicolon_o_var ', ')* declaration_wo_semicolon_o_var ';'
 ;

   /* | block
   | continueStatement
   | breakStatement
   | withStatement
   | labelledStatement
   | switchStatement
   | throwStatement
   | tryStatement
   | debuggerStatement */

 expressionStatement
  : expressionSequence ';'
  ;

 iterationStatementTest
  : iterationStatement Print_loop
  ;

iterationStatement
 : Loop_count_declaration Do '{' Safety_break statement '}' While '(' expressionSequence ')' # DoStatement
 | Loop_count_declaration While '(' expressionSequence ')' '{' Safety_break statement '}' # WhileStatement
 | Loop_count_declaration For '(' expressionSequence? ';' expressionSequence? ';' expressionSequence? ')' '{' Safety_break statement '}' # ForStatement
 | Loop_count_declaration declaration declaration  For '('  'var_1 ' In ' var_2' ')' '{' Safety_break statement '}' # ForInStatement
 | Loop_count_declaration For '(' Var ' ' declaration_wo_semicolon_o_var ' ' In ' ' expressionSequence ')' '{' Safety_break statement '}' # ForVarInStatement
 | Loop_count_declaration For '(' Var ' ' (declaration_wo_semicolon_o_var ', ')* declaration_wo_semicolon_o_var ';' expressionSequence? ';' expressionSequence? ')' '{'Safety_break statement'}' # ForVarStatement
 | Loop_count_declaration Do '{' Safety_break statement '}' While '(' expressionSequence ')' # DoStatement
 ;

/* iterationStatement
 ; */

 /// 7.6.1.1 Keywords
 Break      : 'break';
 Do         : 'do';
 Instanceof : 'instanceof';
 Typeof     : 'typeof';
 Case       : 'case';
 Else       : 'else';
 New        : 'new';
 Var        : 'var';
 Catch      : 'catch';
 Finally    : 'finally';
 Return     : 'return';
 Void       : 'void';
 Continue   : 'continue';
 For        : 'for';
 Switch     : 'switch';
 While      : 'while';
 Debugger   : 'debugger';
 Function   : 'function';
 This       : 'this';
 With       : 'with';
 Default    : 'default';
 If         : 'if';
 Throw      : 'throw';
 Delete     : 'delete';
 In         : 'in';
 Try        : 'try';
 /// Added keywords
 Loop_count_declaration : 'var ' {current += self.create_node(UnlexerRule(name='Loop_count_declaration', src=self.get_loop_varname()))} ' = 0;\n';
 Safety_break : '\n' {current += self.create_node(UnlexerRule(name='Loop_count_declaration', src=self.get_loop_varname()))} '++;\nif(' {current += self.create_node(UnlexerRule(name='Loop_count_declaration', src=self.get_loop_varname()))} '> 1000) break;\n';
 Print_loop : '\nprint(loop_count_1)';

/* Identifier
 : IdentifierStart IdentifierPart*
 ;

variableDeclarationList
 : variableDeclaration ( ',' variableDeclaration )*
 ;

variableDeclaration
 : Identifier initialiser?
 ;

initialiser
 : '=' singleExpression
 ; */
