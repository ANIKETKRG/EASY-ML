from sklearn.metrics import mean_squared_error, r2_score
from ml_conf import register_node, OP_NODE_LINEAR_REGRESSION
from ml_node_base import MlNode
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os

@register_node(OP_NODE_LINEAR_REGRESSION)
class MlNode_LinearRegression(MlNode):
    icon = "icons/linear_reg.png"
    op_code = OP_NODE_LINEAR_REGRESSION
    op_title = "Linear Regression"
    content_label = "Linear Regression"
    content_label_objname = "ml_node_bg"


    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()
    
    def evalOperation(self, datalist):
        X_train = datalist[0]
        X_test = datalist[1]
        y_train = datalist[2]
        y_test = datalist[3]
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)
        m = self.create_metrics_dict(regressor, X_test, y_test)
        self.content.wdg_label.setText(f"Linear Regression\nmse: {m['Mean squared error']}\naccuracy: {m['Coefficient of determination']} ")
        return regressor
    
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

    def create_metrics_dict(self,model, X, y):
        y_pred = model.predict(X)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        print(f'Mean squared error: {mse}')
        print(f'Coefficient of determination: {r2}')
        
        return {'Mean squared error': mse, 'Coefficient of determination': r2}