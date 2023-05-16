from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from ml_conf import register_node, OP_NODE_OUTPUT
from ml_node_base import MlNode, MlGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget


class MlOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_OUTPUT)
class MlNode_Output(MlNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = MlOutputContent(self)
        self.grNode = MlGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        self.content.lbl.setText(f'{val}')
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val
