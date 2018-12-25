'''
Created on 22 Dec 2018

@author: simon
'''
from widgets import write, write_line, new_line, widget
from utilities import Model


@widget(name='MyWidget_C',
        attributes=['attr1', 'attr2'])
def myWidgetA(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('Widget C\n')
    indent()
    write('Attr1: %s\n' % model.attr1())
    write('Attr2: %s\n' % model.attr2())
    outdent()
    write('End widget C\n')
    if not kw.get('last'):
        write(',\n')
    
@widget(name='MyWidget_D', 
        attributes=['attr1', 'attr2'])
def myWidgetB(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('Widget D\n')
    indent()
    write('Attr1: %s\n' % model.attr1())
    write('Attr2: %s\n' % model.attr2())
    outdent()
    write('End widget D\n')
    if not kw.get('last'):
        write(',\n')
    
    