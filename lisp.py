#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from lisp_errors import LispError


class Namespace:
    def __init__(self, previous = None):
        self.prev = previous if previous else {}
        self.nmspace = {}
    def __getitem__(self, key):
        return self.nmspace[key] if key in self.nmspace else self.prev[key]
    def __setitem__(self, key, value):
        self.nmspace[key] = value
    def __delitem__(self, key):
        del self.nmspace[key]
    def __contains__(self, item):
        return item in self.nmspace or item in self.prev
    def __repr__(self):
        return repr(self.nmspace)


# global namespace (toplevel)
_Namespace = {}
# namespace for functions
_Fvals = {}


##################################################


# useful predicates
def nilp(obj):
    return obj is nil

def consp(obj):
    return isinstance(obj, Cons)

def atom(obj):
    return isinstance(obj, Atom)

def listp(obj):
    return nilp(obj) or consp(obj)


####################################################

def list_iterator(cons):
    while cons is not nil:
        yield cons.car
        cons = cons.cdr


# helper function
def _to_list(*args):
    return reduce(lambda x, y: Cons(y, x), reversed(args), nil)


# use closures for cleaner implementation of eval
def func_eval(func):
    def _eval(obj, ns):
        try:
            return func(*[arg.eval(ns) for arg in list_iterator(obj)])
        except TypeError as err:
            raise LispError(repr(err))
    return _eval

# hmmm...
def func_eval_in_namespace(func):
    def _eval(obj, ns):
        try:
            return func(*[arg.eval(ns) for arg in list_iterator(obj)], namespace=ns)
        except TypeError as err:
            raise LispError(repr(err))
    return _eval

def macro_eval(func):
    def _eval(obj, ns):
        try:
            return func(obj).eval(ns)
        except TypeError as err:
            raise LispError(repr(err))
    return _eval



###################################################

# lisp builtins functions
def lsp_set(sym, val, namespace):
    return sym.bind(val, namespace)

def rplaca(cons, o):
    if not consp(cons):
        raise LispError(repr(cons) + ' is not a cons')
    cons.car = o
    return cons

def rplacd(cons, o):
    if not consp(cons):
        raise LispError(repr(cons) + ' is not a cons')
    cons.cdr = o
    return cons

# builtins macros

## impl : (set (quote a) v)
def setq(o):
    return _to_list(*[Symbol('set'), _to_list(*[Symbol('quote'), o.car]), o.cdr.car])

## impl : (setq a (cons e a))
def push(o):
    return _to_list(*[Symbol('setq'), o.cdr.car, _to_list(*[Symbol('cons'), o.car, o.cdr.car])])

## impl : (prog1 (car a) (setq a (cdr a)))
def pop(o):
    return _to_list(*[Symbol('prog1'),
                    _to_list(*[Symbol('car'), o.car]),
                    _to_list(*[Symbol('setq'), o.car, _to_list(*[Symbol('cdr'), o.car])])])



def defun(cons, _):
    symbol, params, corps = cons.car.symbol, cons.cdr.car, cons.cdr.cdr.car
    def eval_user_func(obj, ns):
        new_namespace = Namespace(ns)
        for (k, v) in zip(list_iterator(params), list_iterator(obj)):
            new_namespace[k.symbol] = v.eval(ns)
        return corps.eval(new_namespace)
    _Fvals[symbol] = eval_user_func
    return cons.car

def defmacro(cons, _):
    symbol, params, corps = cons.car.symbol, cons.cdr.car, cons.cdr.cdr.car
    def eval_user_macro(obj, ns):
        new_namespace = Namespace(ns)
        for (k, v) in zip(list_iterator(params), list_iterator(obj)):
            new_namespace[k.symbol] = v.eval(ns)
        return corps.eval(new_namespace).eval(ns)
    _Fvals[symbol] = eval_user_macro
    return cons.car


#   /!\    WARNING   /!\
# l'evaluation doit parfois se faire à l'interieur des fonction, et pas avant...
# c'est absolument crucial, par ex. pour les conditions d'arrets lors d'une récursion
# exemple : if, or...

def _or(o, ns):
    a, b = list_iterator(o)
    a = a.eval(ns)
    return a if not nilp(a) else b.eval(ns)

def _and(o, ns):
    a, b = list_iterator(o)
    return nil if nilp(a.eval(ns)) else b.eval(ns)

def _if(o, ns):
    a, b, c = list_iterator(o)
    return b.eval(ns) if not nilp(a.eval(ns)) else c.eval(ns)

def _div(a, b):
    try:
        return Integer(a.nb // b.nb)
    except ZeroDivisionError as err:
        raise LispError('division by zero')


# setf, eq, eql, char, length, ...
builtins = {
    'car' : func_eval(lambda o: o.car),
    'cdr' : func_eval(lambda o: nil if nilp(o) else o.cdr),
    'cons' : func_eval(lambda a, b: Cons(a, b)),
    'list' : func_eval(lambda *o: _to_list(*o)),
    'not' : func_eval(lambda o: t if nilp(o) else nil),
    'atom' : func_eval(lambda o: t if atom(o) else nil),
    'listp' : func_eval(lambda o: t if listp(o) else nil),
    'consp' : func_eval(lambda o: t if consp(o) else nil),
    'prog1' : func_eval(lambda *lst: lst[0]),
    'progn' : func_eval(lambda *lst: lst[-1]),
    'aref' : func_eval(lambda a, n: a.array[n.nb]),
    'eval' : func_eval(lambda o : o.eval()),
    'set' : func_eval_in_namespace(lsp_set),  ## need namespace
    'rplaca' : func_eval(rplaca),
    'rplacd' : func_eval(rplacd),
# arithmetic
    '+' : func_eval(lambda a, b: Integer(a.nb + b.nb)),
    '-' : func_eval(lambda a, b: Integer(a.nb - b.nb)),
    '*' : func_eval(lambda a, b: Integer(a.nb * b.nb)),
    '/' : func_eval(_div),
    '>' : func_eval(lambda a, b: t if a.nb > b.nb else nil),
    '<' : func_eval(lambda a, b: t if a.nb < b.nb else nil),
    '<=' : func_eval(lambda a, b: t if a.nb <= b.nb else nil),
    '>=' : func_eval(lambda a, b: t if a.nb >= b.nb else nil),
    '=' : func_eval(lambda a, b: t if a.nb == b.nb else nil),
    '/=' : func_eval(lambda a, b: t if a.nb != b.nb else nil),
# macros
    'setq' : macro_eval(setq),
    'push' : macro_eval(push),
    'pop' : macro_eval(pop),
#no-total evaluating
    'defun' : defun,
    'defmacro' : defmacro,
    'if' : _if,
    'and' : _and,
    'or' : _or,
#no-eval
    'quote' : lambda o, _: o.car,
}

###################################################


class Expr:
    pass


class Atom(Expr):
    def eval(self, namespace=None):
        "comportement par défaut : self-evaluating"
        return self


class Symbol(Atom):
    used = {}
    def __new__(cls, symbol):
        if symbol in Symbol.used:
            return Symbol.used[symbol]
        return super(Symbol, cls).__new__(cls, symbol)
    def __init__(self, symbol):
        assert(isinstance(symbol, str))
        if symbol in Symbol.used: return
        Symbol.used[symbol] = self
        self.symbol = symbol
    def eval(self, namespace=_Namespace):
        try:
            return namespace[self.symbol]
        except KeyError:
            raise LispError('variable ' + self.symbol + ' has no value')
    def bind(self, val, namespace):
        namespace[self.symbol] = val
        return val
    def __repr__(self):
        return self.symbol


class Integer(Atom):
    def __init__(self, nb):
        assert(isinstance(nb, int))
        self.nb = nb
    def __repr__(self):
        return repr(self.nb)


class Array(Atom):
    def __init__(self, seq):
        assert(isinstance(seq, list))
        self.array = seq
    def __repr__(self):
        return '#(' + ' '.join(repr(e) for e in self.array) + ')'

class String(Atom):
    def __init__(self, s):
        assert(isinstance(s, str))
        self.str = s
    def __repr__(self):
        return '"' + self.str + '"'

#~ def deco_dbg(fun):     
    #~ def wrap(self, ns=_Namespace):
        #~ print(' <', self, ns)
        #~ retval = fun(self, ns)
        #~ print(' >', retval)
        #~ return retval
    #~ return wrap

class _lst(list):
    def __init__(self, ref, lst):
        super().__init__(lst)
        self.ref = ref        
    

class Cons(Expr):
    def __init__(self, car, cdr):
        assert(isinstance(car, Expr))
        assert(isinstance(cdr, Expr))
        self.car = car
        self.cdr = cdr
    #@deco_dbg
    def eval(self, namespace=_Namespace):
        try:
            sym = self.car.symbol
        except:
            raise LispError(repr(self.car) + ' is not a symbol')
        if sym in builtins:
            foo = builtins[sym]
            return foo(self.cdr, namespace)
        elif sym in _Fvals:
            foo = _Fvals[sym]
            return foo(self.cdr, namespace)
        else:
            raise LispError(sym + ' is not a function/macro')
    # TODO : il faudrait gérer les listes circulaires
    def to_list(self):
        "convert to builtin list"
        return [self.car] + (self.cdr.to_list() if consp(self.cdr) else [self.cdr])

    def get_repr_list(self, visited):
        if self not in visited:
            visited[self] = None  # tmp value
            car = self.car if not consp(self.car) else self.car.get_repr_list(visited)
            cdr = [self.cdr] if not consp(self.cdr) else self.cdr.get_repr_list(visited)
            return _lst(self, [car] + cdr)
        else:
            if visited[self] is None:
                nb = len([e for e in visited.values() if e is not None])
                visited[self] = '#' + str(nb + 1)
            return _lst(self, [visited[self]])
            
    def __repr__(self):
        visited = {}
        def repr_aux(elt):
            if isinstance(elt, _lst):
                ret = '(' + ' '.join(repr_aux(e) for e in elt[:-1]) + ('' if elt[-1] is nil else ' . ' + repr_aux(elt[-1])) + ')'
                if visited[elt.ref] is not None:
                    ret = visited[elt.ref] + '=' + ret
                return ret
            elif isinstance(elt, str):
                return elt + '#'
            else:
                return repr(elt)
        lst = self.get_repr_list(visited)
        # print(lst)
        return repr_aux(lst)


# special class for representation
class Quote(Cons):
    def __repr__(self):
        return "'" + repr(self.cdr.car)


# (setq lst '((A (D) B) (E (H G) . I) E F))
# (rplacd (cdr (car (cdr (car (cdr lst))))) (car (cdr lst)))

# (setq lst '(((G E (F) A I B D)) (E . H)))
# (rplacd (cdr lst) (cdr (cdr (car (car lst)))))

# (setq lst '(E ((A B F D) . D) (H G) (I)))
# (rplacd (cdr (cdr (cdr lst))) (cdr lst))

# (setq lst '(((F) E ((E) H I . G) (B . A) D)))
# (rplacd (car (car (cdr (cdr (car lst))))) (cdr (cdr (car lst))))

# (setq lst '(I ((A) F H B . D) (D (G)) E))
# (rplacd (car (car (cdr lst))) (cdr (cdr (cdr (car (cdr lst))))))


nil = Symbol('nil')
t = Symbol('t')
