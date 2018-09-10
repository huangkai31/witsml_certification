# Copyright (c) 2014 Energistics   .
#
import sys
import os
import time
import re
import ConfigParser
from PySide import QtGui, QtCore
import subprocess
from Queue import Queue

from wtl.witsml import *
import wtl.store_prim
import wtl.config

#
# VERSIONS
#

TEST_PLAN_VERSION = '1.0'
CERTIFICATION_TEST_SUITE_VERSION = '1.0'
CERTIFICATION_TESTING_ENGINE_VERSION = '1.0'

#
# CONSTANTS
#

APP_NAME = 'WITSML Product Certification Testing Tool'
APP_VERSION = 'Version 1.0'
APP_INFO = """This product was developed
by TeyTech Inc. for Energistics

Copyright (c) 2014

"""        

TOOL_CONFIGURATION_FILE = '.\\wtl_cfg.py'
DEFAULT_SERVER_FILE = '.\\server\\default_server.py'
SERVER_ACCESS_PROFILES_FILE = '.\\server\\server_access_profiles.ini'
SCRIPTS_DIRECTORY = '.\\scripts'
RESULTS_DIRECTORY = '.\\results'

NEW_SERVER_NAME = '<new>'

def inplace_change(filename, change_list):
    """
    Utility function to update configuration files where values are 
    stored in the form key=value 
    The filename provided is updated based on the tuples of the form
    (key, value) provided in the change list
    A success/fail indication is returned with an error string is applicable 
    """
    try:
        contents = open(filename).read()
    except Exception as inst:
        return (False, str(inst))
    for change in change_list:
        contents, num = re.subn('^' + change[0] + '.*$',
                               change[0] + ' = ' + change[1],
                               contents,
                               count=1,
                               flags = re.MULTILINE) 
        if (num == 0):
            return (False, "Cannot update values")
    
    try:
        f=open(filename, 'w')
        f.write(contents)
        f.flush()
    except Exception as inst:
        return (False, str(inst))
        
    f.close()
   
    return (True, "")
                
class OutLog:
    """ Class to redirect standard output/error to a queue """
    
    def __init__(self, queue):
        self.queue = queue
        
    def write(self, m):
        self.queue.put(m)
  
class MyReceiver(QtCore.QObject):
    """
    An object (to be run in a thread) which sits waiting for data to come through a queue
    and once it has got something from the queue, it sends it to the main thread
    by emitting a signal
    """
    
    mysignal = QtCore.Signal(str)
    finished = QtCore.Signal()

    def __init__(self,queue,*args,**kwargs):
        QtCore.QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @QtCore.Slot()
    def run(self):
        while True:
            m = self.queue.get()
            if (m == 'AbortMyReceiver'):
                break;
            self.mysignal.emit(m)
            
        self.finished.emit()

    def stop(self):
        self.queue.put('AbortMyReceiver')
        
class ExecuteTest(QtCore.QObject):
    """ An object (to be run in a thread) which runs a test script """

    finished = QtCore.Signal()
    
    def __init__(self,*args,**kwargs):
        QtCore.QObject.__init__(self,*args,**kwargs)
        
    def set_test(self, test):    
        self.test = test

    @QtCore.Slot()
    def run(self):
        run(self.test)
        self.finished.emit()
            
class DialogWindow(QtGui.QDialog):
    """ Standard dialog window to give output to the user """
    
    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)
        
        self.setWindowTitle(APP_NAME)
        self.setGeometry(200, 200, 100, 100)
        self.setWindowIcon(QtGui.QIcon('black_cat.png'))        

        self.message = QtGui.QLabel("")
        self.button = QtGui.QPushButton("OK")        
        self.button.clicked.connect(self.close)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addStretch(1)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.message)
        layout.addLayout(hbox)
        self.setLayout(layout)
        
    def display(self, title, message):
        """ Display the window to show and wait for user to press OK """
        
        self.setWindowTitle(title)
        self.message.setText(message)       

        self.exec_()

class FileDisplayWindow(QtGui.QDialog):
    """ Dialog window to show a file's contents """
    
    def __init__(self, parent=None):
        super(FileDisplayWindow, self).__init__(parent)
        
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QtGui.QIcon('clipboard-icon.png'))        
        
        self.message = QtGui.QLabel("")
        self.fileContents = QtGui.QTextEdit(self)
        self.fileContents.setReadOnly(True)
        self.fileContents.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.button = QtGui.QPushButton("OK")        
        self.button.clicked.connect(self.close)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addStretch(1)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.fileContents)
        layout.addLayout(hbox)
        self.setLayout(layout)
        
    def display(self, title, filename):
        """ Display the window with the file contents and wait for user to press OK """

        self.setWindowTitle(title)
        self.message.setText(filename)
        
        try:
            f = open(filename, 'r')
            self.fileContents.setText(f.read())
            f.close()
        except Exception as inst:
            self.fileContents.setText(str(inst))
        
        self.exec_()

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, queue):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 800, 500)        

        self.dialog_window = DialogWindow(self)

        self.statusBar().showMessage('')
        self.menu()
        
        self.widget = MainWidget(self)
        self.setCentralWidget(self.widget)

        # Create thread that will listen on the other end of the queue,
        # and send the text to the output box in our application
        self.thread = QtCore.QThread()
        self.my_receiver = MyReceiver(queue)
        self.my_receiver.mysignal.connect(self.append_text)
        self.my_receiver.moveToThread(self.thread)
        self.thread.started.connect(self.my_receiver.run)
        self.my_receiver.finished.connect(self.thread.quit)
        self.my_receiver.finished.connect(self.my_receiver.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)     
        self.thread.start()

    def menu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')

        saveAction = QtGui.QAction(QtGui.QIcon(), '&Save Server', self,
                                   shortcut='Ctrl+S',
                                   statusTip='Save server access profile',
                                   triggered=self.save)

        saveAsAction = QtGui.QAction(QtGui.QIcon(),
                                     'S&ave Server As...', self,
                                     statusTip='Save server access profile with a different name',
                                     triggered=self.save_as)
        saveAsAction.triggered.connect(self.save_as)

        updateToolConfigurationAction = QtGui.QAction(QtGui.QIcon(),
                                                      '&Update Tool Configuration', self,
                                                      statusTip='Save the new tool configuration',
                                                      triggered=self.update_too_configuration)

        exitAction = QtGui.QAction(QtGui.QIcon(), '&Exit', self,
                                   shortcut='Ctrl+Q',
                                   statusTip='Exit application',
                                   triggered=self.close)
        
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(updateToolConfigurationAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        ResultsMenu = menubar.addMenu('&Results')

        viewAction = QtGui.QAction(QtGui.QIcon('view.png'), '&View', self)
        viewAction.setStatusTip('Browse one of the output files')
        viewAction.triggered.connect(self.show_file)
        ResultsMenu.addAction(viewAction)

        helpMenu = menubar.addMenu('&Help')

        aboutAction = QtGui.QAction(QtGui.QIcon('about.png'), '&About', self)
        aboutAction.setStatusTip('Info about the application')
        aboutAction.triggered.connect(self.about)
        helpMenu.addAction(aboutAction)

    def save(self):
        self.widget.update_and_save_server_access_profile()

    def save_as(self):
        self.widget.update_and_save_as_server_access_profile()

    def update_too_configuration(self):
        self.widget.save_tool_configuration()
        
    def show_file(self):
        self.widget.show_file_contents()
        
    def status(self, message):
        self.statusBar().showMessage(message)
        
    def about(self):
        self.dialog_window.display("About", APP_VERSION + "\n\n" + APP_INFO)

    def closeEvent(self, event):
        
        self.my_receiver.stop()
        self.widget.close()                    
        event.accept()       
    
    @QtCore.Slot(str)
    def append_text(self,m):
        self.widget.outputBox.moveCursor(QtGui.QTextCursor.End)
        self.widget.outputBox.insertPlainText(m)
        
class MainWidget(QtGui.QWidget):
    """ Main widget containing all the window elements of the user interface """

    ###
    ### Initialization functions
    ###

    def __init__(self, mainWindow):      
        super(MainWidget, self).__init__()
        
        self.main_window = mainWindow
        
        self.dialog_window = DialogWindow(self)
        self.file_display_window = FileDisplayWindow(self)

        self.selected_server = None
        self.tool_configuration_changed = False
        self.server_access_configuration_changed = False
        self.default_server = None
        self.data_grower_process_running = False
                
        self.init_UI()
    
        self.iniitialize_server_access_profiles()
        self.load_tool_configuration()
        self.last_selected_test = None
        self.load_tests()
        self.connect_status(False)
        
    def init_UI(self):     
        """ Setup the GUI elements in the window """
        
        # VERSION INFO
        
        test_plan_version = TEST_PLAN_VERSION
        certification_test_suite_version = CERTIFICATION_TEST_SUITE_VERSION
        certification_testing_engine_version = CERTIFICATION_TESTING_ENGINE_VERSION
        
        TestPlanVersionLabel = QtGui.QLabel('Test plan version: ' + 
                                            "<font color='blue'>" +
                                            test_plan_version, self)
        CertificationTestSuiteVersionLabel = QtGui.QLabel('Test suite version: ' +
                                            "<font color='blue'>" +
                                            certification_test_suite_version, self)
        CertificationTestingEngineVersionLabel = QtGui.QLabel('Testing engine version: ' +
                                            "<font color='blue'>" +
                                            certification_testing_engine_version, self)
        
        versionLabel = QtGui.QLabel('<b>Certification Versions</b>', self)

        vboxVersions = QtGui.QVBoxLayout()
        vboxVersions.addWidget(versionLabel)
        vboxVersions.addWidget(TestPlanVersionLabel)
        vboxVersions.addWidget(CertificationTestSuiteVersionLabel)
        vboxVersions.addWidget(CertificationTestingEngineVersionLabel)
        
        # END OF VERSION INFO

        # SERVER ACCESS CONFIGURATION
        
        serverAccessConfigurationLabel = QtGui.QLabel('<b>Server Access Configuration</b>', self)
        
        profileLabel = QtGui.QLabel('Server:')
        
        self.profilesCombo = QtGui.QComboBox(self)
        self.profilesCombo.currentIndexChanged[str].connect(self.select_server_access_profile)

        self.defaultLabel = QtGui.QLabel('')

        DeleteServerButton = QtGui.QPushButton('Delete server', self)
        DeleteServerButton.clicked.connect(self.delete_server_access_profile)
        DeleteServerButton.setToolTip("Delete this server's access profile")
        DeleteServerButton.resize(DeleteServerButton.sizeHint())
        
        hboxServerAsccessProfiles = QtGui.QHBoxLayout()
        hboxServerAsccessProfiles.addWidget(profileLabel)
        hboxServerAsccessProfiles.addWidget(self.profilesCombo)
        hboxServerAsccessProfiles.addWidget(self.defaultLabel)
        hboxServerAsccessProfiles.addStretch(1)
        hboxServerAsccessProfiles.addWidget(DeleteServerButton)
        
        
        url = QtGui.QLabel('Server URL')
        proxy = QtGui.QLabel('proxy')
        username = QtGui.QLabel('user name')
        password = QtGui.QLabel('password')

        self.urlEdit = QtGui.QLineEdit()
        self.urlEdit.textChanged.connect(self.server_access_profiles_changed)
        self.proxyEdit = QtGui.QLineEdit()
        self.proxyEdit.textChanged.connect(self.server_access_profiles_changed)
        self.usernameEdit = QtGui.QLineEdit()
        self.usernameEdit.textChanged.connect(self.server_access_profiles_changed)
        self.passwordEdit = QtGui.QLineEdit()
        self.passwordEdit.textChanged.connect(self.server_access_profiles_changed)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
               
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(url, 1, 0)
        grid.addWidget(self.urlEdit, 1, 1)

        grid.addWidget(proxy, 2, 0)
        grid.addWidget(self.proxyEdit, 2, 1)

        grid.addWidget(username, 3, 0)
        grid.addWidget(self.usernameEdit, 3, 1)

        grid.addWidget(password, 4, 0)
        grid.addWidget(self.passwordEdit, 4, 1)
        
        self.defaultServerCheckBox = QtGui.QCheckBox('Set as default server', self)

        SaveServerAccessButton = QtGui.QPushButton('  Save  ', self)
        SaveServerAccessButton.clicked.connect(self.update_and_save_server_access_profile)
        SaveServerAccessButton.setToolTip('Save the server access configuration with the new values')
        SaveServerAccessButton.resize(SaveServerAccessButton.sizeHint())

        SaveAsServerAccessButton = QtGui.QPushButton('Save As', self)
        SaveAsServerAccessButton.clicked.connect(self.update_and_save_as_server_access_profile)
        SaveAsServerAccessButton.setToolTip('Save the server access configuration with the new values under a new server name')
        SaveAsServerAccessButton.resize(SaveAsServerAccessButton.sizeHint())

        hboxSaveServerAccess = QtGui.QHBoxLayout()
        hboxSaveServerAccess.addWidget(SaveServerAccessButton)
        hboxSaveServerAccess.addWidget(SaveAsServerAccessButton)
        hboxSaveServerAccess.addStretch(1)
        
        # END OF SERVER CONFIGURATION

        # TOOL CONFIGURATION

        toolLabel = QtGui.QLabel('<b>Tool Configuration</b>', self)

        self.logRequestsCheckBox = QtGui.QCheckBox('Log requests', self)
        self.logRequestsCheckBox.stateChanged.connect(self.update_tool_configuration_log_requests)
        self.logResponsesCheckBox = QtGui.QCheckBox('Log responses', self)
        self.logResponsesCheckBox.stateChanged.connect(self.update_tool_configuration_log_responses)
        self.enableSchemaValidationCheckBox = QtGui.QCheckBox('Enable schema validation', self)
        self.enableSchemaValidationCheckBox.stateChanged.connect(self.update_tool_configuration_schema_validation)
        
        UpdateToolButton = QtGui.QPushButton('Update tool configuration', self)
        UpdateToolButton.clicked.connect(self.save_tool_configuration)
        UpdateToolButton.setToolTip('Save the tool configuration with the current values')
        UpdateToolButton.resize(UpdateToolButton.sizeHint())
       
        hboxUpdateToolButton = QtGui.QHBoxLayout()
        hboxUpdateToolButton.addWidget(UpdateToolButton)
        hboxUpdateToolButton.addStretch(1)

        # END OF TOOL CONFIGURATION

        sep0 = QtGui.QFrame(self)
        sep0.setFrameShape(QtGui.QFrame.HLine)
        sep0.setLineWidth(2)

        sep1 = QtGui.QFrame(self)
        sep1.setFrameShape(QtGui.QFrame.HLine)
        sep1.setLineWidth(2)

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addLayout(vboxVersions)
        vbox1.addWidget(sep0)
        vbox1.addWidget(serverAccessConfigurationLabel)
        vbox1.addLayout(hboxServerAsccessProfiles)
        vbox1.addLayout(grid)
        vbox1.addWidget(self.defaultServerCheckBox)
        vbox1.addLayout(hboxSaveServerAccess)
        vbox1.addWidget(sep1)
        vbox1.addWidget(toolLabel)
        vbox1.addWidget(self.logRequestsCheckBox)
        vbox1.addWidget(self.logResponsesCheckBox)
        vbox1.addWidget(self.enableSchemaValidationCheckBox)
        vbox1.addLayout(hboxUpdateToolButton)
        vbox1.addStretch(1)
        
        config_widget = QtGui.QWidget()
        config_widget.setLayout(vbox1)
        config_widget.setFixedWidth(400)

        # STATUS
        
        statusLabel = QtGui.QLabel('<b>Status</b>', self)
        self.ServerNameLabel = QtGui.QLabel('Server: ', self)
        self.SchemaVersionLabel = QtGui.QLabel('Schema version: ', self)
        self.ConnectedLabel = QtGui.QLabel('', self)
        self.growerLabel = QtGui.QLabel("Data grower script: <font color='red'>Not Running", self)
        self.scriptRunningLabel = QtGui.QLabel("Script: <font color='red'>Not Running", self)

        vboxStatus = QtGui.QVBoxLayout()
        vboxStatus.addWidget(statusLabel)
        vboxStatus.addWidget(self.ServerNameLabel)
        vboxStatus.addWidget(self.SchemaVersionLabel)
        vboxStatus.addWidget(self.ConnectedLabel)
        vboxStatus.addWidget(self.growerLabel)
        vboxStatus.addWidget(self.scriptRunningLabel)
        sep2 = QtGui.QFrame(self)
        sep2.setFrameShape(QtGui.QFrame.HLine)
        sep2.setLineWidth(2)

        ######################## END OF INFO AND STATUS

        #
        # TEST CONTROL
        #
        
        serverSetupLabel = QtGui.QLabel('<b>Server Setup</b> (default server)', self)

        self.LoadDataButton = QtGui.QPushButton('Load data model', self)
        self.LoadDataButton.clicked.connect(self.load_data_model)
        self.LoadDataButton.setToolTip('Upload the data from the data model to the default server')
        self.LoadDataButton.resize(self.LoadDataButton.sizeHint())

        self.DataGrowerButton = QtGui.QPushButton('Start data grower script', self)
        self.DataGrowerButton.clicked.connect(self.click_data_grower_script)
        self.DataGrowerButton.setToolTip('Start/Stop the data grower script in the background')
        self.DataGrowerButton.resize(self.DataGrowerButton.sizeHint())

        sep3 = QtGui.QFrame(self)
        sep3.setFrameShape(QtGui.QFrame.HLine)
        sep3.setLineWidth(2)

        testLabel = QtGui.QLabel('<b>Certification Testing</b>', self)

        self.ConnectButton = QtGui.QPushButton('Connect', self)
        self.ConnectButton.clicked.connect(self.connect)
        self.ConnectButton.setToolTip('Establish initial session with the server')
        self.ConnectButton.resize(self.ConnectButton.sizeHint())

        self.testsCombo = QtGui.QComboBox(self)
        self.testsCombo.installEventFilter(self)
        self.testsCombo.activated[str].connect(self.test_selected)

        self.ExecuteTestButton = QtGui.QPushButton('Execute test', self)
        self.ExecuteTestButton.clicked.connect(self.execute_test)
        self.ExecuteTestButton.setToolTip('Run the selected test')
        self.ExecuteTestButton.resize(self.ExecuteTestButton.sizeHint())

        outputLabel = QtGui.QLabel('<b>Output</b>', self)

        resultFilenameLabel = QtGui.QLabel('Test Suite Result Filename:')
        self.resultFilenameEdit = QtGui.QLineEdit()

        hboxResultFilename = QtGui.QHBoxLayout()
        hboxResultFilename.addWidget(resultFilenameLabel)
        hboxResultFilename.addWidget(self.resultFilenameEdit)
        hboxResultFilename.addStretch(1)

        self.outputBox = QtGui.QPlainTextEdit(self)

        hbox0 = QtGui.QHBoxLayout()
        hbox0.addWidget(self.LoadDataButton)
        hbox0.addStretch(1)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.DataGrowerButton)
        hbox1.addStretch(1)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.ConnectButton)
        hbox2.addStretch(1)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.testsCombo)
        hbox3.addWidget(self.ExecuteTestButton)
        hbox3.addStretch(1)
        
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addLayout(vboxStatus)
        vbox2.addWidget(sep2)
        vbox2.addWidget(serverSetupLabel)       
        vbox2.addLayout(hbox0)
        vbox2.addLayout(hbox1)
        vbox2.addWidget(sep3)
        vbox2.addWidget(testLabel)
        vbox2.addLayout(hbox2)
        vbox2.addLayout(hbox3)
        vbox2.addWidget(outputLabel)
        vbox2.addLayout(hboxResultFilename)
        vbox2.addWidget(self.outputBox)

        sep3 = QtGui.QFrame(self)
        sep3.setFrameShape(QtGui.QFrame.VLine)
        sep3.setLineWidth(2)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(config_widget)
        hbox3.addWidget(sep3)
        hbox3.addLayout(vbox2)

        self.setLayout(hbox3)

        ######################## END OF TEST CONTROL
       
    ###
    ### General reporting functions
    ###

    def status(self, message):
        """ Display a message in the window's status bar """
        
        self.main_window.status(message)
        
    def report_error(self, message):
        """ Show a dialog window to report an error message """
        
        self.dialog_window.display("Error", message)

    ###
    ### Event handling functions
    ###

    def eventFilter(self, target, event):
        """ Capture a click on the testsCombo to reload the test list """
        if ((target == self.testsCombo) and (event.type() == QtCore.QEvent.MouseButtonPress)):
            self.load_tests()

        return False

    ###
    ### Miscellaneous utility functions
    ###

    
    def update_server_variables(self):
        exec('sys.modules["%s"].%s="%s"' % (wtl.config.server_file_name,
                                         'server_name', self.profilesCombo.currentText()))
        exec('sys.modules["%s"].%s="%s"' % (wtl.config.server_file_name,
                                         'server_URL', self.urlEdit.text()))
        exec('sys.modules["%s"].%s="%s"' % (wtl.config.server_file_name,
                                         'server_username', self.usernameEdit.text()))
        exec('sys.modules["%s"].%s="%s"' % (wtl.config.server_file_name,
                                         'server_password', self.passwordEdit.text()))
        exec('sys.modules["%s"].%s="%s"' % (wtl.config.server_file_name,
                                         'server_proxy_URL', self.proxyEdit.text()))
        
    def show_file_contents(self):
        """ Display the file contents in a dailog window """
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file', RESULTS_DIRECTORY)
        if (filename):
            self.file_display_window.display('WITSML Certification Results', filename)
                     
    
    ###
    ### Server access configuration functions
    ###
    
    def load_server_access_profiles(self):
        """
        Load the list of servers and their access parameters from the default
        server access profiles file
        """
        
        self.server_profiles = ConfigParser.SafeConfigParser({'server_url': '',
                                                              'server_proxy_url': '',
                                                              'server_username': '',
                                                              'server_password': ''})
        try:
            file_read = self.server_profiles.read(SERVER_ACCESS_PROFILES_FILE)
            if (not file_read):
                self.report_error("Server access configuration file could not be read")
                return False
        except:
            self.report_error("Server access configuration file could not be read")
            return False
        
        self.server_access_configuration_changed = False
        return True                                                                        

    def iniitialize_server_access_profiles(self):
        """ 
        Initialize the Server Access Profile information based on the stored profiles
        in server_access_profiles.ini and in and the default_server.py file
        """ 
        
        self.profilesCombo.clear()
        self.profilesCombo.addItem(NEW_SERVER_NAME)
        self.load_server_access_profiles()
        for profile in self.server_profiles.sections():
            self.profilesCombo.addItem(profile)
        self.default_server = get('server_name')        
        if (self.default_server in [self.profilesCombo.itemText(i) for i in range(self.profilesCombo.count())]):
            # make sure the access profile matches the default profile
            if ((self.server_profiles.get(self.default_server, 'server_url') != get('server_URL')) or
                (self.server_profiles.get(self.default_server, 'server_proxy_url') != get('server_proxy_URL')) or
                (self.server_profiles.get(self.default_server, 'server_username') != get('server_username')) or
                (self.server_profiles.get(self.default_server, 'server_password') != get('server_password'))):
                self.update_server_access_profile(self.default_server,
                                                  get('server_URL'),
                                                  get('server_proxy_URL'),
                                                  get('server_username'),
                                                  get('server_password'))
                self.server_access_configuration_changed = True
                self.status("Default access configuration profile for '" + self.default_server + "' updated")
        else:
            # Add default server to server profiles
            index = self.add_server_access_profile(self.default_server,
                                              get('server_URL'),
                                              get('server_proxy_URL'),
                                              get('server_username'),
                                              get('server_password'))
            if (index is None):
                self.report_error("Cannot create server access profile for default server access parameters")
            else:
                self.status("Default access configuration profile for '" + self.default_server + "' created")
        temp_changed = self.server_access_configuration_changed
        self.urlEdit.setText(get('server_URL'))
        self.proxyEdit.setText(get('server_proxy_URL'))
        self.usernameEdit.setText(get('server_username'))
        self.passwordEdit.setText(get('server_password'))
        self.server_access_configuration_changed = temp_changed
        self.profilesCombo.setCurrentIndex(self.profilesCombo.findText(self.default_server))

    def save_server_access_profiles(self):                      
        """
        Save the list of servers and their access parameters back to the
        default server access profiles file
        """

        with open('.\\server\server_access_profiles.ini', 'wb') as configfile:
            try:
                self.server_profiles.write(configfile)
            except error:
                self.report_error("Server access configuration file could not be updated" + error)
                return False
        
        self.server_access_configuration_changed = False
        self.status("Server access configuration file updated successfully")
        return True            

    def server_access_profiles_changed(self, text):                      
        """ Indicate that one of the server access parameters changed """

        self.server_access_configuration_changed = True

    def select_server_access_profile(self, server_name):
        """
        Set the access parameters to the server access profile of the given
        server
        """
        
        # Save change status until we load the new server info
        temp_changed = self.server_access_configuration_changed
        
        # Update current server info
        if ((self.selected_server is not None) and (self.selected_server != NEW_SERVER_NAME)):
            self.update_server_access_profile(self.selected_server,
                                              self.urlEdit.text(),
                                              self.proxyEdit.text(),
                                              self.usernameEdit.text(),
                                              self.passwordEdit.text())
        
        if (server_name == NEW_SERVER_NAME):
            self.urlEdit.setText("")
            self.proxyEdit.setText("")
            self.usernameEdit.setText("")
            self.passwordEdit.setText("")
        else:
            self.urlEdit.setText(self.server_profiles.get(server_name, 'server_url'))
            self.proxyEdit.setText(self.server_profiles.get(server_name, 'server_proxy_url'))
            self.usernameEdit.setText(self.server_profiles.get(server_name, 'server_username'))
            self.passwordEdit.setText(self.server_profiles.get(server_name, 'server_password'))

        self.server_access_configuration_changed = temp_changed
        
        self.selected_server = server_name
        if (server_name == self.default_server):
            # this is the default server
            self.defaultLabel.setText("<font color='blue'>DEFAULT")
        else:
            self.defaultLabel.setText("")
            
    def delete_server_access_profile(self):
        """
        Delete the server access profile of the currently selected server
        and update the default server access profiles file
        """
        
        server_name = self.profilesCombo.currentText()
        index = self.profilesCombo.currentIndex()
        if (server_name != NEW_SERVER_NAME):
            self.profilesCombo.setCurrentIndex(0)
            self.server_profiles.remove_section(server_name)
            self.profilesCombo.removeItem(index)
            self.server_access_configuration_changed = True
            self.status("Server access configuration for '" + server_name + "' deleted")
            self.save_server_access_profiles()
        else:           
             self.report_error("Delete failed - No server selected")
           
    def update_server_access_profile(self, server_name, url, proxy, username, password):
        """
        Update the server access parameters for the given server
        """
        self.server_profiles.set(server_name, 'server_url', url)
        self.server_profiles.set(server_name, 'server_proxy_url', proxy)
        self.server_profiles.set(server_name, 'server_username', username)
        self.server_profiles.set(server_name, 'server_password', password)

    def add_server_access_profile(self, new_server_name, url, proxy, username, password):
        """
        Add the server access parameters to a new server access profile with
        the given server name.
        Return the index into the server combo list or None if not able to add
        """
        try:
            self.server_profiles.add_section(new_server_name)
        except:
            return None

        self.update_server_access_profile(new_server_name, url, proxy,
                                          username, password)
        self.profilesCombo.addItem(new_server_name)
        self.server_access_configuration_changed = True
        return self.profilesCombo.count() - 1

    def set_current_server_as_default(self):
        """ Make the current server the default server """
        
        new_default_server = self.profilesCombo.currentText()
        success, error = inplace_change(DEFAULT_SERVER_FILE, [
                                            ('server_name', "'" + new_default_server + "'"),
                                            ('server_URL', "'" + self.urlEdit.text() + "'"),
                                            ('server_proxy_URL', "'" + self.proxyEdit.text() + "'"),
                                            ('server_username', "'" + self.usernameEdit.text() + "'"),
                                            ('server_password', "'" + self.passwordEdit.text() + "'")
                                            ])
        
        if (success):
            self.default_server = new_default_server
            self.dialog_window.display("Server Configuration",
                                   "Server '" + self.default_server + "' is now the default server")
            self.defaultLabel.setText("<font color='blue'>DEFAULT")
        else:
            self.report_error("Server configuration failed - " + error)
        
        
    def update_and_save_server_access_profile(self):
        """
        Update the server access parameters with the new ones provided
        and update the default server access profiles file
        If the defaultServerCheckBox is checked, make this server access
        profile the default profile
        """
        
        if (self.profilesCombo.currentText() == NEW_SERVER_NAME):
            self.update_and_save_as_server_access_profile()
            return
        server_name = self.profilesCombo.currentText()
        self.server_profiles.set(server_name, 'server_url', self.urlEdit.text())
        self.server_profiles.set(server_name, 'server_proxy_url', self.proxyEdit.text())
        self.server_profiles.set(server_name, 'server_username', self.usernameEdit.text())
        self.server_profiles.set(server_name, 'server_password', self.passwordEdit.text())
        self.server_access_configuration_changed = True
        self.status("Server access configuration for '" + server_name + "' updated")

        self.save_server_access_profiles()

        if (self.defaultServerCheckBox.isChecked()):
            self.set_current_server_as_default()

    def update_and_save_as_server_access_profile(self):
        """
        Update the server access parameters with the new ones provided
        under a new server name and update the default server access profiles file
        If the defaultServerCheckBox is checked, make this server access
        profile the default profile
        """
        
        new_server_name, ok = QtGui.QInputDialog.getText(self,
                                                         'Save As',
                                                         'Server:')
        if (new_server_name == ""):
            self.report_error("Update failed - No server name provided")
            return
        index = self.add_server_access_profile(new_server_name,
                                               self.urlEdit.text(),
                                               self.proxyEdit.text(),
                                               self.usernameEdit.text(),
                                               self.passwordEdit.text())    
        if (index is None):
            self.report_error("Update failed - Server name already exists")
            return           
        self.profilesCombo.setCurrentIndex(index)
        self.status("Server access configuration profile for '" + new_server_name + "' created")

        self.save_server_access_profiles()

        if (self.defaultServerCheckBox.isChecked()):
            self.set_current_server_as_default()

    ###
    ### Tool configuration functions
    ###
    
    def load_tool_configuration(self):
        """ Get the current WITSML certification tool configuration """ 
        
        self.logRequestsCheckBox.setCheckState(QtCore.Qt.Checked if wtl.config.log_requests else QtCore.Qt.Unchecked)
        self.logResponsesCheckBox.setCheckState(QtCore.Qt.Checked if wtl.config.log_responses else QtCore.Qt.Unchecked)
        self.enableSchemaValidationCheckBox.setCheckState(QtCore.Qt.Checked if wtl.config.enable_schema_validation else QtCore.Qt.Unchecked)
        self.tool_configuration_changed = False

    def update_tool_configuration_log_requests(self, state):
        """ Update the current WITSML certification tool configuration """ 
        
        self.tool_configuration_changed = True
        wtl.config.log_requests = True if self.logRequestsCheckBox.isChecked() else False
    
    def update_tool_configuration_log_responses(self, state):
        """ Update the current WITSML certification tool configuration """ 
        
        self.tool_configuration_changed = True
        wtl.config.log_responses = True if self.logResponsesCheckBox.isChecked()  else False

    def update_tool_configuration_schema_validation(self, state):
        """ Update the current WITSML certification tool configuration """ 
        
        self.tool_configuration_changed = True
        wtl.config.enable_schema_validation = True if self.enableSchemaValidationCheckBox.isChecked() else False        

    def save_tool_configuration(self):
        """ Save the current WITSML certification tool configuration """ 

        success, error = inplace_change(TOOL_CONFIGURATION_FILE, [
                                                                 ('log_requests', str(self.logRequestsCheckBox.isChecked())),
                                                                 ('log_responses', str(self.logResponsesCheckBox.isChecked())),
                                                                 ('enable_schema_validation', str(self.enableSchemaValidationCheckBox.isChecked()))
                                                                 ])
        if (success):
            self.tool_configuration_changed = False
            self.status("Tool configuration file updated successfully")
        else:
            self.report_error("Tool configuration failed - " + error)
            
    ###
    ### Test execution function
    ###

    def convert_test_number(self, test_name):
        """ 
        Get a converted test number for sorting
        Assumes test name is of the form 'test<number>[abcdef]'
        Use the base number plus any additional letter (i.e. a,b,c...) to generate
        a test number
        """
        
        number = 1000000
        digits = ''
        if test_name[0:4] == 'test':
            for s in test_name[4:]:
                if s.isdigit():
                    digits += s
                elif (digits != ''):
                    number = int(digits) * 1000 + ord(s)
                    break
        
        return number
                

    def load_tests(self):
        """ Get the list of tests from the scripts directory """
        
        self.testsCombo.clear()
        test_files = os.listdir(SCRIPTS_DIRECTORY)
        test_files.sort(key=self.convert_test_number)
        for test in test_files:
            self.testsCombo.addItem(test.replace(".py", ""))
        
        # Restore last selected test
        if (self.last_selected_test is not None):
            index = self.testsCombo.findText(self.last_selected_test)
            if (index == -1):
                self.last_selected_test = None
            else:
                self.testsCombo.setCurrentIndex(index)
    
    def connect(self):
        """
        Establish initial contact with the server using the access parameters
        in the Server Access Configuration Area
        """
        
        self.ExecuteTestButton.setEnabled(False)
        self.update_server_variables()
        self.status('Starting session with server ' + get('server_name') + '...')
        if (wtl.store_prim.WITSMLServer.start_server_session()):
            self.connect_status(True)
            self.status('Session established successfully')
        else:
            self.report_error("Connection with server failed - Cannot get schema versions supported")
            self.connect_status(False)
            self.status('Session establishment failed')
                    
    def connect_status(self, connected):
        """ Update the server session connect status information """
        
        if connected:
            self.ConnectedLabel.setText("Session: <font color='green'>Established")
            self.ServerNameLabel.setText('Server: ' + get('server_name') + ' (' + get('server_URL') + ')')
            self.SchemaVersionLabel.setText('Schema version: ' + get('server_schema_version'))
        else:
            self.ConnectedLabel.setText("Session: <font color='red'>Not Established")           
            self.ServerNameLabel.setText('Server: ')
            self.SchemaVersionLabel.setText('Schema version: ')
        
        self.ExecuteTestButton.setEnabled(connected)
            
    def load_data_model(self):
        """
        Execute the script that loads the data model to the server
        This runs a separate executable that loads the data to the 
        default server (i.e. that server access information stored in the
        server file)
        """
         
        self.status('Loading data set...')
        os.system('load_data_set.exe -a')
        self.status('Data set load ended')
        
    def click_data_grower_script(self):
        """ Execute the data grower script """
        
        if (self.data_grower_process_running):
            if (self.data_grower_process.poll() is None):
                self.data_grower_process.kill()
                self.status('Data grower script terminated')
            else:
                self.status('Data grower script already terminated')
            self.data_grower_process_running = False
            self.DataGrowerButton.setText('Start data grower script')
            self.growerLabel.setText("Data grower script: <font color='red'>Not Running")
        else:
            self.data_grower_process = subprocess.Popen("data_grower_script.exe -a")
            self.status('Data grower script started')
            self.data_grower_process_running = True
            self.DataGrowerButton.setText('Stop data grower script')
            self.growerLabel.setText("Data grower script: <font color='green'>Running...")
        
    def test_selected(self):
        """ Save test selection """
        
        self.last_selected_test = self.testsCombo.currentText()
        
    @QtCore.Slot()
    def execute_test(self):
        """ Run the test selected """
        
        filename = self.resultFilenameEdit.text()
        if (filename != ""):
            wtl.config.result_filename = filename   
        test = self.testsCombo.currentText()  
        
        self.scriptRunningLabel.setText("Script: <font color='green'>Running...")
        self.status("Running test '" + test + "'...")
        self.ConnectButton.setEnabled(False)
        self.ExecuteTestButton.setEnabled(False)

        self.thread = QtCore.QThread()
        self.execute_test_object = ExecuteTest()
        self.execute_test_object.set_test(test)
        self.execute_test_object.moveToThread(self.thread)
        self.thread.started.connect(self.execute_test_object.run)
        self.execute_test_object.finished.connect(self.thread.quit)
        self.execute_test_object.finished.connect(self.execute_test_object.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.test_completed)
        self.thread.start()

    def test_completed(self):
        self.scriptRunningLabel.setText("Script: <font color='red'>Not Running")
        self.status('Test completed')
        self.ConnectButton.setEnabled(True)
        self.ExecuteTestButton.setEnabled(True)
               
    ###
    ### Termination function
    ###

    def close(self):
        """ End the application """
        
        # If the tool configuration was changed, ask if it should be saved
        if (self.tool_configuration_changed):
            reply = QtGui.QMessageBox.question(self, APP_NAME,
                                               "Do you want to save the changes to the Tool Configuration?", QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.save_tool_configuration()

        # If the server access configuration was changed, ask if it should be saved
        if (self.server_access_configuration_changed):
            reply = QtGui.QMessageBox.question(self, APP_NAME,
                                               "Do you want to save the changes to the Server Access Configuration?", QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.save_server_access_profiles()

        # Terminate the grower is running
        if (self.data_grower_process_running):
            self.data_grower_process.terminate()
            
def main():
    
    # Create a queue and redirect the standard output and standard error to 
    # an object that will send it to that queue
    queue = Queue()
    sys.stdout = OutLog(queue)
    sys.stderr = OutLog(queue)

    app = QtGui.QApplication(sys.argv)
    mw = MainWindow(queue)
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

