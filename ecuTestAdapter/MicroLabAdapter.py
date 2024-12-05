"""
This module contains an example of an user-defined Tooladapter. The source code of this example
can be found in the ecu.test installation directory under
``Templates/DefaultData/Utilities``.

A user-defined Tooladapter must be put in the Utilities directory of the current workspace. If a
Tooladapter is changed, it is necessary to stop the current test bench (if it uses the
Tooladapter) and select *Extras -> Update user libraries* in ecu.test.

A Tooladapter's module must contain the class implementing the Tooladapter's functionality. For
autodiscovery and autoimport of ecu.test the module must contain two special variables and two
special methods.
The required variables are:

 - TOOLNAME: The name used in the test bench configuration for this Tooladapter
 - TOOLCAPS: Must be set to Toolcaps.GetNull()

The required methods are:

 - :meth:`IsInstalled`: Check if the interfaced tool is installed on the computer
 - :meth:`CreateToolAdapter`: Method to create an instance of the Tooladapter

The Tooladapter's functionality can be implemented as ToolJobs and ToolProperties. Ports cannot
be implemented in user-defined Tooladapters.

:var TOOLNAME: The name used in the test bench configuration for this Tooladapter - REQUIRED
:vartype TOOLNAME: str
:var TOOLCAPS: Must be set to Toolcaps.GetNull() - REQUIRED
"""

###############################################################################
##
# Imports needed for every Tooladapter
from tts.core.toolingFramework.interface.Descriptors import ToolDescriptor, PropertyDescriptor, JobDescriptor
from tts.core.toolingFramework.interface.Properties import PropertyTypeId
from tts.core.toolingFramework.interface.Capabilities import Toolcaps
##
from tts.core.toolingFramework.interface.AbstractAdapter import ToolAdapter
from tts.core.toolingFramework.interface.Exceptions import ToollibError
from tts.core.toolingFramework.interface.Proxy import ToolAdapterProxy
##
###############################################################################

## Imports
import socket
import os
import subprocess


TOOLNAME = "MicroLab"
TOOLCAPS = Toolcaps.GetNull() 


#Checks if the Relais Control Programm is installed on the PC
def IsInstalled():
    """
    Checks whether the tool handled by this Tooladapter is installed on the
    computer running this ECU-TEST instance. If this Tooladapter does not use
    any external tool, it is save just to return True.

    :return: True if tool is installed
    :rtype: bool
    """
    toolPath = r''#Change here file path to installation folder 'C:\Files\Prog.exe'
    if os.path.isfile(toolPath):
        print("MicroLab is installed")
        return True

def CreateToolAdapter(host, port):                                       
    '''
    Creates and returns an instance of the Tooladapter of this module.

    As these simple Tooladapters cannot be run remotely by the tool server,
    the host and port arguments must be ignored.

    :return: a ToolAdapterProxy of a ToolAdapter (e.g. :class:`ExampleAdapter`)
    :rtype: ToolAdapterProxy
    '''
    return ToolAdapterProxy(MicroLabAdapter())

HOST = '127.0.0.1'
PORT = 5005

udp_socket_Rx = 0

def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))  # Connect to the server
            print(f"Connected to server at {HOST}:{PORT}")
            s.sendall(command.encode('utf-8'))  # Send the command
            print(f"Sent: {command}")
    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")

def receive():
    try:
        data, addr = udp_socket_Rx.recvfrom(1024) # max size 1024
        return data.decode()
    except Exception as e:
        print(f"Error: {e}")
        return None

class MicroLabAdapter(ToolAdapter):
    '''
    Sample implementation of a Tooladapter.

    The ToolDescriptor of the Tooladapter is created on initialization of the
    Tooladapter. It must match the Tooladapter:

     - Toolname argument must be set to TOOLNAME
     - For each JobDescriptor there must be a method with the name Job<jobname>() and a matching signature.

    :ivar _toolDesc: Descriptor of the Tooladapter
    :vartype _toolDesc: :class:`~tts.core.toolingFramework.interface.Descriptors.ToolDescriptor`

    '''

    def __init__(self):
            self.toolPath = r''#Change here file path to installation folder 'C:\Files\Prog.exe'
            self.cwd = r''#Change here file path to installation folder 'C:\Files'
            self.process = 'process'
            ToolAdapter.__init__(self)
            self._toolDesc = ToolDescriptor(
                TOOLNAME,
                [],  # must be an empty list
                0,
                # List of PropertyDescriptors:
                [

                ],
                # List of ToolJobs:
                [
                    JobDescriptor("Switch_A", [],
                                "Switch A",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_B", [],
                                "Switch B",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_C", [],
                                "Switch C",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_D", [],
                                "Switch D",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),

                    JobDescriptor("Switch_E", [],
                                "Switch E",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_F", [],
                                "Switch F",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_G", [],
                                "Switch G",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                    JobDescriptor("Switch_H", [],
                                "Switch H",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.bytestream),
                                ),
                ]
            )

    # create 8 jobs for handling ON/OFF
    def JobSwitch_A(self):
        send_command("JobA")
        return bool(receive())

    def JobSwitch_B(self):
        send_command("JobB")
        return bool(receive())

    def JobSwitch_C(self):
        send_command("JobC")
        return bool(receive())

    def JobSwitch_D(self):
        send_command("JobD")
        return bool(receive())

    def JobSwitch_E(self):
        send_command("JobE")
        return bool(receive())

    def JobSwitch_F(self):
        send_command("JobF")
        return bool(receive())

    def JobSwitch_G(self):
        send_command("JobG")
        return bool(receive())

    def JobSwitch_H(self):
        send_command("JobH")
        return bool(receive())

    def OnConfigure(self): # Given in Example Code 
            """
            This method is called on tool start (test bench start, manual start in
            configuration window). It can be used to start any external tool needed by this
            ToolAdapter. Raise a ToollibError to signal an error. If OnConfigure fails,
            OnUnconfigure will not be called. Use "pass" if no external tool is used.
            
            udp_connect() (opening the sockets) must be placed here to be able to reconnect on tool restart
            """
            self.process = subprocess.Popen(self.toolPath, cwd=self.cwd)
            #udp_connect()

    def OnUnconfigure(self):
            """
            This method is called on tool shutdown, if the previous call to OnConfigure
            did not fail. It can be used to stop any tool needed by this ToolAdapter.
            Raise a ToollibError to signal an error. Use "pass" if no external tool is used.
            """
            
            subprocess.call(['taskkill', '/F', '/T', '/PID',  str(self.process.pid)])

    def IsBroken(self): # Given in Example Code 
            """
            This method is called before test execution and on configuration window update.
            Return True if any of the external tools used by this ToolAdapter cannot be used anymore
            (e.g connection lost, tool locked up). Otherwise or if no tool is used, return
            False.

            :return: True if tool is broken (not usable)
            :rtype: bool
            """
            return False

    def GetVersion(self): # Given in Example Code 
            """
            You can return the version of the tool you are connecting via this tool adapter
            as a string. The version will be documented in the test report.

            :return: version
            :rtype: Optional<str>
            """
            return None
