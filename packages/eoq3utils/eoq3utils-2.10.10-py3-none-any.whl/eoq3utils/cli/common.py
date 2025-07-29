"""
 Common functions used for EOQ CLI modules
 Bjoern Annighoefer 2024
"""
# eoq3 imports
from eoq3.config import Config
from eoq3.domain import Domain
from eoq3.logger import DEFAULT_LOGGER_LEVELS
from eoq3.command import Hel
from eoq3.value import STR
from eoq3.util import GenerateSessionId
# external imports
from importlib.resources import files, as_file # for internal resources
import sys
import os
from typing import Any, Dict, List, Tuple

# constants
SERVICES_MODULE_NAME = 'eoq3utils.services'
CONFIG_PATH = 'config'

def GetInModuleFileAbsPath(moduleName:str, innerPath:str, fileName:str)->str:
    """Returns the absolute path for a file delivered in a module
    """
    filePath = None
    with as_file(files(moduleName).joinpath(innerPath).joinpath(fileName)) as moduleFile:
        filePath = str(moduleFile.absolute())
    return filePath

class CliArgument:
    """A class to define a command line argument used by eoq3 CLI modules.
    This seperate class enables an easy conversion to argparse arguments or
    configargparse arguments.
    It also enables to reuse arguments in different CLI modules.
    """
    def __init__(self, key:str, name:str, short:str=None, description:str=None, required:bool=False, typ:any=str, default:Any=None, isSecret:bool=False, isConfigFile:bool=False):
        self.key:str = key #key to be used in the command line, i.e. --key
        self.name:str = name #full text name of the argument
        self.short:str = short #one char key (optional) for the command line, i.e. -k
        self.description:str = description #
        self.required:bool = required
        self.typ:str = typ #str,int
        self.default:Any = default
        self.isSecret:bool = isSecret #if true, the value is not printed
        self.isConfigFile:bool = isConfigFile #if true, the value is a path to a config file

    def Set(self, propertyNamesAndValues:Dict[str,Any]):
        """Sets the values from a dictionary
        """
        for (k,v) in propertyNamesAndValues.items():
            setattr(self, k, v)

CLI_ARGS_REGISTRY:Dict[str,CliArgument] = {} # a registry for predefined CLI arguments

def RegisterCliArgument(key:str, name:str, short:str=None, description:str=None, required:bool=False, typ:str=str, default:Any=None, isSecret:bool=False, isConfigFile:bool=False):
    CLI_ARGS_REGISTRY[key] = CliArgument(key, name, short, description, required, typ, default, isSecret, isConfigFile)

def GetCliPredefinedArguments(keys:List[str])->Dict[str,CliArgument]:
    """Returns a dictionary with the predefined arguments if existing.
    If a key does not exist in the predefined ones, an exception is raised.
    """
    return {k:CLI_ARGS_REGISTRY[k] for k in keys}

def PrintCliHeader(name:str=None,version:str=None,subVersions:Dict[str,str]=None,showLicense:bool=True,showCopyRight:bool=True, author:str='Bjoern Annighoefer',shallPrint:bool=True):
    """Default header printout for all pyeoq3 CLI modules.
    Prints the name, version, subversions, license and copy right.
    """
    if(shallPrint):
        print('************ pyeoq3 ************')
        if(name):
            print('%s:'%(name),end='')
        if(version):
            print('%s'%(version))
        if(subVersions):
            print("(%s)"%(", ".join(["%s:%s"%(k,v) for k,v in subVersions.items()])))
        if(showCopyRight):
            print("Copyright (c) 2025 %s"%(author))
        if(showLicense):
            print("MIT license - no warranty")
        print('********************************')

def PrintCliArgument(ca:CliArgument,value:Any=None,allign:int=20):
    """Prints a cli argument with its value
    If the value is a secret, it is masked by stars
    """
    if(ca.isSecret and None != value):
        value = '********'
    elif(str==type(value)):
        value = "'%s'"%(value)
    nl = len(ca.name)
    print('%s:%s%s'%(ca.name,"".join([" " for i in range(allign-nl)]),str(value)))

def PrintCliArgumentValues(args:Any,argDefs:Dict[str,CliArgument],shallPrint:bool):
    """Prints all values returned by argparse with the definitions in argDefs
    """
    if (shallPrint):
        for a in argDefs.values():
            PrintCliArgument(a, getattr(args, a.key))

def _GetLoggerLevelsByNumber(l:int):
    """Internal function to convert the logger levels from a single number.
    0 is silent, 1 is error, 2 is warning, 3 is info, 4 is debug.
    """
    logLevels = DEFAULT_LOGGER_LEVELS.L0_SILENT
    if(0 == l):
        logLevels = DEFAULT_LOGGER_LEVELS.L0_SILENT
    elif(1 == l):
        logLevels = DEFAULT_LOGGER_LEVELS.L1_ERROR
    elif(2 == l):
        logLevels = DEFAULT_LOGGER_LEVELS.L2_WARNING
    elif(3 == l):
        logLevels = DEFAULT_LOGGER_LEVELS.L3_INFO
    elif(4 == l):
        logLevels = DEFAULT_LOGGER_LEVELS.L4_DEBUG
    else:
        raise EOQ_ERROR_INVALID_VALUE('Invalid value %d for log level'%(l))
    return logLevels

def _GetLoggerAndInitArgs(logToConsole:bool, logToFile:bool, logDir:str, logFileName:str, logFileSplit:bool)->Tuple[str,Dict[str,Any]]:
    """Internal function to retrieve the logger and its init arguments
    based on the logToConsole and logToFile args.
    """
    if(logToConsole and logToFile):
        return "CFL", {"logDir":logDir, "prefix":logFileName, "splitFiles":logFileSplit}
    elif(logToConsole):
        return "CON", {}
    elif(logToFile):
        return "FIL", {"logDir":logDir, "prefix":logFileName, "splitFiles":logFileSplit}
    else:
        return "NOL", {}

def ArgparseToEoqConfig(args:Any)->Config:
    """Converts argparse arguments to an EOQ config
    All fields relevant for the EOQ config must be present in the argparse arguments,i.e.
    logToConsole, logToFile, logDir, logLevel, printExpectedExceptionTraces, printUnexpectedExceptionTraces
    connectTimeout
    """
    # initialize EOQ config
    config = Config()
    # determine loglevel
    if(hasattr(args,'logLevel')):
        config.activeLogLevels = _GetLoggerLevelsByNumber(args.logLevel)
    if(hasattr(args,'logToConsole') and hasattr(args,'logToFile') and hasattr(args,'logDir') and hasattr(args,'logFileName') and hasattr(args,'logFileSplit')):
        config.logger, config.loggerInitArgs = _GetLoggerAndInitArgs(args.logToConsole, args.logToFile, args.logDir, args.logFileName, args.logFileSplit)
    if(hasattr(args,'printExpectedExceptionTraces')):
        config.printExpectedExceptionTraces = args.printExpectedExceptionTraces
    if(hasattr(args,'printUnexpectedExceptionTraces')):
        config.printUnexpectedExceptionTraces = args.printUnexpectedExceptionTraces
    if(hasattr(args,'connectTimeout')):
        config.connectTimeout = args.connectTimeout  # reduce timeout to 2 seconds
    if(hasattr(args,'remoteFrmTxSerializer')):
        config.remoteFrmTxSerializer = args.remoteFrmTxSerializer
    if(hasattr(args,'remoteCmdTxSerializer')):
        config.remoteCmdTxSerializer = args.remoteCmdTxSerializer
    if(hasattr(args,'remoteFrmRxSerializer')):
        config.remoteFrmRxSerializer = args.remoteFrmRxSerializer
    if(hasattr(args,'remoteCmdRxSerializers')):
        config.remoteCmdRxSerializers = args.remoteCmdRxSerializers.split('|')
    if(hasattr(args,'fileSerializer')):
        config.fileSerializer = args.fileSerializer
    return config

def LogginIfDesired(domain:Domain, user:str, password:str, allwaysGenerateSessionId:bool=False)->str:
    """Logs in to the domain if a user and password are given
    and returns the session ID.
    If no user and password are given, None is returned,
    except allwaysGenerateSessionId is True, then a new session ID is generated.
    """
    sessionId = None
    if(user and password):
        sessionId = GenerateSessionId()
        domain.Do(Hel(STR(user), STR(password)), sessionId)
    elif(allwaysGenerateSessionId):
        sessionId = GenerateSessionId()
    return sessionId

def ExitGraceful(returncode:int):
    """Exits execution with the given system return code.
    A graceful waits for subprocesses to finish and buffers to be flushed.
    """
    sys.exit(returncode)

def ExitHard(returncode:int):
    """Exits execution with the given system return code immediately.
    All subprocess, threads and buffers are terminated.
    Unwritten data may be lost.
    """
    os._exit(returncode)

def none_or_str(value):
    """Fake type for argparse to allow for None values for strings
    """
    if value == 'None':
        return None
    return value

### REGISTER COMMON CLI ARGUMENTS ###
# Verbosity
RegisterCliArgument('printHeader',            "Print header",         typ=int,         default=1,             description='Show the header (1=show, 0=hide)')
RegisterCliArgument('printArgs',              "Print arg",            typ=int,         default=1,             description='Show list of arguments (1=show, 0=hide)')
# User
RegisterCliArgument('user',                   'User',                 typ=none_or_str, default=None,          description='If given, this user is used for accessing the domain')
RegisterCliArgument('password',               'Password',             typ=none_or_str, default=None,          description='If given and user is given, this password is used for accessing the domain', isSecret=True)
# Logging
RegisterCliArgument('logToConsole',           "Console log",          typ=int,         default=0,             description='Print log messages in the console? (0=no, 1=yes)')
RegisterCliArgument('logToFile',              "File log",             typ=int,         default=1,             description='Print log messages in log files? (0=no, 1=yes)')
RegisterCliArgument('logLevel',               "log levels",           typ=int,         default=2,             description='The verboseness of logging (0=silent, 1=error, 2=warning, 3=info, 4=debug)')
RegisterCliArgument('logDir',                 "Log path",             typ=str,         default='./log',       description='Destination folder for log file')
RegisterCliArgument('logFileName',            "Log file name",        typ=str,         default='log',         description='The name of the log file. The postfix is always .log')
RegisterCliArgument('logFileSplit',           "Split log files",      typ=int,         default=0,             description='Separate a log files for each log level? (0=no, 1=yes)')
RegisterCliArgument('printExpectedExceptionTraces',   "Trace known",  typ=int,         default=0,             description='Print Python trace for expected exceptions')
RegisterCliArgument('printUnexpectedExceptionTraces', "Trace unknown",typ=int,         default=1,             description='Print Python trace output for unexpected exceptions')
# Remote connection
RegisterCliArgument('connectTimeout',         "Con. timeout",         typ=float,       default=2.0,           description='The time waited for a connection to be established in seconds')
RegisterCliArgument('remoteFrmTxSerializer',  "Remote FRM ser.",      typ=str,         default='TXT',         description='The default serializer used for sending remote frames')
RegisterCliArgument('remoteCmdTxSerializer',  "Remote CMD ser.",      typ=str,         default='JSO',         description='The default serializer used for sending remote commands')
RegisterCliArgument('remoteFrmRxSerializer',  "Remote FRM ser.",      typ=str,         default='TXT',         description='The serializer allowed for incoming frames. For security reasons, this should not be JSC or PYT')
RegisterCliArgument('remoteCmdRxSerializers', "Remote CMD ser.",      typ=str,         default='TXT|JSO',     description='The serializers allowed for incoming commands seperated by |. All named here will be accepted for command deserialization. For security reasons, this should not be JSC or PYT')
RegisterCliArgument('fileSerializer',         'File serializer',      typ=str,         default='TXT',         description='EOQ expression to file serializer, e.g. TXT, JS, PY or JSO')
# Web Socket connection
RegisterCliArgument('wsHost',                 "WS host",              typ=str,         default='127.0.0.1',   description='Web socket host address')
RegisterCliArgument('wsPort',                 "WS port",              typ=int,         default=5141,          description='Web socket port')
RegisterCliArgument('enableSsl',              "Enable SSL",           typ=int,         default=1,             description='Enable SSL protected web socket. Certificate and key pem must be provided in addition (0=no, 1=yes)')
RegisterCliArgument('sslCertificatePem',      "SSL certificate",      typ=none_or_str, default=GetInModuleFileAbsPath(SERVICES_MODULE_NAME, CONFIG_PATH, 'sslCertificate_DO_NOT_USE_IN_PRODUCTION.pem'), description='Path to the certificate pem file to be used for the SSL server')
# TCP connection
RegisterCliArgument('tcpHost',                "TCP host",             typ=str,         default='127.0.0.1',   description='The EOQ TCP host address')
RegisterCliArgument('tcpPort',                "TCP port",             typ=int,         default=6141,          description='The EOQ TCP port')
# file processing
RegisterCliArgument('infile',                 'Input file',           typ=str,         default='input.model', description='The input file')
RegisterCliArgument('infile2',                'Input file 2',         typ=none_or_str, default=None,          description='The second input file')
RegisterCliArgument('infile3',                'Input file 3',         typ=none_or_str, default=None,          description='The the third input file')
RegisterCliArgument('infile4',                'Input file 4',         typ=none_or_str, default=None,          description='The the fourth input file')
RegisterCliArgument('outfile',                'Output file',          typ=str,         default='output.model',description='The output file')
#model options
RegisterCliArgument('metafile',               'Meta-file',            typ=none_or_str, default=None,          description='The meta-model file')
RegisterCliArgument('m1modelname',            'M1 Model Name',        typ=str,         default='m1model',     description='M1 model name')
RegisterCliArgument('checksyntax',            'Check syntax?',        typ=int,         default=0,             description='Validate input files before preprocessing')
RegisterCliArgument('rootobj',                'Root obj. qry.',       typ=str,         default='(/*MDB)',     description='A query retrieving the model element to be downloaded.')
