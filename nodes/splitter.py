from ml_conf import register_node, OP_NODE_SPLITTER
from ml_node_base import MlNode
import pandas as pd
from sklearn.model_selection import train_test_split
import os

@register_node(OP_NODE_SPLITTER)
class MlNode_Splitter(MlNode):
    icon = "icons/split.png"
    op_code = OP_NODE_SPLITTER
    op_title = "Splitter"
    content_label = "Splitter"
    content_label_objname = "ml_node_bg"

    # take filepath as input
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()
    
    def evalOperation(self, filepath):
        print(os.listdir('dataset'))
        df = pd.read_csv(filepath, nrows=10000)
        print(f'Loaded {filepath} with {len(df)} rows')
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        return[X_train, X_test, y_train, y_test]
    
    def evalImplementation(self):
        val = self.evalOperation(self.getInput(0).eval())
        self.value = val
        self.markDirty(False)
        self.markInvalid(False)
        self.grNode.setToolTip("")
        self.markDescendantsDirty()
        self.evalChildren()
        return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value
        try:
            val = self.evalImplementation()
            return val
        except Exception as e:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip(str(e))
            print(e)
            return None
        
    
