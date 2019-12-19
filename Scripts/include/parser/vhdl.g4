/**
 * @ Author: Your name
 * @ Create Time: 2019-12-19 14:48:25
 * @ Modified by: Your name
 * @ Modified time: 2019-12-19 15:08:09
 * @ Description:
 */

grammar vhdl;

// vhd_file : header entity body EOF;

// header : line;
// line : 


// TOKENS

file: header+ entity;

// HEADER
header : headline+;
headline : library
         | use
         | TEXT
         | headline Comment
         | Comment
         ;

library : 'library' TEXT ';';

use : 'use' libName ';';

libName : libName '.' TEXT
        | TEXT
        ;

// ENTITY
entity : 'entity' entity_name 'is' generic? port 'end' entity_name ';';
generic : 'generic' '(' gen_decl+ ')' ';';
port : 'port' '(' port_decl+ ')' ';';

entity_name : TEXT;

gen_decl : signalList ':' sig_type
          | gen_decl ':=' value
          | gen_decl ';'
          ;

port_decl : signalList ':' sig_direction sig_type
          | signalList ':' sig_direction sig_type ':=' value
          | port_decl ';'
          ;


signalList : TEXT
           | signalList ',' TEXT
           ;

sig_direction : ('in' | 'out');

sig_type : 'integer'
         | 'std_logic'
         | 'std_logic_vector' '(' size 'downto' size ')'
         ;

size : NUMBER
     | TEXT
     | size OPERAND size
     ;

value : NUMBER
      | BIT
      | BITSTRING
      ;

//architecture : 'architecture' TEXT 'of' entity_name 'is' .* 'end;';

Comment
  :  '--' ~( '\r' | '\n' )*
  ;

NUMBER : [0-9]+;
BITSTRING : '"' [0-1]+ '"';
BIT : '\'' [0-1] '\'';
TEXT : [a-zA-Z0-9_]+;
OPERAND : ('/' | '*' | '-' | '+');
WS: [ \n\t\r]+ -> skip;