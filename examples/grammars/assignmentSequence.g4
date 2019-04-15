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

def get_varname_lefthand(self):
    return 'var_%d' % random.randint(1, 5)
}

assignmentSequence
: declaration declaration declaration declaration declaration 'print(Math.round(' AssignmentExpression '));'
;

AssignmentExpression
 : LeftHandSideExpression AssignmentOperator '(' AssignmentExpression ')'
 | LeftHandSideExpression AssignmentOperator DecimalIntegerLiteral
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
