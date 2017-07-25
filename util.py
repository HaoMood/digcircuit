"""Common gates and propositional units for digital circuits.

This file is also a demo of how to use the digcircuit module.
"""

from __future__ import division, print_function

__all__ = ['XorGate', 'XNorGate']
__author__ = 'Hao Zhang'
__copyright__ = 'Copyright @2017'
__date__ = '2017-07-25'
__email__ = 'zhangh0214@gmail.com'
__license__ = 'CC BY-SA 3.0'
__status__ = 'Development'
__updated__ = '2017-07-25'
__version__ = '1.0'

import digcircuit


class XorGate(object):
    """Xor gate with two inputs and one output.

    See res/xor_gate.jpg for the architecture of the XOR gate.

    Attributes:
        _label (str): Name of the gate for identification.
        _input_a (int {0, 1}): One input of the gate.
        _input_b (int {0, 1}): Another input of the gate.
        _gates (dict of (str, digcircuit._LogicGate)): All gates needed.
        _connectors (dict of (str, digcircuit.Connector)): All connectors
            needed.

    >>> xor_gate = XorGate('xor')
    >>> xor_gate.setInput(1, 1)
    >>> xor_gate.getOutput()
    0
    >>> xor_gate.setInput(1, 0)
    >>> xor_gate.getOutput()
    1
    >>> xor_gate.setInput(0, 1)
    >>> xor_gate.getOutput()
    1
    >>> xor_gate.setInput(1, 1)
    >>> xor_gate.getOutput()
    0
    """
    def __init__(self, label):
        self._input_a = None
        self._input_b = None
        self._label = label

        self._gates = {}
        self._gates['not_a'] = digcircuit.NotGate('not_a')
        self._gates['not_b'] = digcircuit.NotGate('not_b')
        self._gates['and_1'] = digcircuit.AndGate('add_1')
        self._gates['and_2'] = digcircuit.AndGate('add_2')
        self._gates['or'] = digcircuit.OrGate('or')

        self._connectors = {}
        self._connectors['not_a_to_and_1'] = digcircuit.Connector(
            self._gates['not_a'], self._gates['and_1'])
        self._connectors['not_b_to_and_2'] = digcircuit.Connector(
            self._gates['not_b'], self._gates['and_2'])
        self._connectors['and_1_to_or'] = digcircuit.Connector(
            self._gates['and_1'], self._gates['or'])
        self._connectors['and_2_to_or'] = digcircuit.Connector(
            self._gates['and_2'], self._gates['or'])

    def setInput(self, input_a, input_b):
        digcircuit.checkInputValid(input_a)
        digcircuit.checkInputValid(input_b)
        self._input_a = input_a
        self._input_b = input_b

        self._gates['not_a'].setInput(self._input_a)
        self._gates['not_b'].setInput(self._input_b)
        self._gates['and_1'].setInput(input_b=self._input_b)
        self._gates['and_2'].setInput(input_b=self._input_a)

    def getLabel(self):
        return self._label

    def getOutput(self):
        return self._gates['or'].getOutput()


class XNorGate(object):
    """XNor gate with two inputs and one output.

    Attributes:
        _label (str): Name of the gate for identification.
        _input_a (int {0, 1}): One input of the gate.
        _input_b (int {0, 1}): Another input of the gate.
        _gates (dict of (str, digcircuit._LogicGate)): All gates needed.
        _connectors (dict of (str, digcircuit.Connector)): All connectors
            needed.

    >>> xnor_gate = XNorGate('xnor')
    >>> xnor_gate.setInput(1, 1)
    >>> xnor_gate.getOutput()
    1
    >>> xnor_gate.setInput(1, 0)
    >>> xnor_gate.getOutput()
    0
    >>> xnor_gate.setInput(0, 1)
    >>> xnor_gate.getOutput()
    0
    >>> xnor_gate.setInput(1, 1)
    >>> xnor_gate.getOutput()
    1
    """
    def __init__(self, label):
        self._input_a = None
        self._input_b = None
        self._label = label

        self._gates = {}
        self._gates['xor'] = XorGate('xor')
        self._gates['not'] = digcircuit.NotGate('not')

        self._connectors = {}
        self._connectors['xor_to_not'] = digcircuit.Connector(
            self._gates['xor'], self._gates['not'])

    def setInput(self, input_a, input_b):
        digcircuit.checkInputValid(input_a)
        digcircuit.checkInputValid(input_b)
        self._input_a = input_a
        self._input_b = input_b

        self._gates['xor'].setInput(self._input_a, self._input_b)

    def getLabel(self):
        return self._label

    def getOutput(self):
        return self._gates['not'].getOutput()


def test():
    """Test code for this module.

    Run "python -v gate.py" to see the results.
    """
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()
