'''
Created on 22 Dec 2018

@author: simon
'''
from widgets import write, write_line, new_line, widget
from utilities import Model


@widget(name='MyWidget_A',
        attributes=['attr2', 'attr3', 'attr4', 'attr5'])
def myWidgetA(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('aaa\n')
    indent()
    write('bbb\n')
    write('bbb\n')
    indent()
    write('ccc\n')
    write('ccc\n')
    outdent()
    write('bbb\n')
    write('bbb\n')
    outdent()
    write('aaa\n')
    if not kw.get('last'):
        write(',\n')
    
@widget(name='MyWidget_B',
        attributes=['attr1', 'attr2', 'attr3', 'attr4'])
def myWidgetB(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    
    write('AAA\n')
    indent()
    write('BBB\n')
    write('BBB\n')
    indent()
    write('CCC\n')
    write('CCC\n')
    outdent()
    write('BBB\n')
    write('BBB\n')
    outdent()
    write('AAA\n')
    if not kw.get('last'):
        write(',\n')
    

    
    
    