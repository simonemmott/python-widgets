'''
Created on 22 Dec 2018

@author: simon
'''
import unittest, json
from widgets import WidgetFactory, widgetFactory, Assembly, write, write_line, new_line, write_container,\
    dummy_widget
from utilities.writers import StringWriter
from utilities import Indentable

class TestClassA(object):
    def __init__(self, **kw):
        self._attr1 = kw.get('attr1', None)
        self._attr2 = kw.get('attr2', None)
        self._attr3 = kw.get('attr3', None)
        self._attr4 = kw.get('attr4', None)
        
    def attr1(self, *args):
        if len(args) > 0:
            self._attr1 = args[0]
        return self._attr1

    def attr2(self, *args):
        if len(args) > 0:
            self._attr2 = args[0]
        return self._attr2
    
    def attr3(self, *args):
        if len(args) > 0:
            self._attr3 = args[0]
        return self._attr3

class TestClassB(object):
    def __init__(self, **kw):
        self._attr1 = kw.get('attr1', None)
        self._attr2 = kw.get('attr2', None)
        self._attr3 = kw.get('attr3', None)
        self._attr4 = kw.get('attr4', None)
        
    def attr1(self, *args):
        if len(args) > 0:
            self._attr1 = args[0]
        return self._attr1

    def attr2(self, *args):
        if len(args) > 0:
            self._attr2 = args[0]
        return self._attr2
    
    def attr3(self, *args):
        if len(args) > 0:
            self._attr3 = args[0]
        return self._attr3

class TestWidgetFactory(unittest.TestCase):
    
    def test_create_widgetFactory(self):
        
        wf = WidgetFactory()
        self.assertNotEqual(None, wf)

    def test_widgetFactory_add_get(self):
        
        wf = WidgetFactory()
        
        def funcA():
            return 'aaa'

        def funcB():
            return 'bbb'
        
        wf.add('FuncA', [], funcA)
        wf.add('FuncB', [], funcB)
        
        w1 = wf.get('FuncA')
        self.assertEquals(funcA, w1)
        self.assertEquals('aaa', w1())
        
        self.assertEqual(2, wf.size())

    def test_widgetFactory_export_clear(self):
        
        wf = WidgetFactory()
        
        def funcA():
            return 'aaa'

        def funcB():
            return 'bbb'
        
        wf.add('FuncA', [], funcA)
        wf.add('FuncB', [], funcB)
        wf2 = wf.export()
        
        wf.clear()
        w1 = wf.get('FuncA')
        self.assertEquals(dummy_widget, w1)
        
        
        w2 = wf2.get('FuncA')
        self.assertEquals(funcA, w2)
        self.assertEquals('aaa', w2())
        
        self.assertEqual(2, wf2.size())
        
class TestWriter(unittest.TestCase):
    
    def test_write(self):
        sw = StringWriter()
        i = Indentable()
        write(i, sw, 'aaa')
        
        self.assertEqual('aaa', sw.__str__())
        
        write(i, sw, 'bbb')
        self.assertEqual('aaabbb', sw.__str__())
        
        write(i, sw, 'ccc', 'ddd')
        self.assertEqual('aaabbbcccddd', sw.__str__())
       
        
    def test_write_line(self):
        sw = StringWriter()
        i = Indentable()
        write_line(i, sw, 'aaa')
        
        self.assertEqual('aaa\n', sw.__str__())
        
        write_line(i, sw, 'bbb')
        self.assertEqual('aaa\nbbb\n', sw.__str__())
        
        write_line(i, sw, 'ccc', 'ddd')
        self.assertEqual('aaa\nbbb\nccc\nddd\n', sw.__str__())
        
    def test_new_line(self):
        sw = StringWriter()
        i = Indentable()
        new_line(i, sw, 'aaa')
        
        self.assertEqual('\naaa', sw.__str__())
        
        new_line(i, sw, 'bbb')
        self.assertEqual('\naaa\nbbb', sw.__str__())
        
        new_line(i, sw, 'ccc', 'ddd')
        self.assertEqual('\naaa\nbbb\nccc\nddd', sw.__str__())
        
    def test_indented(self):
        sw = StringWriter()
        i = Indentable()
        
        write(i, sw, 'aaa')
        i.indent()
        new_line(i, sw, 'bbb')
        new_line(i, sw, 'bbb')
        i.indent()
        new_line(i, sw, 'ccc')
        new_line(i, sw, 'ccc')
        i.outdent()
        new_line(i, sw, 'bbb')
        new_line(i, sw, 'bbb')
        i.outdent()
        new_line(i, sw, 'aaa')
        
        ex = StringWriter()
        ex.write('aaa\n')
        ex.write('  bbb\n')
        ex.write('  bbb\n')
        ex.write('    ccc\n')
        ex.write('    ccc\n')
        ex.write('  bbb\n')
        ex.write('  bbb\n')
        ex.write('aaa')
        
        self.assertEqual(ex.__str__(), sw.__str__())
        
class TestAssembly(unittest.TestCase):
    
    def test_create_assembly(self):
        import test_widgets_a
        
        sw = StringWriter()
        
        assembly = Assembly(sw, indent='    ')
        assembly.write('aaa\n')
        assembly.indent()
        assembly.write('bbb\n')
        assembly.outdent()
        assembly.write('ccc\n')

        ex = StringWriter()
        ex.write('aaa\n')
        ex.write('    bbb\n')
        ex.write('ccc\n')
        
        self.assertEqual(ex.__str__(), sw.__str__())
        
        
    def test_assembly_get_widget(self):
        import test_widgets_a
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        self.assertNotEqual(dummy_widget, assembly.get_widget('MyWidget_A'))
        self.assertEqual(dummy_widget, assembly.get_widget('XXXX'))
        
    def test_assembly_model(self):
        import test_widgets_a
          
        sw = StringWriter()
        assembly = Assembly(sw)
        
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        
        model = assembly.model(testA, 'MyWidget_A')
        
        self.assertNotEqual(None, model)
        
        self.assertFalse(hasattr(model, 'attr1'))
        self.assertTrue(hasattr(model, 'attr2'))
        self.assertTrue(hasattr(model, 'attr3'))
        self.assertTrue(hasattr(model, 'attr4'))
        self.assertTrue(hasattr(model, 'attr5'))
        self.assertFalse(hasattr(model, 'attr6'))
        
        self.assertEqual('a2', model.attr2())
        self.assertEqual('a3', model.attr3())
        self.assertEqual('a4', model.attr4())
        self.assertEqual(None, model.attr5())

    def test_assembly_model_with_kw(self):
        import test_widgets_a
          
        sw = StringWriter()
        assembly = Assembly(sw)
        
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        
        model = assembly.model(testA, 'MyWidget_A', attr1='A1', attr2='A2', attr5='A5')
        
        self.assertNotEqual(None, model)
        
        self.assertTrue(hasattr(model, 'attr1'))
        self.assertTrue(hasattr(model, 'attr2'))
        self.assertTrue(hasattr(model, 'attr3'))
        self.assertTrue(hasattr(model, 'attr4'))
        self.assertTrue(hasattr(model, 'attr5'))
        self.assertFalse(hasattr(model, 'attr6'))
        
        self.assertEqual('A1', model.attr1())
        self.assertEqual('A2', model.attr2())
        self.assertEqual('a3', model.attr3())
        self.assertEqual('a4', model.attr4())
        self.assertEqual('A5', model.attr5())

class TestWidget(unittest.TestCase):
    
    def test_widget_factory_a(self):
        
        import test_widgets_a
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        self.assertTrue('MyWidget_A' in assembly.widgetFactory.get_widget_names())
        self.assertTrue('MyWidget_B' in assembly.widgetFactory.get_widget_names())
        
        self.assertEqual(['attr2', 'attr3', 'attr4', 'attr5'], assembly.widgetFactory.get_attributes('MyWidget_A'))
        self.assertEqual(['attr1', 'attr2', 'attr3', 'attr4'], assembly.widgetFactory.get_attributes('MyWidget_B'))
        

        assembly.get_widget('MyWidget_A')(assembly, assembly.model({}, 'MyWidget_A'), {}, last=True)       
        ex = StringWriter()
        ex.write('aaa\n')
        ex.write('  bbb\n')
        ex.write('  bbb\n')
        ex.write('    ccc\n')
        ex.write('    ccc\n')
        ex.write('  bbb\n')
        ex.write('  bbb\n')
        ex.write('aaa\n')  
        self.assertEqual(ex.__str__(), sw.__str__())
        
        sw = StringWriter()
        assembly = Assembly(sw)
        assembly._indent_str = '    '
        assembly.get_widget('MyWidget_B')(assembly, assembly.model({}, 'MyWidget_B'), {}, last=True)      
        ex = StringWriter()
        ex.write('AAA\n')
        ex.write('    BBB\n')
        ex.write('    BBB\n')
        ex.write('        CCC\n')
        ex.write('        CCC\n')
        ex.write('    BBB\n')
        ex.write('    BBB\n')
        ex.write('AAA\n')  
        self.assertEqual(ex.__str__(), sw.__str__())
        
    def test_widget_factory_b(self):
        
        import test_widgets_b
        
        self.assertTrue('MyWidget_C' in widgetFactory.get_widget_names())
        self.assertTrue('MyWidget_D' in widgetFactory.get_widget_names())
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        widgetFactory.get('MyWidget_C')(assembly, assembly.model({}, 'MyWidget_C'), {}, last=True)       
        ex = StringWriter()
        ex.write('Widget C\n')
        ex.write('  Attr1: None\n')
        ex.write('  Attr2: None\n')
        ex.write('End widget C\n')  
        self.assertEqual(ex.__str__(), sw.__str__())
        
        sw = StringWriter()
        assembly = Assembly(sw)
        assembly._indent_str = '    '
        widgetFactory.get('MyWidget_D')(assembly, assembly.model({}, 'MyWidget_D'), {}, last=True)       
        ex = StringWriter()
        ex.write('Widget D\n')
        ex.write('    Attr1: None\n')
        ex.write('    Attr2: None\n')
        ex.write('End widget D\n')  
        self.assertEqual(ex.__str__(), sw.__str__())
        
        sw = StringWriter()
        assembly = Assembly(sw)
        assembly._indent_str = '    '
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        widgetFactory.get('MyWidget_D')(assembly, assembly.model(testA, 'MyWidget_D'), {}, last=True)       
        ex = StringWriter()
        ex.write('Widget D\n')
        ex.write('    Attr1: a1\n')
        ex.write('    Attr2: a2\n')
        ex.write('End widget D\n')  
        self.assertEqual(ex.__str__(), sw.__str__())
        
    def test_widget_factory_my_assembly_a(self):
        
        import test_widgets_c
        
        self.assertTrue('MyWidget_E' in widgetFactory.get_widget_names())
        self.assertTrue('MyWidget_F' in widgetFactory.get_widget_names())
        self.assertTrue('MyAssembly_A' in widgetFactory.get_widget_names())
        self.assertTrue('MyAssembly_B' in widgetFactory.get_widget_names())
        self.assertTrue('MyAssembly_C' in widgetFactory.get_widget_names())
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        assembly.get_widget('MyAssembly_A')(assembly, assembly.model({}, 'MyAssembly_A'), {})       
        ex = StringWriter()
        ex.write('Widget E\n')
        ex.write('Attr1: \n')
        ex.write('Attr2: \n')
        ex.write('Container A [\n')  
        ex.write('] Container A\n')  
        ex.write('Container B [\n')  
        ex.write('] Container B\n')  
        ex.write('End widget E\n')  
        
        self.assertEqual(ex.__str__(), sw.__str__())

    def test_widget_factory_my_assembly_b(self):
        
        import test_widgets_c
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        widgetFactory.get('MyAssembly_B')(assembly, assembly.model({}, 'MyAssembly_B'), {})       
        ex = StringWriter()
        ex.write('Widget E\n')
        ex.write('Attr1: \n')
        ex.write('Attr2: \n')
        ex.write('Container A [\n')  
        ex.write('  aaa\n')  
        ex.write('  aaa\n')  
        ex.write('  aaa\n')  
        ex.write('  ,\n')  
        ex.write('  bbb\n')  
        ex.write('  bbb\n')  
        ex.write('  bbb\n')  
        ex.write('] Container A\n')  
        ex.write('Container B [\n')  
        ex.write('] Container B\n')  
        ex.write('End widget E\n')  
        
        self.assertEqual(ex.__str__(), sw.__str__())

    def test_widget_factory_my_assembly_c(self):
        
        self.maxDiff = None
        
        import test_widgets_a, test_widgets_b, test_widgets_c
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        testB1 = TestClassB(attr1='B1.1', attr2='B1.2', attr3='B1.3', attr4='B1.4')
        testB2 = TestClassB(attr1='B2.1', attr2='B2.2', attr3='B2.3', attr4='B2.4')
        testA = TestClassA(attr1='A1', attr2='A2', attr3=[testB1, testB2], attr4=testB2)
        
        widgetFactory.get('MyAssembly_C')(assembly, 
                                          assembly.model({}, 'MyAssembly_C', 
                                                         attr1='a1', 
                                                         attr2='a2',
                                                         attr3=testA), {})       
        ex = StringWriter()
        ex.write('Widget E\n')
        ex.write('Attr1: a1\n')
        ex.write('Attr2: a2\n')
        ex.write('Container A [\n')  
        ex.write('  aaa\n')  
        ex.write('    bbb\n')  
        ex.write('    bbb\n')  
        ex.write('      ccc\n')  
        ex.write('      ccc\n')  
        ex.write('    bbb\n')  
        ex.write('    bbb\n')  
        ex.write('  aaa\n')  
        ex.write('  ,\n')  
        ex.write('  AAA\n')  
        ex.write('    BBB\n')  
        ex.write('    BBB\n')  
        ex.write('      CCC\n')  
        ex.write('      CCC\n')  
        ex.write('    BBB\n')  
        ex.write('    BBB\n')  
        ex.write('  AAA\n')  
        ex.write('] Container A\n')  
        ex.write('Container B [\n')  
        ex.write('  Widget F\n')  
        ex.write('  Attr1: A1\n')  
        ex.write('  Attr2: A2\n')  
        ex.write('  Container A [\n')  
        ex.write('    Widget C\n')  
        ex.write('      Attr1: B1.1\n')  
        ex.write('      Attr2: B1.2\n')  
        ex.write('    End widget C\n')  
        ex.write('    ,\n')  
        ex.write('    Widget C\n')  
        ex.write('      Attr1: B2.1\n')  
        ex.write('      Attr2: B2.2\n')  
        ex.write('    End widget C\n')  
        ex.write('  ] Container A\n')  
        ex.write('  Container B [\n')  
        ex.write('    Widget D\n')  
        ex.write('      Attr1: B2.1\n')  
        ex.write('      Attr2: B2.2\n')  
        ex.write('    End widget D\n')  
        ex.write('  ] Container B\n')  
        ex.write('  End widget F\n')  
        ex.write('] Container B\n')  
        ex.write('End widget E\n')  
        
        self.assertEqual(ex.__str__(), sw.__str__())

    def test_widget_factory_my_assembly_d(self):
        
        self.maxDiff = None
        
        import test_widgets_a, test_widgets_b, test_widgets_c
        
        sw = StringWriter()
        assembly = Assembly(sw)
        
        testB1 = TestClassB(attr1='B1.1', attr2='B1.2', attr3='B1.3', attr4='B1.4')
        testB2 = TestClassB(attr1='B2.1', attr2='B2.2', attr3='B2.3', attr4='B2.4')
        testA = TestClassA(attr1='A1', attr2='A2', attr3=[testB1, testB2], attr4=testB2)
        
        widgetFactory.get('MyAssembly_D')(assembly, 
                                          assembly.model({}, 'MyAssembly_D', 
                                                         attr1='a1', 
                                                         attr2='a2',
                                                         attr3=testA), {})       
        ex = StringWriter()
        ex.write('Widget E\n')
        ex.write('Attr1: a1\n')
        ex.write('Attr2: a2\n')
        ex.write('Container A [\n')  
        ex.write('  aaa\n')  
        ex.write('    bbb\n')  
        ex.write('    bbb\n')  
        ex.write('      ccc\n')  
        ex.write('      ccc\n')  
        ex.write('    bbb\n')  
        ex.write('    bbb\n')  
        ex.write('  aaa\n')  
        ex.write('  ,\n')  
        ex.write('  AAA\n')  
        ex.write('    BBB\n')  
        ex.write('    BBB\n')  
        ex.write('      CCC\n')  
        ex.write('      CCC\n')  
        ex.write('    BBB\n')  
        ex.write('    BBB\n')  
        ex.write('  AAA\n')  
        ex.write('] Container A\n')  
        ex.write('Container B [\n')  
        ex.write('  Widget F\n')  
        ex.write('  Attr1: A1\n')  
        ex.write('  Attr2: A2\n')  
        ex.write('  Container A [\n')  
        ex.write('    Widget C\n')  
        ex.write('      Attr1: B1.1\n')  
        ex.write('      Attr2: B1.2\n')  
        ex.write('    End widget C\n')  
        ex.write('    ,\n')  
        ex.write('    Widget C\n')  
        ex.write('      Attr1: B2.1\n')  
        ex.write('      Attr2: B2.2\n')  
        ex.write('    End widget C\n')  
        ex.write('  ] Container A\n')  
        ex.write('  Container B [\n')  
        ex.write('    Widget D\n')  
        ex.write('      Attr1: A1\n')  
        ex.write('      Attr2: A2\n')  
        ex.write('    End widget D\n')  
        ex.write('  ] Container B\n')  
        ex.write('  End widget F\n')  
        ex.write('] Container B\n')  
        ex.write('End widget E\n')  
        
        self.assertEqual(ex.__str__(), sw.__str__())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()