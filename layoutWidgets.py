from ipywidgets import interact, interactive, HBox, Layout,VBox
from IPython.display import clear_output, display, HTML

def layout(w):
    controls = HBox(w.children[:-1], layout = Layout(flex_flow='row wrap'))
    output = w.children[-1]
    output.layout.height = '550px'
    display(VBox([controls, output]))
    #without this ping - the visualization would only update when someone actually interacts with the controls
    w.children[1].value=w.children[1].value+1
    w.children[1].value=w.children[1].value-1