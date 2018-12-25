'''
Created on 22 Dec 2018

@author: simon
'''
from widgets import write, write_line, new_line, widget, widget_assembly, write_container, WidgetAssembly, ContainedWidget
from utilities import Model


@widget(name='MyWidget_E',
        attributes=['attr1', 'attr2'])
def myWidgetA(assembly, model, ctx, **kw):   
    def write(msg): assembly.write(msg)
    def container(cont): ctx.wite_container(assembly, model, cont)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('Widget E\n')
    write('Attr1: %s\n' % (model.attr1() if model.attr1() != None else ''))
    write('Attr2: %s\n' % (model.attr2() if model.attr2() != None else ''))
    write('Container A [\n')
    indent()
    container('A')
    outdent()
    write('] Container A\n')
    write('Container B [\n')
    indent()
    container('B')
    outdent()
    write('] Container B\n')
    write('End widget E\n')
    
@widget(name='MyWidget_F',
        attributes=['attr1', 'attr2', 'attr3', 'attr4'])
def myWidgetB(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def container(cont): ctx.wite_container(assembly, model, cont)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('Widget F\n')
    write('Attr1: %s\n' % (model.attr1() if model.attr1() != None else ''))
    write('Attr2: %s\n' % (model.attr2() if model.attr2() != None else ''))
    write('Container A [\n')
    indent()
    container('A')
    outdent()
    write('] Container A\n')
    write('Container B [\n')
    indent()
    container('B')
    outdent()
    write('] Container B\n')
    write('End widget F\n')
    
@widget(name='AAA',
        attributes=['attr1', 'attr2'])
def aaa(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('aaa\n')
    write('aaa\n')
    write('aaa\n')
    if not kw.get('last'):
        write(',\n')
    

@widget(name='BBB',
        attributes=['attr1', 'attr2'])
def bbb(assembly, model, ctx, **kw):
    def write(msg): assembly.write(msg)
    def indent(): assembly.indent()
    def outdent(): assembly.outdent()
    
    write('bbb\n')
    write('bbb\n')
    write('bbb\n')
    if not kw.get('last'):
        write(',\n')

    
@widget_assembly(name='MyAssembly_A',
                 attributes=['attr1', 'attr2'])    
def myWidgetAssemnlyA(assembly, model, ctx, **kw):
    wa = WidgetAssembly('MyWidget_E')
    wa.write(assembly, model, ctx, **kw)

@widget_assembly(name='MyAssembly_B',
                 attributes=['attr1', 'attr2'])    
def myWidgetAssemnlyB(assembly, model, ctx, **kw):
    wa = WidgetAssembly('MyWidget_E', [
        ContainedWidget('AAA', None, 'A'),
        ContainedWidget('BBB', None, 'A'),
        ])
    wa.write(assembly, model, ctx, **kw)

@widget_assembly(name='MyAssembly_C',
                 attributes=['attr1', 'attr2', 'attr3'])    
def myWidgetAssemnlyC(assembly, model, ctx, **kw):
    wa = WidgetAssembly('MyWidget_E', [
        ContainedWidget('MyWidget_A', 'attr1', 'A'),
        ContainedWidget('MyWidget_B', 'attr2', 'A'),
        ContainedWidget('MyWidget_F', 'attr3', 'B', [
            ContainedWidget('MyWidget_C', 'attr3', 'A'),
            ContainedWidget('MyWidget_D', 'attr4', 'B'),
            ]),
        ])
    wa.write(assembly, model, ctx, **kw)

@widget_assembly(name='MyAssembly_D',
                 attributes=['attr1', 'attr2', 'attr3'])    
def myWidgetAssemnlyD(assembly, model, ctx, **kw):
    wa = WidgetAssembly('MyWidget_E', [
        ContainedWidget('MyWidget_A', 'attr1', 'A'),
        ContainedWidget('MyWidget_B', 'attr2', 'A'),
        ContainedWidget('MyWidget_F', 'attr3', 'B', [
            ContainedWidget('MyWidget_C', 'attr3', 'A'),
            ContainedWidget('MyWidget_D', model.attr3, 'B'),
            ]),
        ])
    wa.write(assembly, model, ctx, **kw)
    