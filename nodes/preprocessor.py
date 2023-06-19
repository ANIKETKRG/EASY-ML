
from ml_conf import register_node, OP_NODE_STANDARD_SCALER
from ml_node_base import MlNode
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

@register_node(OP_NODE_STANDARD_SCALER)
class MlNode_StandardScaler(MlNode):
    icon = "icons/standard_scaler.png"
    op_code = OP_NODE_STANDARD_SCALER
    op_title = "Standard Scaler"
    content_label = "Scale the data"
    content_label_objname = "ml_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()

    def evalOperation(self, datalist):
        X_train = datalist[0]
        X_test = datalist[1]
        y_train = datalist[2]
        y_test = datalist[3]
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        return X_train, X_test, y_train, y_test
    
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
            return self.value[0][0]
        try:
            val = self.evalImplementation()
            return val
        except Exception as e:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip(str(e))
            print(e)
            return None
        
