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
        self.filepath = "dataset/carspeed.csv"
        self.lbl = QLabel("Select a file", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.filepath
        return res

    def setupFilePath(self):
        print('updated')
        self.filepath = "dataset/carspeed.csv"

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
        self.fileBrowser.setAcceptMode(QFileDialog.AcceptOpen)
        self.fileBrowser.setOption(QFileDialog.DontUseNativeDialog, True)
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
        self.grNode.height = 200
        self.grNode.mouseDoubleClickEvent(self.content.showFileDialog())

        self.content.fileBrowser.show()

    def evalImplementation(self):
        self.value = self.content.filepath
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()
        self.content.lbl.setText(f'{self.content.filepath}')
        self.grNode.setToolTip("Selected File for Training")
        print(f'{self.content.filepath}')