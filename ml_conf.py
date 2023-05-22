LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6
OP_NODE_BROWSE_FILE = 7
OP_NODE_CSV_READER = 8
OP_NODE_CSV_WRITER = 9
OP_NODE_SPLITTER = 10
OP_NODE_LINEAR_REGRESSION = 11
OP_NODE_POLYNOMIAL_REGRESSION = 12
OP_NODE_STANDARD_SCALER = 13
OP_NODE_ORDINAL_ENCODER = 14
OP_NODE_ONE_HOT_ENCODER = 15
OP_NODE_POLYNOMIAL_FEATURES = 16
OP_NODE_SVM_REGRESSION = 17
OP_NODE_SVM_CLASSIFICATION = 18
OP_NODE_KNN_REGRESSION = 19
OP_NODE_KNN_CLASSIFICATION = 20


ML_NODES = {
}


class ConfException(Exception): pass


class InvalidNodeRegistration(ConfException): pass


class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in ML_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, ML_NODES[op_code]
        ))
    ML_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class

    return decorator


def get_class_from_opcode(op_code):
    if op_code not in ML_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return ML_NODES[op_code]


# import all nodes and register them
from nodes import *
