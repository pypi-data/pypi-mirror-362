#!/usr/bin/python
##
## (C) 2007, 2008-2013, 2015 Muthiah Annamalai,
## Licensed under GPL Version 3
## 
## tamil parser & AST builder - tamil frontend and  AST elements to build the parse tree.
## refactored left-recursion in the examples

import sys

PYTHON3 = (sys.version[0] == '3')
if PYTHON3:
    str = str

## scanner for tamil language
from .tamil_scanner import tamilToken, tamilLex, tamilLexeme

## exceptions
from .errors import RuntimeException, ParseException

## runtime elements
from .runtime import  Environment, BuiltinFunction, \
 BlindBuiltins, DebugUtils

## AST elements
from .ast import Expr, UnaryExpr, ExprCall, ExprList, Stmt, ReturnStmt, \
 BreakStmt, ContinueStmt, ElseStmt, IfStmt, WhileStmt, DoWhileStmt, \
 ForStmt, AssignStmt, PrintStmt, DeclarationStmt, EvalStmt, ArgList, \
 ImportStmt, ValueList, Function, StmtList, Identifier, Number, \
 String, Array, Dict

## use exprs language parser
from .ExprsParser import Parser

## Tamil messages
from .tamil_messages import get_message, Messages

## Parser implementes the grammar for 'exprs' language.
## Entry point is parse(), after appropriate ctor-setup.
class tamilParser(Parser):
    """ when you add new language feature, add a AST class 
    and its evaluate methods. Also add a parser method """
    def __init__(self,lexer,fcn_map, builtin_map, dbg = False):
        if ( not isinstance(lexer, tamilLex) ):
                exception_msg = get_message(Messages.ClassNotFound)
                raise RuntimeException(Messages.ClassNotFound,u"tamil lexer")
        Parser.__init__(self,lexer,fcn_map,builtin_map,dbg)
        self.open_if_stmts = 0
        self.backtrack_atexpr = None

    @staticmethod
    def factory(lexer,fcn_map,builtin_map, dbg = False):
        """ Factory method """
        return tamilParser(lexer,fcn_map,builtin_map, dbg)

    def match(self,kind):
        ## if match return token, else ParseException
        tok = self.dequeue()
        if ( tok.kind != kind ):
            raise ParseException(u"cannot find token "+ \
                                 tamilToken.get_name(kind) + u" got " \
                                + str(tok)  \
                                + u" instead!")
        return tok

    def parse(self):
        """ parser routine """
        self.ast = StmtList(istoplevel=True)
        self.dbg_msg(u" entering parser " )
        while ( not self.lex.end_of_tokens() ):
            self.dbg_msg( u"AST length = %d"%len(self.ast) )
            if ( self.lex.peek().kind ==  tamilToken.DEF ):
                self.dbg_msg ( u"parsing for function" )
                ## save function in a global table.
                func = self.function()
                self.warn_function_overrides(func.name)
                self.function_map[func.name]=func
                self.ast.append(DeclarationStmt(func)) #add to AST
            else:
                self.dbg_msg( u"parsing for stmt" )
                st = self.stmtlist()
                if ( not self.parsing_function ):
                    self.ast.append(st)
        return self.ast

    def stmtlist(self,pass_in_ATexpr=None):
        """ parse a bunch of statements """
        self.dbg_msg(u" STMTLIST ")
        stlist = StmtList()
        while( not self.lex.end_of_tokens() ):
            self.dbg_msg(u"STMTLIST => STMT")
            ptok = self.peek()
            self.dbg_msg(u"STMTLIST "+str(ptok))
            if ( self.debug ): print(u"peek @ ",str(ptok))
            if ( ptok.kind == tamilToken.END ):
                self.dbg_msg(u"End token found");
                break
            elif ( ptok.kind == tamilToken.DOWHILE ):
                if ( self.debug ): print("DOWHILE token found")
                break            
            elif( self.inside_if and 
                 ( ptok.kind ==  tamilToken.ELSE
                   or ptok.kind == tamilToken.ATRATEOF 
                   or ptok.kind == tamilToken.CASE 
                   or ptok.kind == tamilToken.OTHERWISE ) ):
                break
            elif( ptok.kind ==  tamilToken.DEF ):
                break
            st = self.stmt(pass_in_ATexpr)
            pass_in_ATexpr = None
            stlist.append( st )
        return stlist
    
    def parseSwitchStmt(self,exp):
        ## @ <ID/EXPR> SWITCH @( expr ) CASE {stmtlist} @( expr ) CASE {stmtlist} OTHERWISE {stmtlist} END
        ## implement as an if-elseif-else statement
        self.dbg_msg("parsing SWITCH statement")
        sw_tok = self.dequeue()
        [l,c]=sw_tok.get_line_col()
        self.inside_if = True
        lhs=exp[0]
        # enter this if-statement always
        ifstmt = IfStmt( Number(1), None, None, l, c, self.debug)
        self.if_stack.append(ifstmt)
        self.dbg_msg("parsing SWITCH-body") #self.dbg_msg        
        ptok = self.peek()
        equality_token = tamilLexeme("=",tamilToken.EQUALITY)
        while ( ptok.kind == tamilToken.ATRATEOF or ptok.kind == tamilToken.OTHERWISE ):
            self.inside_if = True
            [l,c]=ptok.get_line_col()
            if ( ptok.kind == tamilToken.ATRATEOF ):
                # parse elseif branch
                self.dbg_msg("parsing CASE")
                self.match( tamilToken.ATRATEOF )
                exp = self.valuelist();
                self.dbg_msg("parsing CASE EXPR")
                self.match( tamilToken.CASE )
                next_stmt = self.stmtlist()                
                expr = Expr( lhs, equality_token, exp[0], l, c, self.debug )
                self.dbg_msg("building an Expr "+str(expr))                
                if not ifstmt.body :
                    ifstmt.expr = expr
                    ifstmt.body = next_stmt
                else:
                    case_stmt = IfStmt(expr,next_stmt,None,l,c,self.debug);
                    ifstmt.append_stmt( case_stmt )
            elif ( ptok.kind == tamilToken.OTHERWISE ):
                #parse else branch
                self.dbg_msg("parsing OTHERWISE: ")
                self.match( tamilToken.OTHERWISE )
                self.dbg_msg("parsing OTHERWISE-Body")
                self.inside_if = False
                body = self.stmtlist()
                else_stmt = ElseStmt( body , l, c, self.debug)
                if not ifstmt.body :
                    ifstmt.body = else_stmt
                else:
                    ifstmt.append_stmt( else_stmt )
                break
            else:
                self.inside_if = False
                exception_msg = get_message(Messages.CaseSyntaxError)
                raise ParseException(exception_msg)
            ptok = self.peek()
            self.dbg_msg("parsing SWITCH-CASE next bits "+str(ptok))
        self.match( tamilToken.END )
        self.inside_if = False
        self.dbg_msg("parsing -SWITCH-CASE- complete")
        return ifstmt
    
    def parseIfStmt(self,exp):
        ## @ <expression> if { stmtlist } @<expr> ELSEIF {stmtlist} ELSE <stmtlist> END
        self.dbg_msg(u"parsing IF statement")
        if_tok = self.dequeue()
        [l,c]=if_tok.get_line_col()
        self.inside_if = True
        ifstmt = IfStmt( exp[0], None, None, l, c, self.debug)
        self.if_stack.append(ifstmt)
        self.dbg_msg(u"parsing IF-body")
        body = self.stmtlist()
        prev_body = body;
        ifstmt.set_body( body )
        ptok = self.peek()
        while ( ptok.kind == tamilToken.ATRATEOF or ptok.kind == tamilToken.ELSE ):
            self.inside_if = True        
            [l,c]=ptok.get_line_col()
            if ( ptok.kind == tamilToken.ATRATEOF ):
                # parse elseif branch
                self.dbg_msg(u"parsing ELSE-IF")                
                self.match( tamilToken.ATRATEOF )
                exp = self.valuelist();
                self.dbg_msg(u"parsing ELSE-IF EXPR")
                tok = self.peek()
                if ( tok.kind != tamilToken.ELSEIF ):
                    # maybe another IF statement, SWITCH-CASE or a WHILE loop, DO-WHILE loop etc.
                    next_stmt = self.stmtlist(exp) #pass in the expression                                        
                    prev_body.append( next_stmt )
                    # append to previously scanned body.
                else:
                    self.dbg_msg(u"parsing ELSE-IF-body")
                    self.match( tamilToken.ELSEIF )
                    body = self.stmtlist()
                    prev_body = body
                    next_stmt = IfStmt(exp[0],body,None,l,c,self.debug)
                    self.dbg_msg(u"ELSEIF parsed correctly => "+str(next_stmt))
                    ifstmt.append_stmt( next_stmt )
            elif ( ptok.kind == tamilToken.ELSE ):
                #parse else branch                
                self.dbg_msg(u"parsing stmt else: ")
                self.match( tamilToken.ELSE )
                self.dbg_msg(u"parsing ELSE-Body")
                self.inside_if = False
                body = self.stmtlist()
                prev_body = body;
                else_stmt = ElseStmt( body , l, c, self.debug)                
                ifstmt.append_stmt( else_stmt )
                break
            else:
                self.inside_if = False
                exception_msg = get_message(Messages.IfSyntaxError)
                raise ParseException(exception_msg)
            ptok = self.peek()
            self.dbg_msg(u"parsing -IF next bits "+str(ptok))
        self.match( tamilToken.END )
        self.inside_if = False
        self.dbg_msg(u"parsing -IF-complete")
        return ifstmt
    
    def stmt(self,pass_in_ATexpr=None):
        """ try an assign, print, return, if or eval statement """
        self.dbg_msg(u" STMT ")
        ptok = self.peek()
        self.dbg_msg(u"stmt: peeking at "+str(ptok))
        if ( ptok.kind ==  tamilToken.RETURN ):
            ## return <expression>
            self.dbg_msg('enter->return: <expression>')
            ret_tok = self.dequeue()
            [l,c]=ret_tok.get_line_col();
            if ( not self.parsing_function ):
                raise ParseException( u"return statement outside of function body "+str(ret_tok))
            rstmt = ReturnStmt(self.expr(),l,c,self.debug)
            self.dbg_msg(u"return statement parsed")
            return rstmt
        elif ( ptok.kind ==  tamilToken.PRINT ):
            self.dbg_msg(u"stmt : print ")
            self.currently_parsing.append( ptok )
            ## print <expression>
            print_tok = self.dequeue()
            [l,c]=print_tok.get_line_col();
            exprlist_val = self.exprlist();
            self.currently_parsing.pop()
            return PrintStmt(exprlist_val,l,c,self.debug)        
        elif ( ptok.kind ==  tamilToken.ATRATEOF or pass_in_ATexpr):
            ## @ <expression> {if | while | elseif}
            if not pass_in_ATexpr:
                at_tok = self.match(tamilToken.ATRATEOF)
                self.currently_parsing.append( at_tok )
                exp = self.valuelist();
                self.currently_parsing.pop()
            else:
                exp = pass_in_ATexpr
                pass_in_ATexpr = None #use it just once
            if( self.debug ): print ("return from valuelist ",str(exp))
            ptok = self.peek();
            if ( ptok.kind == tamilToken.IF ):                
                return self.parseIfStmt(exp)
            elif ( ptok.kind ==  tamilToken.WHILE ):
                ## @ ( expr ) while { body } end               
               self.loop_stack.append(True)
               self.dbg_msg(u"while-statement")
               while_tok = self.dequeue()
               self.currently_parsing.append( while_tok )
               [l,c]=while_tok.get_line_col()
               wexpr = exp[0];
               body = self.stmtlist( )
               self.match( tamilToken.END)
               whilestmt = WhileStmt(wexpr, body, l, c, self.debug)
               self.loop_stack.pop()
               self.currently_parsing.pop()
               return whilestmt
            elif ( ptok.kind ==  tamilToken.SWITCH ):
                return self.parseSwitchStmt(exp)
            elif ( ptok.kind ==  tamilToken.FOREACH ):
                foreach_tok = self.dequeue()
                self.currently_parsing.append(foreach_tok)
                [l,c]=foreach_tok.get_line_col()
                if ( self.debug ): print(u"parsing FOREACH stmt")
                self.loop_stack.append(True)
                self.dbg_msg(u"foreach-statement")
                # convert to a for statement - building tamil AST - transformations
                if not isinstance( exp[1], Identifier ):
                    raise ParseException(u" FOR-EACH statement "+str(foreach_tok) )
                foreach_iter = exp[1];
                iter = Identifier("__"+foreach_iter.id,l=0,c=-1);
                eq_token = tamilLexeme(u"=",tamilToken.EQUALS)
                plus_token = tamilLexeme(u"+",tamilToken.PLUS)
                lt_token = tamilLexeme(u"<",tamilToken.LT)
                if ( self.debug ): print(u"build init assign stmt")
                init = AssignStmt( iter, eq_token , Number(0),l,c,self.debug)
                if ( self.debug ): print(u"build cond expr")
                VL1 = ValueList([exp[0]],l,c,self.debug)
                cond = Expr( iter, lt_token, ExprCall( Identifier("len",l,c), VL1, l, c, self.debug ), l, c, self.debug )
                if ( self.debug ): print("build plus1 stmt")
                plus1_iter = Expr( iter, plus_token, Number(1), l, c, self.debug  )
                if ( self.debug ): print(u"build equals stmt")
                update = AssignStmt( iter, eq_token , plus1_iter ,l,c,self.debug)
                body = self.stmtlist() #parse body
                # and insert artifical update variable in body
                VL2 = ValueList([exp[0],iter],l,c,self.debug)
                extract_foreach_iter_from_list = ExprCall( Identifier("__getitem__",l,c), VL2,l,c,self.debug);
                foreach_iter_Assign = AssignStmt( foreach_iter, eq_token , extract_foreach_iter_from_list, l,c,self.debug )
                body.List.insert( 0,foreach_iter_Assign)
                # complete FOREACH stmt
                self.match( tamilToken.END)
                self.currently_parsing.pop()
                foreach_stmt = ForStmt(init, cond, update, body, l, c, self.debug);                
                self.loop_stack.pop();                
                if ( self.debug ): print(u"completed parsing FOR-EACH loop",str(foreach_stmt))
                return foreach_stmt
            elif ( ptok.kind ==  tamilToken.FOR ):
                ## Fixme : empty for loops not allowed.
                """ For ( exp1 , exp2 , exp3 ) stmtlist  end"""
                if ( self.debug ): print("parsing FOR stmt")
                self.loop_stack.append(True)
                self.dbg_msg("for-statement")                
                for_tok = self.peek()
                self.currently_parsing.append(for_tok)
                if ( self.debug ): print("matching for STMT",str(self.peek()))
                self.match( tamilToken.FOR )
                if ( self.debug ): print("matched for STMT",str(self.peek()))
                [l,c]= for_tok.get_line_col();
                init,cond,update = exp[0],exp[1],exp[2]            
                if ( self.debug ): print("extract 3 parts",str(init),str(cond),str(update))
                body = self.stmtlist()
                self.match( tamilToken.END)
                self.currently_parsing.pop()
                if ( self.debug ): print("body of loop",str(body))
                forstmt = ForStmt(init, cond, update, body, l, c, self.debug);
                self.loop_stack.pop();
                if ( self.debug ): print("completed parsing FOR loop",str(forstmt))
                return forstmt
        elif ( ptok.kind == tamilToken.DO ):
            if ( self.debug ): print("parsing DO-WHILE statement")
            self.loop_stack.append(True)
            do_tok = self.dequeue()
            self.currently_parsing.append(do_tok)
            [l,c]=do_tok.get_line_col()
            body = self.stmtlist()
            if ( self.debug ): print("parsed body")
            self.match(tamilToken.DOWHILE)            
            self.match(tamilToken.ATRATEOF)
            exp = self.valuelist();
            if ( self.debug ): print("parsed EXP",exp[0])
            doWhileStmt = DoWhileStmt(exp[0], body, l, c, self.debug)
            self.loop_stack.pop()
            self.currently_parsing.pop()
            return doWhileStmt
        elif ( ptok.kind ==  tamilToken.BREAK ):
            ## break, must be in loop-environment
            self.dbg_msg("break-statement");
            break_tok = self.dequeue();
            [l,c]=break_tok.get_line_col()
            self.check_loop_stack(); ##raises a parse error
            brkstmt = BreakStmt( l, c, self.debug);
            return brkstmt
        elif ( ptok.kind ==  tamilToken.CONTINUE ):
            ## continue, must be in loop-environment
            self.dbg_msg("continue-statement");
            cont_tok = self.dequeue();
            [l,c]=cont_tok.get_line_col()
            self.check_loop_stack(); ##raises a parse error
            cntstmt = ContinueStmt( l, c, self.debug);
            return cntstmt
        elif ( ptok.kind == tamilToken.IMPORT ):
            self.dbg_msg("import-statement")
            import_tok = self.dequeue()
            [l,c] = import_tok.get_line_col()
            self.currently_parsing.append(import_tok)
            fname = self.expr()
            self.currently_parsing.pop()
            importstmt = ImportStmt(l,c,self.debug,fname)
            return importstmt
        else:
            ## lval := rval
            ptok = self.peek()
            self.currently_parsing.append(ptok)
            [l,c] = ptok.get_line_col()
            lhs = self.expr()
            self.dbg_msg("parsing expr: "+str(lhs))
            ptok = self.peek()
            if ( ptok.kind in  tamilToken.ASSIGNOP ):
                assign_tok = self.dequeue()
                rhs = self.expr()
                [l,c]=assign_tok.get_line_col()
                self.currently_parsing.pop()
                if isinstance(lhs,ExprCall):
                    # however array assignment is carried out through setitem
                    # print 'expr-->',lhs,'rhs-->',rhs
                    newlhs = lhs
                    newlhs.fname = '__setitem__'
                    newlhs.arglist.append(rhs)
                    return EvalStmt(newlhs,l,c,self.debug)
                return AssignStmt( lhs, assign_tok, rhs, l, c, self.debug)
            self.currently_parsing.pop()
            return EvalStmt( lhs, l, c, self.debug )
        raise ParseException("parsing Statement, unknown operators" + str(ptok))
    
    def function(self):
        """ def[kw] fname[id] (arglist) {body} end[kw] """
        if ( self.parsing_function ):
            self.parsing_function = False
            raise ParseException(u" Nested functions not allowed! "+str(self.last_token()))

        self.parsing_function = True
        def_tok = self.dequeue()
        if ( def_tok.kind !=  tamilToken.DEF ):
            raise ParseException(u"unmatched 'def'  in function " +str(def_tok))
        
        id_tok = self.dequeue()
        if ( id_tok.kind !=  tamilToken.ID ):
            raise ParseException(u"expected identifier in function"+str(id_tok))
        
        arglist = self.arglist()
        self.dbg_msg( u"finished parsing arglist" )
        body = self.stmtlist()

        self.match(  tamilToken.END )
        [l,c] = def_tok.get_line_col()
        fval = Function( id_tok.val, arglist, body, l, c, self.debug )
        self.parsing_function = False
        self.dbg_msg( u"finished parsing function" ) 
        return fval

    def valuelist(self):
        """parse: ( expr_1 , expr_2, ... ) """
        valueList = list()
        self.dbg_msg(u"valuelist: ")
        lparen_tok = self.match(  tamilToken.LPAREN )
        while ( self.peek().kind !=  tamilToken.RPAREN ):            
            val = self.expr()
            if ( self.debug ): print(u"val = ",str(val))
            ptok = self.peek()
            if ( self.debug ) : print(u"ptok = ",str(ptok),str(ptok.kind),str(tamilToken.ASSIGNOP))
            if ( ptok.kind in  tamilToken.ASSIGNOP ):
                assign_tok = self.dequeue()
                rhs = self.expr()
                [l,c]=assign_tok.get_line_col()
                lhs = val
                val =  AssignStmt( lhs, assign_tok, rhs, l, c, self.debug)
                if ( self.debug ): print(u"AssignStmt = ",str(val))
                ptok = self.peek()
            else:
                if ( self.debug ): print(u"No-Assign // Expr =",str(val))
            self.dbg_msg(u"valuelist-expr: "+str(val))
            valueList.append( val )
            if  ( ptok.kind ==  tamilToken.RPAREN ):
                break
            elif ( ptok.kind ==  tamilToken.COMMA ):
                self.match(  tamilToken.COMMA )
            else:
                raise ParseException(u" function call argument list "+str(ptok))
        self.match(  tamilToken.RPAREN )
        [l,c] = lparen_tok.get_line_col()
        return ValueList(valueList, l, c, self.debug )

    def arglist(self):
        """parse: ( arg_1, arg_2, ... ) """
        self.dbg_msg( u" ARGLIST " )
        args = list()
        lparen_tok = self.match(  tamilToken.LPAREN )
        while ( self.peek().kind !=  tamilToken.RPAREN ):
            arg_name = self.dequeue()
            args.append( arg_name.val )
            ptok = self.peek()
            if  ( ptok.kind ==  tamilToken.RPAREN ):
                break
            elif ( ptok.kind ==  tamilToken.COMMA ):
                self.match(  tamilToken.COMMA )
            else:
                raise ParseException(u" function definition argument list "
                                     +str(ptok))
        self.match(  tamilToken.RPAREN )
        [l,c] = lparen_tok.get_line_col()
        return ArgList(args , l, c, self.debug )
        
    def exprlist(self):
        """   EXPRLIST : EXPR, EXPRLIST        
        ##  EXPRLIST : EXPR """
        self.dbg_msg( u" EXPRLIST " )
        exprs=[]
        comma_tok = None
        l = 0; c = 0
        while ( not self.lex.end_of_tokens() ):
            exprs.append(self.expr())
            if self.lex.peek().kind !=  tamilToken.COMMA:
                break            
            tok = self.match( tamilToken.COMMA)
            if ( not comma_tok ):
                comma_tok = tok 

        if ( comma_tok ):
            [l,c] = comma_tok.get_line_col()
        self.dbg_msg(u"finished expression list")
        return ExprList(exprs, l, c, self.debug)

    def expr(self):
        self.dbg_msg( u" EXPR " )
        val1=self.term()
        res=val1
        ptok = self.peek()
        if ptok.kind in  tamilToken.ADDSUB:
            binop=self.dequeue()
            if ( ptok.kind == tamilToken.MINUS ):
                val2 = self.term()
            else:
                val2=self.expr()
            [l,c] = binop.get_line_col()
            res=Expr(val1,binop,val2, l, c, self.debug )
        elif ptok.kind ==  tamilToken.LPAREN:
            ## function call
            if ( not isinstance(res, Identifier) ):
                raise ParseException(u"invalid function call"+str(ptok))
            [l,c] = ptok.get_line_col()
            vallist = self.valuelist()
            res=ExprCall( res, vallist, l, c, self.debug )
        
        ptok = self.peek()
        while  ptok.kind in tamilToken.BINOP:
            binop = self.dequeue()
            [l,c] = binop.get_line_col()
            res = Expr( res, binop,self.expr(), l,c,self.debug)
            ptok = self.peek()
        return res
    
    def term(self):
        """ this is a grammar abstraction; 
        but AST only has Expr elements"""
        self.dbg_msg( "term" )
        val1=self.factor()
        res=val1

        tok = self.peek()
        if ( tok.kind in  tamilToken.MULDIV 
             or  tok.kind in  tamilToken.COMPARE 
             or tok.kind in  tamilToken.EXPMOD 
             or tok.kind in tamilToken.BITWISE_AND_LOGICAL ):
            binop=self.dequeue()
            val2=self.term()
            [l,c] = binop.get_line_col()
            res=Expr(val1,binop,val2, l, c, self.debug)
            
        return res
    
    def factor(self):
        self.dbg_msg( "factor" )
        tok=self.peek()
        if tok.kind ==  tamilToken.LPAREN:
            lparen_tok = self.dequeue()
            val=self.expr()
            if self.dequeue().kind!= tamilToken.RPAREN:
                raise SyntaxError("Missing Parens "+str(self.last_token()))
        elif tok.kind ==  tamilToken.NUMBER:
            tok_num = self.dequeue()
            [l, c] = tok_num.get_line_col()
            val = Number( tok.val , l, c, self.debug )
        elif tok.kind == tamilToken.LOGICAL_NOT:
            tok_not = self.dequeue()
            [l, c] = tok_not.get_line_col()
            val = UnaryExpr( self.expr(), tok_not , l, c, self.debug )
            self.dbg_msg("completed parsing unary logical-not expression"+str(val))
        elif tok.kind == tamilToken.BITWISE_COMPLEMENT:
            tok_compl = self.dequeue()
            [l, c] = tok_compl.get_line_col()
            val = UnaryExpr( self.expr(), tok_compl , l, c, self.debug )
            self.dbg_msg("completed parsing unary bitwise-complement expression"+str(val))
        elif tok.kind ==  tamilToken.ID:
            tok_id = self.dequeue()
            [l, c] = tok_id.get_line_col()
            val = Identifier( tok.val , l, c, self.debug )
            ptok = self.peek()
            self.dbg_msg(u"factor: "+str(ptok) + u" / "+ str(tok) )
            if ( ptok.kind ==  tamilToken.LPAREN ):
                ## function call
                [l, c] = ptok.get_line_col()
                vallist = self.valuelist()
                val=ExprCall( val, vallist, l, c, self.debug )
            elif ( ptok.kind ==  tamilToken.LSQRBRACE ):
                ## indexing a array type variable or ID                
                [l,c] = ptok.get_line_col()
                ## replace with a call to __getitem__
                exp = self.factor();
                if ( hasattr(exp,'__getitem__') ):
                    VL2 = ValueList([val,exp[0]],l,c,self.debug)
                else:
                    # when exp is a expression
                    VL2 = ValueList([val,exp],l,c,self.debug)
                val = ExprCall( Identifier("__getitem__",l,c), VL2,l,c,self.debug)
                for itr in range(1,len(exp)):
                    VL2 = ValueList([val,exp[itr]],l,c,self.debug)
                    val = ExprCall( Identifier("__getitem__",l,c), VL2,l,c,self.debug)
            elif ( ptok.kind ==  tamilToken.LCURLBRACE ):
                val=None
                raise ParseException("dictionary indexing uses square brackets '[' only ']'"+str(ptok));
        elif tok.kind ==  tamilToken.STRING :
            str_tok = self.dequeue()
            [l,c] = str_tok.get_line_col()
            val = String( tok.val , l, c, self.debug )
        elif tok.kind in tamilToken.ADDSUB:
            unop = self.dequeue();
            [l, c] = unop.get_line_col()
            val=Expr(Number(0),unop,self.term(),l,c,self.debug);
        elif tok.kind == tamilToken.LCURLBRACE:
            # creating a list/dictionary expression
            dict_start = self.dequeue();
            val = Dict()
            while( True ):
                if ( self.peek().kind == tamilToken.RCURLBRACE ):
                    break;
                exprkey = self.expr()
                tok_colon = self.match(tamilToken.COLON)
                exprval = self.expr()
                val.update( {exprkey : exprval}  )
                if self.debug : print(self.peek().__class__,self.peek())
                if ( self.peek().kind == tamilToken.RCURLBRACE ):
                    break
                else:
                    assert( self.peek().kind == tamilToken.COMMA)
                    self.dequeue()
            assert( self.peek().kind == tamilToken.RCURLBRACE )
            list_end = self.dequeue()
        elif tok.kind == tamilToken.LSQRBRACE:
            # creating a list/array expression
            list_start = self.dequeue();
            val = Array()
            while( True ):
                if ( self.peek().kind == tamilToken.RSQRBRACE ):
                    break;
                exprval = self.expr()
                val.append( exprval  )
                if self.debug : print(self.peek().__class__,self.peek())
                if ( self.peek().kind == tamilToken.RSQRBRACE ):
                    break
                else:
                    assert( self.peek().kind == tamilToken.COMMA)
                    self.dequeue()
            assert( self.peek().kind == tamilToken.RSQRBRACE )
            list_end = self.dequeue()
        else:
            exception_msg = get_message(Messages.UnexpectedNumber,str(tok))
            raise ParseException(exception_msg)
        self.dbg_msg( u"factor-returning: "+str(val) )
        return val
