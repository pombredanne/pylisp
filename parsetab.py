
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b"\x97' O`D\xf4GM\xce\xeb]\xe1:ab"
    
_lr_action_items = {'#':([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[5,-23,5,-12,-24,5,5,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,5,-13,5,-17,-18,5,-21,-14,-19,5,-22,-15,]),"'":([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[6,-23,6,-12,-24,6,6,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,6,-13,6,-17,-18,6,-21,-14,-19,6,-22,-15,]),'NIL':([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[16,-23,16,-12,-24,16,16,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,16,-13,16,-17,-18,16,-21,-14,-19,16,-22,-15,]),'INT':([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[17,-23,17,-12,-24,17,17,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,17,-13,17,-17,-18,17,-21,-14,-19,17,-22,-15,]),'(':([0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[7,-23,7,-12,-24,21,7,7,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,7,-13,7,-17,-18,7,-21,-14,-19,7,-22,-15,]),'SYMBOL':([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[1,-23,1,-12,-24,1,1,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,1,-13,1,-17,-18,1,-21,-14,-19,1,-22,-15,]),'.':([1,3,4,10,11,12,13,14,15,16,17,19,22,23,24,25,27,28,29,31,33,],[-23,-12,-24,-11,-8,-7,-9,-5,-10,-16,-25,-6,-13,30,-17,-18,-21,-14,-19,-22,-15,]),')':([1,3,4,7,10,11,12,13,14,15,16,17,19,21,22,23,24,25,26,27,28,29,31,32,33,],[-23,-12,-24,24,-11,-8,-7,-9,-5,-10,-16,-25,-6,27,-13,28,-17,-18,31,-21,-14,-19,-22,33,-15,]),'$end':([0,1,2,3,4,8,9,10,11,12,13,14,15,16,17,18,19,20,22,24,27,28,31,33,],[-20,-23,-2,-12,-24,0,-1,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,-13,-17,-21,-14,-22,-15,]),'STRING':([0,1,2,3,4,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,],[4,-23,4,-12,-24,4,4,-11,-8,-7,-9,-5,-10,-16,-25,-3,-6,-4,4,-13,4,-17,-18,4,-21,-14,-19,4,-22,-15,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'string':([0,2,6,7,21,23,26,30,],[10,10,10,10,10,10,10,10,]),'nil':([0,2,6,7,21,23,26,30,],[11,11,11,11,11,11,11,11,]),'lsource':([0,],[2,]),'symbol':([0,2,6,7,21,23,26,30,],[13,13,13,13,13,13,13,13,]),'list':([0,2,6,7,21,23,26,30,],[19,19,19,19,19,19,19,19,]),'expr':([0,2,6,7,21,23,26,30,],[18,20,22,25,25,29,29,32,]),'source':([0,],[8,]),'quote':([0,2,6,7,21,23,26,30,],[12,12,12,12,12,12,12,12,]),'atom':([0,2,6,7,21,23,26,30,],[14,14,14,14,14,14,14,14,]),'integer':([0,2,6,7,21,23,26,30,],[15,15,15,15,15,15,15,15,]),'array':([0,2,6,7,21,23,26,30,],[3,3,3,3,3,3,3,3,]),'seq':([7,21,],[23,26,]),'empty':([0,],[9,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> source","S'",1,None,None,None),
  ('source -> empty','source',1,'p_source','/home/yoch/pylisp/pylisp/lisp_parser.py',21),
  ('source -> lsource','source',1,'p_source','/home/yoch/pylisp/pylisp/lisp_parser.py',22),
  ('lsource -> expr','lsource',1,'p_lsource','/home/yoch/pylisp/pylisp/lisp_parser.py',28),
  ('lsource -> lsource expr','lsource',2,'p_lsource','/home/yoch/pylisp/pylisp/lisp_parser.py',29),
  ('expr -> atom','expr',1,'p_expr','/home/yoch/pylisp/pylisp/lisp_parser.py',38),
  ('expr -> list','expr',1,'p_expr','/home/yoch/pylisp/pylisp/lisp_parser.py',39),
  ('expr -> quote','expr',1,'p_expr','/home/yoch/pylisp/pylisp/lisp_parser.py',40),
  ('atom -> nil','atom',1,'p_atom','/home/yoch/pylisp/pylisp/lisp_parser.py',47),
  ('atom -> symbol','atom',1,'p_atom','/home/yoch/pylisp/pylisp/lisp_parser.py',48),
  ('atom -> integer','atom',1,'p_atom','/home/yoch/pylisp/pylisp/lisp_parser.py',49),
  ('atom -> string','atom',1,'p_atom','/home/yoch/pylisp/pylisp/lisp_parser.py',50),
  ('atom -> array','atom',1,'p_atom','/home/yoch/pylisp/pylisp/lisp_parser.py',51),
  ("quote -> ' expr",'quote',2,'p_quote','/home/yoch/pylisp/pylisp/lisp_parser.py',58),
  ('list -> ( seq )','list',3,'p_list','/home/yoch/pylisp/pylisp/lisp_parser.py',65),
  ('list -> ( seq . expr )','list',5,'p_list','/home/yoch/pylisp/pylisp/lisp_parser.py',66),
  ('nil -> NIL','nil',1,'p_nil','/home/yoch/pylisp/pylisp/lisp_parser.py',76),
  ('nil -> ( )','nil',2,'p_nil','/home/yoch/pylisp/pylisp/lisp_parser.py',77),
  ('seq -> expr','seq',1,'p_seq','/home/yoch/pylisp/pylisp/lisp_parser.py',85),
  ('seq -> seq expr','seq',2,'p_seq','/home/yoch/pylisp/pylisp/lisp_parser.py',86),
  ('empty -> <empty>','empty',0,'p_empty','/home/yoch/pylisp/pylisp/lisp_parser.py',96),
  ('array -> # ( )','array',3,'p_array','/home/yoch/pylisp/pylisp/lisp_parser.py',102),
  ('array -> # ( seq )','array',4,'p_array','/home/yoch/pylisp/pylisp/lisp_parser.py',103),
  ('symbol -> SYMBOL','symbol',1,'p_symbol','/home/yoch/pylisp/pylisp/lisp_parser.py',108),
  ('string -> STRING','string',1,'p_string','/home/yoch/pylisp/pylisp/lisp_parser.py',113),
  ('integer -> INT','integer',1,'p_number','/home/yoch/pylisp/pylisp/lisp_parser.py',118),
]