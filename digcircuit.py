"""A simulation of digital circuits.

The basic building blocks for this simulation are logic gates, such as and, or,
and not. These electronic switches represent boolean algebra relationships
between their input and their output. The value of the output is dependent on
the values given on the input lines. We use 0 and 1 to represent False and
True, repectively.

The class inheritance hierarchy is:
    LogicGate <- BinaryGate  <- AndGate, OrGate
              <- UnaryGate   <- NotGate

By combining these gates in various patterns and then applying a set of input
values, we can build circuits that have logical functions.
"""

from __future__ import division, print_function

__all__ = ['AndGate', 'OrGate', 'NotGate', 'Connector', 'checkInputValid']
__author__ = 'Hao Zhang'
__copyright__ = 'Copyright @2017'
__date__ = '2017-07-24'
__email__ = 'zhangh0214@gmail.com'
__license__ = 'CC BY-SA 3.0'
__status__ = 'Development'
__updated__ = '2017-07-25'
__version__ = '2.2'  # No need to call setInput for every gate.


def checkInputValid(args):
    """Helper function to check whether the input(s) is/are valid, i.e., 0 or 1.

    Args:
        args (int): An input.

    Raises:
        ValueError: If input is not 0 or 1.
    """
    if not (isinstance(args, int) and (args == 1 or args == 0)):
        raise ValueError('The input must be 0 or 1.')


class _LogicGate(object):
    """The very most basic class of all digit gates.

    It represents the most general characteristics of logic gates.

    Attributes:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
    """

    def __init__(self, label):
        self._label = label
        self._output = None

    def getLabel(self):
        return self._label

    def getOutput(self):
        self._output = self._forward()
        return self._output

    def _forward(self):
        """Compute the output value based on input and the gate's logic.

        This is a pure virtual function, such that any new logic gate that gets
        added to the hierarchy will need to implement their own forward()
        function.
        """
        raise NotImplementedError


class _BinaryGate(_LogicGate):
    """Gate with two inputs.

    Attributes:
        _input_a (int {0, 1}): One input of the gate.
        _input_b (int {0, 1}): Another input of the gate.
        _is_connected_a (bool): Whether _input_a is connected to a connector.
        _is_connected_b (bool): Whether _input_b is connected to a connector.
        _input_connector_a (Connector): Connector to _input_a, if possible.
        _input_connector_b (Connector): Connector to _input_b, if possible.

    Attributes from Base Class:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
    """

    def __init__(self, label):
        _LogicGate.__init__(self, label)
        self._input_a = None
        self._input_b = None
        self._is_connected_a = False
        self._is_connected_b = False
        self._input_connector_a = None
        self._input_connector_b = None

    def setInput(self, input_a=None, input_b=None):
        """Set the input_a and input_b from user input or a connector.

        If the input is not connected to a Connector, then uses the user's
        input.

        Args:
            self (_BinaryGate): A class instance.
            input_a (int {0, 1}): Input value to _input_a.
            input_b (int {0, 1}): Input value to _input_b.
        """
        if not self._is_connected_a:
            checkInputValid(input_a)
            self._input_a = input_a

        if not self._is_connected_b:
            checkInputValid(input_b)
            self._input_b = input_b

    def _chooseProperInput(self, connector):
        """Each gate can choose the proper input for the connection.

        For gates with two possible inputs, the connector must be connected
        to only one. If both of them are available, we will choose input_a by
        default. If input_a is already connected, then we will choose input_b.
        It is not possible to connect to a gate with no available input.

        If there is a connection, the connection is accessed and from_gate's
        ouput value is retrieved. This continues until all input is available
        and the final output becomes the required input for the gate in
        question. In a sense, the curcuit works backwards to find the input
        necessary to finally produce output.

        Args:
            self (_BinaryGate): A class instance.
            connector (Connector): A connector where self is the at the end of
                that connector.

        Raises:
            RuntimeError: If no empty input is available.
        """
        if not self._is_connected_a:
            self._is_connected_a = True
            self._input_connector_a = connector
        elif not self._is_connected_b:
            self._is_connected_b = True
            self._input_connector_b = connector
        else:
            raise RuntimeError('No empty input available.')


class _UnaryGate(_LogicGate):
    """Gate with one input.

    Attributes:
        _input (int {0, 1}/Connector): Input of the gate.
        _is_connected (bool): Whether _input is connected to a Connector.
        _input_connector (Connector): Connector to _input, if possible.

    Attributes from Base Classes:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
    """

    def __init__(self, label):
        _LogicGate.__init__(self, label)
        self._input = None
        self._is_connected = False
        self._input_connector = None

    def setInput(self, input_=None):
        """Set the input from user input or a connector.

        If the input is not connected to a Connector, then uses the user's
        input.

        Args:
            self (_UnaryGate): A class instance.
            input_ (int {0, 1}): Input value to _input.
        """
        if not self._is_connected:
            checkInputValid(input_)
            self._input = input_

    def _chooseProperInput(self, connector):
        """Each gate can choose the proper input for the connection.

        For gates with only one input, if the input is available, we will
        choose that input. It is not possible to connect to a gate with no
        available input.

        If there is a connection, the connection is accessed and from_gate's
        ouput value is retrieved. This continues until all input is available
        and the final output becomes the required input for the gate in
        question. In a sense, the curcuit works backwards to find the input
        necessary to finally produce output.

        Args:
            self (_UnaryGate): A unary gate.
            connector (Connector): A connector where self is the at the end of
                that connector.

        Raises:
            RuntimeError: If no empty input is available.
        """
        if not self._is_connected:
            self._is_connected = True
            self._input_connector = connector
        else:
            raise RuntimeError('No empty input available.')


class AndGate(_BinaryGate):
    """And gate with two inputs and one output.

    Attributes from Base Class:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
        _input_a (int {0, 1}): One input of the gate.
        _input_b (int {0, 1}): Another input of the gate.
        _is_connected_a (bool): Whether _input_a is connected to a connector.
        _is_connected_b (bool): Whether _input_b is connected to a connector.
        _input_connector_a (Connector): Connector to _input_a, if possible.
        _input_connector_b (Connector): Connector to _input_b, if possible.

    >>> and_gate = AndGate('add')
    >>> and_gate.setInput(1, 1)
    >>> and_gate.getOutput()
    1
    >>> and_gate.setInput(1, 0)
    >>> and_gate.getOutput()
    0
    >>> and_gate.setInput(0, 1)
    >>> and_gate.getOutput()
    0
    >>> and_gate.setInput(0, 0)
    >>> and_gate.getOutput()
    0
    >>> and_gate.setInput('str', 1)
    Traceback (most recent call last):
    ...
    ValueError: The input must be 0 or 1.
    """

    def __init__(self, label):
        _BinaryGate.__init__(self, label)

    def _forward(self):
        if self._is_connected_a:
            self._input_a = self._input_connector_a._getFrom().getOutput()
        if self._is_connected_b:
            self._input_b = self._input_connector_b._getFrom().getOutput()
        if self._input_a == 1 and self._input_b == 1:
            return 1
        else:
            return 0


class OrGate(_BinaryGate):
    """Or gate with two inputs and one output.

    Attributes from Base Class:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
        _input_a (int {0, 1}): One input of the gate.
        _input_b (int {0, 1}): Another input of the gate.
        _is_connected_a (bool): Whether _input_a is connected to a connector.
        _is_connected_b (bool): Whether _input_b is connected to a connector.
        _input_connector_a (Connector): Connector to _input_a, if possible.
        _input_connector_b (Connector): Connector to _input_b, if possible.

    >>> or_gate = OrGate('or')
    >>> or_gate.setInput(1, 1)
    >>> or_gate.getOutput()
    1
    >>> or_gate.setInput(1, 0)
    >>> or_gate.getOutput()
    1
    >>> or_gate.setInput(0, 1)
    >>> or_gate.getOutput()
    1
    >>> or_gate.setInput(0, 0)
    >>> or_gate.getOutput()
    0
    """

    def __init__(self, label):
        _BinaryGate.__init__(self, label)

    def _forward(self):
        if self._is_connected_a:
            self._input_a = self._input_connector_a._getFrom().getOutput()
        if self._is_connected_b:
            self._input_b = self._input_connector_b._getFrom().getOutput()
        if self._input_a == 1 or self._input_b == 1:
            return 1
        else:
            return 0


class NotGate(_UnaryGate):
    """Not gate with one input and one output.

    Attributes from Base Class:
        _label (str): Name of the gate for identification.
        _output (int {0, 1}): Output of the gate.
        _input (int {0, 1}): One input of the gate.
        _is_connected (bool): Whether _input is connected to a connector.
        _input_connector (Connector): Connector to _input, if possible.

    >>> not_gate = NotGate('not')
    >>> not_gate.setInput(1)
    >>> not_gate.getOutput()
    0
    >>> not_gate.setInput(0)
    >>> not_gate.getOutput()
    1
    """

    def __init__(self, label):
        _UnaryGate.__init__(self, label)

    def _forward(self):
        if self._is_connected:
            self._input = self._input_connector._getFrom().getOutput()
        if self._input == 1:
            return 0
        else:
            return 1


class Connector(object):
    """Class to connect gates together in a circuit.

    Each connector will have two gates, one on either end. The output of
    one flowing into the input of another. It is a HAS-A relationship of
    gate.LogicGate.

    Attributes:
        _from_gate (gate.LogicGate): One gate at the from end.
        _to_gate (gate.LogicGate): One gate at the to end.

    >>> and1 = AndGate('and1')
    >>> and2 = AndGate('and2')
    >>> or1 = OrGate('or1')
    >>> not1 = NotGate('not1')
    >>> c1 = Connector(and1, or1)
    >>> c2 = Connector(and2, or1)
    >>> c3 = Connector(or1, not1)
    >>> and1.setInput(0, 1)
    >>> and2.setInput(1, 1)
    >>> not1.getOutput()
    0
    >>> and1.setInput(1, 1)
    >>> and2.setInput(0, 0)
    >>> not1.getOutput()
    0
    >>> and1.setInput(0, 1)
    >>> and2.setInput(1, 0)
    >>> not1.getOutput()
    1
    """

    def __init__(self, from_gate, to_gate):
        self._from_gate = from_gate
        self._to_gate = to_gate
        self._to_gate._chooseProperInput(self)

    def _getFrom(self):
        return self._from_gate

    def _getTo(self):
        return self._to_gate


def test():
    """Test code for this module.

    Run "python -v gate.py" to see the results.
    """
    import doctest
    doctest.testmod()  # Automatically validate the embedded tests.


if __name__ == '__main__':
    test()
