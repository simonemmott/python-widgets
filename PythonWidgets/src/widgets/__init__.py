from utilities import classUtil, typeUtil, Indentable, Model
from utilities.writers import IndentableWriter

class Assembly(IndentableWriter):
    def __init__(self, writer, **kw):
        IndentableWriter.__init__(self, writer, **kw)           
        self.widgetFactory = kw.get('widgetFactory', widgetFactory)
        
    def get_widget(self, name):
        return self.widgetFactory.get(name)
    
    def model(self, src, widget_name, **kw):
        attrs = self.widgetFactory.get_attributes(widget_name)
        return Model(src, *attrs, **kw)


def write(assembly, writer, *msgs):
    for msg in msgs:
        msg.replace('\n', '\n'+assembly.get_indent())
        writer.write(msg)

def write_line(assembly, writer, *msgs):
    for msg in msgs:
        writer.write(msg)
        writer.write('\n')
        writer.write(assembly.get_indent())
        
            
def new_line(assembly, writer, *msgs):
    for msg in msgs:
        writer.write('\n')
        writer.write(assembly.get_indent())
        writer.write(msg)
        
def write_container(assembly, writer, src, ctx, container):
    print("write_container: "+container)
    if hasattr(ctx, 'container'):
        print('Context has container')
        contents = ctx.container(container)
    else:
        print('Context has NO container')
        return
    
    for i in range(len(contents)):
        is_first = i==0
        is_last = i==len(contents)-1
        cw = contents[i]
        widget = assembly.widgetFactory.get(cw.widget)
        if cw.bound_to == None:
            _src = src
        else:
            _src = src.get(cw.bound_to)
        if typeUtil.is_collection(_src):
            
            for j in range(len(_src)):
                s = _src[j]
                j_is_first = j==0 and is_first
                j_is_last = j==len(_src)-1 and is_last
                widget(assembly, writer, s, cw, first=j_is_first, last=j_is_last)
        else:
            widget(assembly, writer, _src, cw, first=is_first, last=is_last)
            
    
        
def dummy_widget(assembly, model, ctx, **kw):
    return
        
class WidgetFactory(object):
    def __init__(self):
        self.widgets = {}
        self.attributes = {}
        
    def add(self, name, attributes, widget):
        self.widgets[name] = widget
        self.attributes[name] = attributes
        
    def get(self, name):
        return self.widgets.get(name, dummy_widget)
    
    def get_attributes(self, name):
        return self.attributes.get(name, [])
    
    def size(self):
        return len(self.widgets)
    
    def get_widget_names(self):
        return self.widgets.keys()
    
    def clear(self):
        self.widgets = {}
        self.attributes = {}
    
    def export(self):
        wf = WidgetFactory()
        for name in self.get_widget_names():
            wf.add(name, self.get_attributes(name), self.get(name))
        return wf
    
    def export_and_clear(self):
        wf = self.export()
        self.clear()
        return wf
    
        
widgetFactory = WidgetFactory()

class WidgetAssembly(object):
    def __init__(self, widget, *contained_widgets):
        self.widget = widget
        self.contained_widgets = {}
        if len(contained_widgets) == 1:
            for cw in contained_widgets[0]:
                self.contains(cw)
        
    def contains(self, contained_widget):
        container = self.contained_widgets.get(contained_widget.in_container, [])
        container.append(contained_widget)
        self.contained_widgets[contained_widget.in_container] = container
    
    def write(self, assembly, model, ctx, **kw):
        assembly.widgetFactory.get(self.widget)(assembly, model, self, **kw)
        
    def container(self, name):
        return self.contained_widgets.get(name, [])
    
    def wite_container(self, assembly, model, name):
        if self.contained_widgets.__contains__(name):
            contents = self.contained_widgets.get(name, [])
        else:
             return
        
        for i in range(len(contents)):
            is_first = i==0
            is_last = i==len(contents)-1
            cw = contents[i]
            widget = assembly.get_widget(cw.widget)
            if cw.bound_to == None:
                src = model
                assembly.model(model, cw.widget)
            else:
                if callable(cw.bound_to):
                    src = cw.bound_to()
                else:
                    src = model.get(cw.bound_to)
            if typeUtil.is_collection(src):
                
                for j in range(len(src)):
                    _src = src[j]
                    j_is_first = j==0 and is_first
                    j_is_last = j==len(src)-1 and is_last
                    widget(assembly, assembly.model(_src, cw.widget), cw, first=j_is_first, last=j_is_last)
            else:
                widget(assembly, assembly.model(src, cw.widget), cw, first=is_first, last=is_last)
        
        
 
class ContainedWidget(WidgetAssembly):
    def __init__(self, widget, bound_to, in_container, *contained_widgets):
        self.bound_to = bound_to
        self.in_container = in_container   
        WidgetAssembly.__init__(self, widget, *contained_widgets)
     
  

        
def widget(**kw):
    def decorator(func):
        widgetFactory.add(kw.get('name', func.__name__), kw.get('attributes', []), func)
        return func
    return decorator
    
def widget_assembly(**kw):
    def decorator(func):
        widgetFactory.add(kw.get('name', func.__name__), kw.get('attributes', []), func)
        return func
    return decorator
    




