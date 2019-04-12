grammar singleExpression;

singleExpression
 : {5}? singleExpression '+' singleExpression                                                   /// UnaryPlusExpression
 | {5}? singleExpression '-' singleExpression                                                   /// UnaryMinusExpression
 | {5}? '(' '~' singleExpression ')'                    /// BitNotExpression
 | {5}? '(' '!' singleExpression ')'                    /// NotExpression
 | {5}? singleExpression '*' singleExpression
 | {5}? singleExpression '/' singleExpression
 | {5}? singleExpression '%' singleExpression           /// MultiplicativeExpression
 | {5}? singleExpression '+' singleExpression
 | {5}? singleExpression '-' singleExpression           /// AdditiveExpression
 | {5}? singleExpression '<<' singleExpression
 | {5}? singleExpression '>>' singleExpression
 | {5}? singleExpression '>>>' singleExpression         /// BitShiftExpression
 | {5}? singleExpression '<'  singleExpression          /// RelationalExpression
 | {5}? singleExpression '>'  singleExpression          /// RelationalExpression
 | {5}? singleExpression '<=' singleExpression          /// RelationalExpression
 | {5}? singleExpression '>=' singleExpression          /// RelationalExpression
 | {5}? singleExpression '==' singleExpression
 | {5}? singleExpression '!=' singleExpression
 | {5}? singleExpression '===' singleExpression
 | {5}? singleExpression '!==' singleExpression           /// EqualityExpression
 | {5}? singleExpression '&' singleExpression             /// BitAndExpression
 | {5}? singleExpression '^' singleExpression             /// BitXOrExpression
 | {5}? singleExpression '|' singleExpression             /// BitOrExpression
 | {5}? singleExpression '&&' singleExpression            /// LogicalAndExpression
 | {5}? singleExpression '||' singleExpression            /// LogicalOrExpression
 | {5}? '(' singleExpression ')'                          /// ParenthesizedExpression
 | {10}? DecimalIntegerLiteral
 | {1}? 'null'
 | {1}? 'true'
 | {1}? 'false'
 | {1}? 'undefined'
 ;

 fragment DecimalIntegerLiteral
 : {1}? '0'
 | {10}? [1-9] DecimalDigit*
 ;

 fragment DecimalDigit
 : [0-9]
 ;
