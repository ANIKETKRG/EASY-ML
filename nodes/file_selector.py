# file selection widdget
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QLabel

from ml_conf import register_node, OP_NODE_BROWSE_FILE
from ml_node_base import MlNode, MlGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


class FileInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("Select a file", self)
        self.lbl.setObjectName(self.node.content_label_objname)
        self.lbl.wordWrap = True
        self.lbl.setMinimumWidth(250)
        self.filepath = "dataset/carspeed.csv"
        self.is_file_selected = False
        print(f'1 {self.filepath}')

    def serialize(self):
        res = super().serialize()
        res['value'] = self.filepath
        return res

    def setupFilePath(self):
        print('updated', self.fileBrowser.selectedFiles()[0])
        self.lbl.setText(f'{self.filepath.split("/")[-1]}')
        self.filepath = self.fileBrowser.selectedFiles()[0]
        self.is_file_selected = True
        print(f'2 {self.filepath}')
       

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.fileBrowser.setDirectory(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

    def showFileDialog(self):
        self.fileBrowser = QFileDialog(self)
        self.fileBrowser.setFileMode(QFileDialog.AnyFile)
        self.fileBrowser.fileSelected.connect(self.setupFilePath)
        self.fileBrowser.show()


@register_node(OP_NODE_BROWSE_FILE)
class MlnodeBrowser(MlNode):
    icon = "icons/in.png"
    op_code = OP_NODE_BROWSE_FILE
    op_title = "Browse file"
    content_label_objname = "ml_node_browse"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = FileInputContent(self)
        self.grNode = MlGraphicsNode(self)
        self.grNode.height = 100
      

    def evalImplementation(self):
        if not self.content.is_file_selected:
            self.content.showFileDialog()
        else:
            self.value = self.content.filepath
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsInvalid(False)
            self.markDescendantsDirty()
            print(f'3 {self.content.filepath}')
            self.content.lbl.setText(f'{self.content.filepath.split("/")[-1]}')
            self.grNode.setToolTip("Selected File for Training")
            self.evalChildren()
        

    
