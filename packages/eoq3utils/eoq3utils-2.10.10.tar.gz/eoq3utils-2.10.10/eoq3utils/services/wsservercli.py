"""
This is a management script to configure and start an EOQ3 web socket server
composed of the following services:
 - domain,
 - MPL,
 - action manager and
 - action handler

See EOQ User Manual for more information: https://gitlab.com/eoq/doc

2025 Bjoern Annighoefer
"""
from .. import __version__ as version
# other services imports
from .wsdomaincli import WsDomainCli
from .wsmplcli import WsMplCli
from .wsactionmanagercli import WsActionManagerCli
from .wsactionhandlercli import WsActionHandlerCli
# eoq cli commons
from ..cli.common import PrintCliHeader, GetCliPredefinedArguments, PrintCliArgument, CliArgument, ExitHard
from .common import ServiceMenuLoop, ShallRun, ConfigFileOpenFunc, SERVICE_READY_MESSAGE
# subprocess management imports
from threading import Thread, Semaphore
from queue import Empty
from multiprocessing import Process, Queue
from collections import deque
# external imports
import time
import configargparse #like argparse but allows for config files in addition to command line parameters
import traceback
import os
import sys
#type checking 
from typing import List, Dict, Any, Callable

MODULE_NAME = "eoq3utils.services.wsservercli"

class OutputRedirector:
    def __init__(self, stream, outQueue:Queue, ):
        self.stream = stream
        self.outQueue = outQueue
        #internals
        self.legacyWriteFcn = None

    def Redirect(self):
        self.legacyWriteFcn = self.stream.write
        self.stream.write = self.write

    def Restore(self):
        self.stream.write = self.legacyWriteFcn
     
    # with handlers   
    def __enter__(self):
        self.Redirect()
        
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.Restore()
         
    # overwrite stream functions        
    def write(self,data,*args):
            try:
                if(isinstance(data, str) and 0<len(data)):
                    self.outQueue.put(data)
            except Exception as e:
                sys.stderr.write(str(e))
                
                
class InputRedirector:
    def __init__(self, stream, inQueue:Queue, ):
        self.stream = stream
        self.inQueue = inQueue
        #internal 
        self.inputBuffer = deque()
        self.inputSignal = Semaphore(0)
        self.legacyReadFcn = None
        self.active = False
        self.inputThread = None #is created on redirect

    def Redirect(self):
        self.legacyReadFcn = self.stream.read
        self.stream.readline = self.read
        self.active = True
        self.inputThread = Thread(target=self.__InputThread)
        self.inputThread.daemon = True
        self.inputThread.start()

    def Restore(self):
        self.active = False
        self.inputThread.join()
        self.stream.readline = self.legacyReadFcn
        
    #
    def __InputThread(self):
        while (self.active):
            try:
                data = self.inQueue.get(timeout=1)
                self.inputBuffer.appendleft(data)
                self.inputSignal.release()
                #print("input received: "+data)
            except Empty:
                pass #do nothing, just retry reading
     
    # with handlers   
    def __enter__(self):
        self.Redirect()
        
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.Restore()
         
    # overwrite stream functions        
    def read(self, *args):
        #print("read() called!")
        self.inputSignal.acquire()
        data = self.inputBuffer.pop()
        #print("read() returns "+ data)
        return data
            
            
def ChildProcess(target:Callable[[List[Any]],int],args:List[Any], stdoutQueue:Queue, stderrQueue:Queue, stdinQueue:Queue):
    stdoutRedirector = OutputRedirector(sys.stdout,stdoutQueue)
    stdoutRedirector.Redirect()
    stderrRedirector = OutputRedirector(sys.stderr,stderrQueue)
    stderrRedirector.Redirect()
    stdinRedirector = InputRedirector(sys.stdin,stdinQueue)
    stdinRedirector.Redirect()
    target(args)
    stdinRedirector.Restore()
    stdoutRedirector.Restore()
    stderrRedirector.Restore()

class LinePrefixPrinter:
    '''Prints output of with a prefix at the beginning of newlines
    '''
    def __init__(self,prefix:str,stream=sys.stdout):
        self.prefix = prefix
        self.stream = stream
        self.startLine = True
    def Print(self,text):
        if self.startLine:
            print(self.prefix, end='', file=self.stream)
            self.startLine = False
        lineWisePrefixedText = ('\n'+self.prefix).join(text.split('\n'))
        print(lineWisePrefixedText, end='', file=self.stream)
        if text[-1] == '/n':
            self.startLine = True

class SubprocessMonitor:
    def __init__(self, readyString:str, quitStr:str="q\n", forwardStdout:bool=True, forwardStderr:bool=True, stdoutPrefix:str="OUT >> ", stderrPrefix:str="ERR >> ", stdoutCallback=None, stderrCallback=None, readyCallback=None, quitCallback=None):
        self.readyString = readyString
        self.quitStr = quitStr
        self.forwardStdout = forwardStdout
        self.forwardStderr = forwardStderr
        self.stdoutPrefix = stdoutPrefix
        self.stderrPrefix = stderrPrefix
        self.stdoutCallback = stdoutCallback
        self.stderrCallback = stderrCallback
        self.readyCallback = readyCallback
        self.quitCallback = quitCallback
        #internals
        self.proc = None #the process handle
        self.isReady = False #indicated if the process has started successfully
        self.isRunning = True #indicates if the process is still running
        self.stdoutQueue = Queue()
        self.stderrQueue = Queue()
        self.stdinQueue = Queue()
        self.stdoutPrinter = LinePrefixPrinter(self.stdoutPrefix,sys.stdout)
        self.stderrPrinter = LinePrefixPrinter(self.stderrPrefix,sys.stderr)
        #start observing threads (we need three threads, since pipe reads are blocking
        self.stdoutMonitor = Thread(target=self.__StdoutMonitor)
        self.stdoutMonitor.daemon = True #quit with father
        self.stderrMonitor = Thread(target=self.__StderrMonitor)
        self.stderrMonitor.daemon = True #quit with father
        self.runMonitor = Thread(target=self.__RunMonitor)
        self.runMonitor.daemon = True #quit with father

    def Start(self,target:Callable[[List[Any]],int],args:List[Any]):
        self.proc = Process(target=ChildProcess,args=(target,args,self.stdoutQueue,self.stderrQueue,self.stdinQueue))
        self.proc.start()
        self.stdoutMonitor.start()
        self.stderrMonitor.start()
        self.runMonitor.start()
        
    def __StdoutMonitor(self):
        while self.isRunning:
            try: 
                data = self.stdoutQueue.get(timeout=1)
                if(self.forwardStdout):
                    self.stdoutPrinter.Print(data)
                if(self.stdoutCallback):
                    try:
                        self.stdoutCallback(data)
                    except Exception as e: #prevent that callback errors terminate the thread
                        print("STDOUT CALLBACK ERROR: %s"%(str(e))) 
                if(not self.isReady and self.readyString in data):
                    self.isReady = True
                    if(self.readyCallback):
                        try:
                            self.readyCallback()
                        except Exception as e: #prevent that callback errors terminate the thread
                            print("READY CALLBACK ERROR: %s"%(str(e))) 
            except Empty:
                pass #do nothing, just retry reading

    def __StderrMonitor(self):
        while self.isRunning:
            try: 
                data = self.stderrQueue.get(timeout=1)
                if(self.forwardStderr):
                    self.stderrPrinter.Print(data)
                if(self.stderrCallback):
                    try:
                        self.stderrCallback(data)
                    except Exception as e: #prevent that callback errors terminate the thread
                        print("STDERR CALLBACK ERROR: %s"%(str(e)))
            except Empty:
                pass #do nothing, just retry reading

    def __RunMonitor(self):
        while self.proc.is_alive():
            time.sleep(1)#wait until the process has quit
        self.isRunning = False
        if(self.quitCallback):
            try:
                self.quitCallback()
            except Exception as e: #prevent that callback errors terminate the thread
                print("QUIT CALLBACK ERROR: %s"%(str(e)))
                
    def WriteToProcess(self,text:str)->None:
        self.stdinQueue.put(text)
        
    def Quit(self):
        if(self.isRunning):
            if(self.isReady):
                self.WriteToProcess(self.quitStr) #graceful shutdown
            else: 
                self.proc.kill()
        self.proc.join(timeout=5)
    

'''
MAIN: Execution starts here
'''            
def WsServerCli(argv:List[Any]):
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'config',
        'configout',
    ])
    # add custom arguments
    argDefs['enableDomain']        = CliArgument('enableDomain',        'Enable Domain'        , typ=int, default=1,                       description='Start a web socket domain (0=no, 1=yes)')
    argDefs['domainConfig']        = CliArgument('domainConfig',        'Domain Config'        , typ=str, default='./wsdomain.ini',        description='Config file for the domain')
    argDefs['enableMpl']           = CliArgument('enableMpl',           'Enable MPL'           , typ=int, default=1,                       description='Start a web socket model persistence layer (MPL) (0=no, 1=yes)')
    argDefs['mplConfig']           = CliArgument('mplConfig',           'MPL Config'           , typ=str, default='./wsmpl.ini',           description='Config file for the MPL')
    argDefs['enableActionManager'] = CliArgument('enableActionManager', 'Enable Action Manager', typ=int, default=0,                       description='Start a web socket action manager (0=no, 1=yes)')
    argDefs['actionManagerConfig'] = CliArgument('actionManagerConfig', 'Action Manager Config', typ=str, default='./wsactionmanager.ini', description='Config file for the action manager')
    argDefs['enableActionHandler'] = CliArgument('enableActionHandler', 'Enable Action Handler', typ=int, default=0,                       description='Start a web socket action handler (0=no, 1=yes)')
    argDefs['actionHandlerConfig'] = CliArgument('actionHandlerConfig', 'Action Handler Config', typ=str, default='./wsactionhandler.ini', description='Config file for the action handler')
    # use configargparse to parse the command line arguments
    parser = configargparse.ArgParser(description='Eoq3 web socket server. This can be used to start and stop the services web socket domain, a web socket MPL, an action manager and an action handler.',default_config_files=[argDefs['config'].default] if argDefs['config'].default else [],config_file_open_func=ConfigFileOpenFunc)
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key, is_config_file=a.isConfigFile)
    #read the arguments
    args = parser.parse_args(argv)
    # print header
    if(args.printHeader):
        PrintCliHeader(MODULE_NAME, version,None)
    # print args
    if(args.printArgs):
        for a in argDefs.values():
            PrintCliArgument(a, getattr(args, a.key))
    # write config file if desired
    if (args.configout):
        outPath = args.configout
        args.config = None  # remove. Otherwise, the config file path is stored, which makes no sence.
        args.configout = None  # remove. Otherwise, the config file overrides itself on being used.
        parser.write_config_file(args, [outPath])
    try:
        #initialize a monitor for each service
        domMonitor = None
        mplMonitor = None
        amaMonitor = None
        ahaMonitor = None
        #start the domain
        if(args.enableDomain):
            print("Starting domain...")
            domMonitor = SubprocessMonitor(SERVICE_READY_MESSAGE,"q\n",True,True,"DOM>>","DOM!!")
            domMonitor.Start(WsDomainCli,['--config',args.domainConfig])
            while(not domMonitor.isReady):
                if(not domMonitor.isRunning): #the startup failed
                    raise RuntimeError("Failed to start the domain.")
                time.sleep(0.5)
        #start the MPL
        if(args.enableMpl):
            print("Starting MPL...")
            mplMonitor = SubprocessMonitor(SERVICE_READY_MESSAGE,"q\n",True,True,"MPL>>","MPL!!")
            mplMonitor.Start(WsMplCli,['--config',args.mplConfig])
            while(not mplMonitor.isReady):
                if(not mplMonitor.isRunning): #the startup failed
                    raise RuntimeError("Failed to start the MPL.")
                time.sleep(0.5)
        #start the Action Manager
        if(args.enableActionManager):
            print("Starting Action Manager...")
            amaMonitor = SubprocessMonitor(SERVICE_READY_MESSAGE,"q\n",True,True,"AMA>>","AMA!!")
            amaMonitor.Start(WsActionManagerCli,['--config',args.actionManagerConfig])
            while(not amaMonitor.isReady):
                if(not amaMonitor.isRunning): #the startup failed
                    raise RuntimeError("Failed to start the Action Manager.")
                time.sleep(0.5)
        #start the Action Handler
        if(args.enableActionHandler):
            print("Starting Action Handler...")
            ahaMonitor = SubprocessMonitor(SERVICE_READY_MESSAGE,"q\n",True,True,"AHA>>","AHA!!")
            ahaMonitor.Start(WsActionHandlerCli,['--config',args.actionHandlerConfig])
            while(not ahaMonitor.isReady):
                if(not ahaMonitor.isRunning): #the startup failed
                    raise RuntimeError("Failed to start the Action Manager.")
                time.sleep(0.5)
        #all services started show menu
        def ShowServiceStatus():
            print("Domain        : %s"%("1" if None!=domMonitor and domMonitor.isRunning else "0"))
            print("MPL           : %s"%("1" if None!=mplMonitor and mplMonitor.isRunning else "0"))
            print("Action Manager: %s"%("1" if None!=amaMonitor and amaMonitor.isRunning else "0"))
            print("Action Handler: %s"%("1" if None!=ahaMonitor and ahaMonitor.isRunning else "0"))
        ServiceMenuLoop(ShallRun(), "EOQ3 server ready!", 'q', {'status':("Service status",ShowServiceStatus)})
        #shut down
        if (ahaMonitor):
            ahaMonitor.Quit()
        if (amaMonitor):
            amaMonitor.Quit()
        if (mplMonitor):
            mplMonitor.Quit()
        if (domMonitor):
            domMonitor.Quit()
        print('EOQ3 server says goodbye!')
        os._exit(0)
    except Exception as e:
        print("ERROR: %s"%(str(e)))
        traceback.print_exc()
        if(ahaMonitor):
            ahaMonitor.Quit()
        if(amaMonitor):
            amaMonitor.Quit()
        if(mplMonitor):
            mplMonitor.Quit()
        if(domMonitor):
            domMonitor.Quit()
        os._exit(1) #make sure all processes are killed
        
'''
MAIN: Execution starts here
'''            
if __name__ == "__main__":
    code = WsServerCli(sys.argv[1:])
    ExitHard(code)
    