from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ml_conf import register_node, OP_NODE_SVM_CLASSIFICATION, OP_NODE_KNN_CLASSIFICATION
from ml_node_base import MlNode
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

@register_node(OP_NODE_SVM_CLASSIFICATION)
class MlNode_SVMClassification(MlNode):
    icon = "icons/svm.png"
    op_code = OP_NODE_SVM_CLASSIFICATION
    op_title = "SVM Classification"
    content_label = "Support vector classification"
    content_label_objname = "ml_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()

    def evalOperation(self, datalist):
        X_train = datalist[0]
        X_test = datalist[1]
        y_train = datalist[2]
        y_test = datalist[3]
        classifier = SVC(random_state=0)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        m = self.create_metrics_dict(y_test, y_pred)
        self.content_label=f"{m['acc']}"
        return m
    
    def evalImplementation(self):
        val = self.evalOperation(self.getInput(0).eval())
        self.value = val['acc']
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
            return val['acc']
        except Exception as e:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip(str(e))
            print(e)
            return None
        
    def create_metrics_dict(self,y_test, y_pred):
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        prec = precision_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')
        return {'acc':acc, 'f1':f1, 'prec':prec, 'rec':rec}
    
@register_node(OP_NODE_KNN_CLASSIFICATION)
class MlNode_KNNClassification(MlNode):
    icon = "icons/knn.png"
    op_code = OP_NODE_KNN_CLASSIFICATION
    op_title = "KNN Classification"
    content_label = "K-nearest neighbors classification"
    content_label_objname = "ml_node_bg"    

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()

    def evalOperation(self, datalist):
        X_train = datalist[0]
        X_test = datalist[1]
        y_train = datalist[2]
        y_test = datalist[3]
        classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        m = self.create_metrics_dict(y_test, y_pred)
        self.content_label=f"{m['acc']}"
        return m
    
    def evalImplementation(self):
        val = self.evalOperation(self.getInput(0).eval())
        self.value = val['acc']
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
            return val['acc']
        except Exception as e:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip(str(e))
            print(e)
            return None
        
    def create_metrics_dict(self,y_test, y_pred):
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        prec = precision_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')
        return {'acc':acc, 'f1':f1, 'prec':prec, 'rec':rec}
    