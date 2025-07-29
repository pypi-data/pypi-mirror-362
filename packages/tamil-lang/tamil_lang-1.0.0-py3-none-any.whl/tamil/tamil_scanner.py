#!/usr/bin/python
## -*- coding: utf-8 -*-
## 
## (C) 2008, 2013, 2015 Muthiah Annamalai
## Licensed under GPL Version 3
##
## This module is the scanner for the tamil language.
## It contains classes tamilLex.
## 

import re
from .scanner import Token, Lexeme, Lex, PYTHON3
from tamil.utf8 import has_tamil, istamil, istamil_alnum
from .errors import ScannerException

if PYTHON3:
    str = str

class tamilLexeme(Lexeme):
    """ tamil Lexeme - """ 
    def __init__(self,val,kind,fname=u""):
        Lexeme.__init__(self,val,kind,fname)
    
    def get_kind(self):
        return u"%s - %s"%(self.val,self.kind)
    
    def __str__(self):
        return u" %s [%s] Line=%d, Col=%d in File %s "% \
            (self.val,self.get_kind(), \
                self.line,self.col,self.fname)
    
class tamilToken( Token):
    """ add '@' token in extending the Token type """
    FORBIDDEN_FOR_IDENTIFIERS = [ "]","["," ",",", "\t","\r","\n","/", "-","+","^","=","*",")","(",">","<","&","&&","|","||","!","%","{","}",";","'","\"","$","@","#","."]
    Token.token_types.append("@")
    Token.ATRATEOF = len(Token.token_types)

    Token.token_types.append(u"RETURN|பின்கொடு")
    Token.token_types.append(u"FOREACH|ஒவ்வொன்றாக")
    Token.FOREACH = len(Token.token_types)

    Token.token_types.append(u"IN|இல்")
    Token.IN = Token.COMMA #short-circuit!
    
    Token.token_types.append(u"DOWHILE|முடியேனில்")
    Token.DOWHILE = len(Token.token_types)

    Token.token_types.append(u"IMPORT|உள்ளடக்கு")
    Token.IMPORT = len(Token.token_types)

    TALETTERS = u'|அ|ஆ|இ|ஈ|உ|ஊ|எ|ஏ|ஐ|ஒ|ஓ|ஔ|ஃ|க்|ச்|ட்|த்|ப்|ற்|ங்|ஞ்|ண்|ந்|ம்|ன்|ய்|ர்|ல்|வ்|ழ்|ள்|க|ச|ட|த|ப|ற|ஞ|ங|ண|ந|ம|ன|ய|ர|ல|வ|ழ|ள|ஜ|ஷ|ஸ|ஹ|க|கா|கி|கீ|கு|கூ|கெ|கே|கை|கொ|கோ|கௌ|ச|சா|சி|சீ|சு|சூ|செ|சே|சை|சொ|சோ|சௌ|ட|டா|டி|டீ|டு|டூ|டெ|டே|டை|டொ|டோ|டௌ|த|தா|தி|தீ|து|தூ|தெ|தே|தை|தொ|தோ|தௌ|ப|பா|பி|பீ|பு|பூ|பெ|பே|பை|பொ|போ|பௌ|ற|றா|றி|றீ|று|றூ|றெ|றே|றை|றொ|றோ|றௌ|ஞ|ஞா|ஞி|ஞீ|ஞு|ஞூ|ஞெ|ஞே|ஞை|ஞொ|ஞோ|ஞௌ|ங|ஙா|ஙி|ஙீ|ஙு|ஙூ|ஙெ|ஙே|ஙை|ஙொ|ஙோ|ஙௌ|ண|ணா|ணி|ணீ|ணு|ணூ|ணெ|ணே|ணை|ணொ|ணோ|ணௌ|ந|நா|நி|நீ|நு|நூ|நெ|நே|நை|நொ|நோ|நௌ|ம|மா|மி|மீ|மு|மூ|மெ|மே|மை|மொ|மோ|மௌ|ன|னா|னி|னீ|னு|னூ|னெ|னே|னை|னொ|னோ|னௌ|ய|யா|யி|யீ|யு|யூ|யெ|யே|யை|யொ|யோ|யௌ|ர|ரா|ரி|ரீ|ரு|ரூ|ரெ|ரே|ரை|ரொ|ரோ|ரௌ|ல|லா|லி|லீ|லு|லூ|லெ|லே|லை|லொ|லோ|லௌ|வ|வா|வி|வீ|வு|வூ|வெ|வே|வை|வொ|வோ|வௌ|ழ|ழா|ழி|ழீ|ழு|ழூ|ழெ|ழே|ழை|ழொ|ழோ|ழௌ|ள|ளா|ளி|ளீ|ளு|ளூ|ளெ|ளே|ளை|ளொ|ளோ|ளௌ|ௐ|ஜ|ஜா|ஜி|ஜீ|ஜு|ஜூ|ஜெ|ஜே|ஜை|ஜொ|ஜோ|ஜௌ|ஷ|ஷா|ஷி|ஷீ|ஷு|ஷூ|ஷெ|ஷே|ஷை|ஷொ|ஷோ|ஷௌ|ஸ|ஸா|ஸி|ஸீ|ஸு|ஸூ|ஸெ|ஸே|ஸை|ஸொ|ஸோ|ஸௌ|ஹ|ஹா|ஹி|ஹீ|ஹு|ஹூ|ஹெ|ஹே|ஹை|ஹொ|ஹோ|ஹௌ|'
    RE_ALPHA_NUMERIC_ = re.compile(r'[a-z|A-Z|_'+TALETTERS+'][a-z|A-Z|0-9|_'+TALETTERS+']*')
    RE_ALPHA_NUMERIC_ = re.compile(r'your_pattern', re.IGNORECASE)

    
    @staticmethod
    def is_keyword(kind):
        if Token.is_keyword(kind):
            return True
        if Token.get_name(kind) in [u"FOREACH",u"DOWHILE",u"IN",u"IMPORT"]:
            return True
        if Token.get_name(kind) in [u"பின்கொடு",u"பதிப்பி",u"ஒவ்வொன்றாக",u"@",u"இல்"]:
            return True
        return False

## SCANNER

class tamilLex ( Lex ) :
    """ Lex Tamil characters : RAII principle - lex on object construction"""
    
    def __init__(self,fname=None,dbg=False,encoding="utf-8"):
        if ( dbg ): print(u"init/tamilLex")
        Lex.__init__(self,fname,dbg,encoding)
        
    def get_lexeme(self,chunks , pos):
        if ( self.debug ):
            print(u"get_lexeme",chunks,pos)
        
        if chunks == None:
            return None
        
        if chunks == u"பதிப்பி":
            tval = tamilLexeme(chunks,tamilToken.PRINT )
        elif chunks == u"தேர்ந்தெடு":
            tval = tamilLexeme(chunks,tamilToken.SWITCH )
        elif chunks == u"தேர்வு":
            tval = tamilLexeme(chunks,tamilToken.CASE )
        elif chunks == u"ஏதேனில்":
            tval = tamilLexeme(chunks,tamilToken.OTHERWISE )
        elif chunks == u"ஆனால்":
            tval = tamilLexeme( chunks, tamilToken.IF )
        elif chunks == u"இல்லைஆனால்":
            tval = tamilLexeme( chunks, tamilToken.ELSEIF )
        elif chunks == u"இல்லை":
            tval = tamilLexeme( chunks, tamilToken.ELSE )
        elif chunks == u"ஆக":
            tval = tamilLexeme( chunks, tamilToken.FOR )
        elif chunks == u"ஒவ்வொன்றாக":
            tval = tamilLexeme( chunks, tamilToken.FOREACH )
        elif chunks == u"இல்":
            tval = tamilLexeme( chunks, tamilToken.COMMA )
        elif chunks == u"வரை":
            tval = tamilLexeme( chunks, tamilToken.WHILE )
        elif chunks == u"செய்":
            tval = tamilLexeme( chunks, tamilToken.DO )
        elif chunks == u"முடியேனில்":
            tval = tamilLexeme( chunks, tamilToken.DOWHILE )
        elif chunks == u"பின்கொடு":
            tval=tamilLexeme(chunks,tamilToken.RETURN)
        elif chunks == u"முடி":
            tval=tamilLexeme(chunks,tamilToken.END)
        elif chunks == u"நிரல்பாகம்":
            tval=tamilLexeme(chunks,tamilToken.DEF)
        elif chunks == u"தொடர்":
            tval=tamilLexeme(chunks,tamilToken.CONTINUE)
        elif chunks == u"நிறுத்து":
            tval=tamilLexeme(chunks,tamilToken.BREAK)
        elif chunks == u"உள்ளடக்கு":
            tval=tamilLexeme(chunks,tamilToken.IMPORT)
        elif chunks == u"@":
            tval=tamilLexeme(chunks,tamilToken.ATRATEOF)
        elif chunks == u"=":
            tval=tamilLexeme(chunks,tamilToken.EQUALS)
        elif chunks == u"-":
            tval=tamilLexeme(chunks,tamilToken.MINUS)
        elif chunks == u"+":
            tval=tamilLexeme(chunks,tamilToken.PLUS)
        elif chunks == u">":
            tval=tamilLexeme(chunks,tamilToken.GT)
        elif chunks == u"<":
            tval=tamilLexeme(chunks,tamilToken.LT)
        elif chunks == u">=":
            tval=tamilLexeme(chunks,tamilToken.GTEQ)
        elif chunks == u"<=":
            tval=tamilLexeme(chunks,tamilToken.LTEQ)
        elif chunks == u"==":
            tval=tamilLexeme(chunks,tamilToken.EQUALITY)
        elif chunks == u"!=":
            tval=tamilLexeme(chunks,tamilToken.NEQ)
        elif chunks == u"*":
            tval=tamilLexeme(chunks,tamilToken.PROD)
        elif chunks == u"/":
            tval=tamilLexeme(chunks,tamilToken.DIV)
        elif chunks == u",":
            tval=tamilLexeme(chunks,tamilToken.COMMA)
        elif chunks == u"(":
            tval=tamilLexeme(chunks,tamilToken.LPAREN)
        elif chunks == u")":
            tval=tamilLexeme(chunks,tamilToken.RPAREN)
        elif chunks == u"[":
            tval=tamilLexeme(chunks,tamilToken.LSQRBRACE)
        elif chunks == u"]":
            tval=tamilLexeme(chunks,tamilToken.RSQRBRACE)
        elif chunks == u"{":
            tval=Lexeme(chunks,Token.LCURLBRACE)
        elif chunks == u"}":
            tval=Lexeme(chunks,Token.RCURLBRACE)
        elif chunks == u":":
            tval=Lexeme(chunks,Token.COLON)
        elif chunks == u"%":
            tval=tamilLexeme(chunks,tamilToken.MOD)
        elif chunks == u"^":
            tval=tamilLexeme(chunks,tamilToken.EXP)
        elif chunks == u"&&":            
            tval=Lexeme(chunks,tamilToken.LOGICAL_AND)
        elif chunks == u"&":
            tval=Lexeme(chunks,tamilToken.BITWISE_AND)
        elif chunks == u"||":
            tval=Lexeme(chunks,tamilToken.LOGICAL_OR)
        elif chunks == u"|":
            tval=Lexeme(chunks,tamilToken.BITWISE_OR)
        elif chunks == u"<<":
            tval=Lexeme(chunks,tamilToken.BITWISE_LSHIFT)
        elif chunks == u">>":
            tval=Lexeme(chunks,tamilToken.BITWISE_RSHIFT)
        elif chunks == u"~":
            tval=Lexeme(chunks,tamilToken.BITWISE_COMPLEMENT)
        elif chunks == u"!":
            tval=Lexeme(chunks,tamilToken.LOGICAL_NOT)
        elif ( chunks[0] == u"\"" and chunks[-1] == u"\"" ):
            tval = tamilLexeme( chunks[1:-1], tamilToken.STRING )
        elif chunks[0].isdigit() or chunks[0]=='+' or chunks[0]=='-':
            #tval=tamilLexeme(float(chunks),tamilToken.NUMBER)
            # deduce a float or integer
            if ( chunks.find(u'.') >= 0 or chunks.find(u'e') >= 0 or chunks.find(u'E') >= 0 ):
                tval=tamilLexeme(float(chunks),tamilToken.NUMBER)
            else:
                tval=tamilLexeme(int(chunks),tamilToken.NUMBER)
        else:
            ## check for tamil/english/mixed indentifiers even starting with a lead '_'
            match_obj = re.match(tamilToken.RE_ALPHA_NUMERIC_,chunks)        
            if match_obj:
                if len(match_obj.group(0)) != len(chunks):
                    raise ScannerException(u"Lexical error: Invalid identifier name '"+str(chunks) + u"' at Line , Col "+str(self.get_line_col( pos ))+u" in file "+self.fname)            
                tval=tamilLexeme(chunks,tamilToken.ID)
            else:
                raise ScannerException(u"Lexical error: " + str(chunks) + u" at Line , Col "+str(self.get_line_col( pos )) +u" in file "+self.fname )
        
        [l,c]=self.get_line_col( pos )
        tval.set_line_col( [l,c] )
        tval.set_file_name( self.fname )
        self.tokens.append( tval )        
        
        if ( self.debug ): print(u"Lexer token = ",tval)
        return l
    
    @staticmethod
    def is_allowed_for_identifier(letter):
        return ( not letter in tamilToken.FORBIDDEN_FOR_IDENTIFIERS )
    
    def tokenize(self,data=None):
        """ do hard-work of tokenizing and
        put tamilLexemes into the tokens[] Q """
        if ( self.debug ): print(u"Start of tamil lexer - begin tokenize")
        if ( self.stdin_mode ):
            if ( self.debug ): print(self.tokens)
            ## cleanup the Q for stdin_mode of any EOF that can remain.
            if ( len(self.tokens) != 0 ):
                self.match( tamilToken.EOF )
            if( len(self.tokens) != 0 ):
                raise ScannerException("Lexer: token Q has previous session tokens ")
            self.tokens = list()
        else:
            if hasattr(self.File,'data'):
                if ( self.debug ): print("data attribute")
                data = self.File.data
            elif self.encoding == "utf-8":
                data = self.File.read()
            elif self.encoding == "tscii":
                if self.debug: print("Loading TSCII converted data -> ")
                data = self.converted_data
            else:
                assert False
        if ( self.debug ): print(data)
        idx = 0
        tok_start_idx = 0
        
        while ( idx < len( data ) ):
            c = data[idx]
            if ( self.debug ): print(idx,c)
            if ( istamil( c ) or c.isalpha( ) or c == u'_' ):
                tok_start_idx = idx
                s = c; idx = idx + 1
                while ( ( idx < len( data ) )
                        and self.is_allowed_for_identifier( data[idx] ) ):
                    s = s + data[idx]
                    idx = idx + 1
                if idx < len(data) and not data[idx].isspace():
                    if  data[idx] in ['#','$','@','\'','"']:
                        raise ScannerException("Lexer: token %s is not valid for identifier, with prefix %s"%(data[idx],s))
                self.get_lexeme( s , tok_start_idx )
            elif  ( c.isspace() ): # or c in u' 'or c == u'\t' or c == u'\n'
                if ( c == u'\n' ):
                    ##actual col = idx - col_idx
                    self.update_line_col(idx)
                idx = idx + 1
            elif ( c == u'\r' ):
                idx = idx + 1
                continue
            elif ( c == u'#' ):
                ## single line skip comments like Python/Octave
                start = idx;
                while ( idx < len( data ) and not (data[idx] in [u'\r',u'\n']) ):
                    idx = idx + 1
                if ( idx < len(data) and data[idx] == u'\r' ):
                    idx = idx + 1
                end = idx
                self.comments[self.line]= data[start:end]
            elif ( c.isdigit() ): #or c == '+' or c == '-'  ):
                num = c
                tok_start_idx = idx
                idx = idx + 1
                ## FIXME: this prevents you from +.xyz, or -.xyz use 0.xyz 
                ## instead. also may throw an error if we exceed 
                ## buffer-length.                
                if ( c in [u'+',u'-']  and ( idx < len( data ) ) 
                     and not data[idx].isdigit() ):
                    self.get_lexeme( c , idx )
                    continue
                in_sci_notation = False
                while ( ( idx < len( data) )
                            and ( data[idx].isdigit() or data[idx] in [u'+',u'-',u'e',u'E',u'.']) ):
                    if ( data[idx] in [u'+',u'-'] and not in_sci_notation ):
                        break;
                    elif( data[idx] in [u'e',u'E'] ):
                        in_sci_notation = True
                    num = num + data[idx]
                    idx = idx + 1
                self.get_lexeme( num , tok_start_idx  )
            elif ( c == u"\"" ):
                tok_start_idx = idx 
                s = c; idx = idx + 1
                while ( idx < len( data ) and
                         ( data[idx] != u'\"' ) ):
                    if ( data[idx] == u'\\' ):
                        idx = idx + 1
                        if ( data[idx] == u'n' ):
                            s = s + u'\n'
                        elif ( data[idx] == u't' ):
                            s = s +u'\t'
                        else:
                            s = s + data[idx]
                    else:
                        s = s + data[idx]
                    idx  = idx + 1
                s = s+data[idx]
                idx  = idx + 1
                self.get_lexeme( s , tok_start_idx )
            elif ( c in self.unary_binary_ops ):
                tok_start_idx = idx                 
                if ( len(data) > ( 1 + idx  ) 
                     and data[idx+1] in [u'=',u'|',u'&',u'>',u'<'] ):
                    c = c +data[idx+1]
                    idx = idx + 1
                self.get_lexeme(  c , tok_start_idx )
                idx = idx + 1
            elif c == u";":
                # treat as newline
                idx = idx + 1
                continue
            else:
                tok_start_idx = idx 
                idx = idx + 1
                self.get_lexeme( c , tok_start_idx )
        
        tok_start_idx = idx
        ## close the file if not stdin_mode
        if ( not self.stdin_mode ): self.File.close()
        
        ## and manually add an EOF statement.
        eof_tok = tamilLexeme("",tamilToken.EOF )
        eof_tok.set_line_col( self.get_line_col( tok_start_idx ) )
        self.tokens.append( eof_tok )
        if ( self.debug ):  print(u"before reverse"); self.dump_tokens()
        self.tokens.reverse()
        if ( self.debug ):  print(u"after reverse"); self.dump_tokens()
        return
