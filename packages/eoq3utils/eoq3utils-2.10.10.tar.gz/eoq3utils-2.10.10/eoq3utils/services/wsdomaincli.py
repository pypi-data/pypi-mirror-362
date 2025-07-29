"""
This starts a model database (MDB) domain and offers it via a web socket server.
Optionally also a TCP/IP server can be started.

See EOQ User Manual for more information: https://gitlab.com/eoq/doc

2024 Bjoern Annighoefer
"""

from .. import __version__ as version
# eoq
from eoq3 import __version__ as eoqVersion
from eoq3.command import Hel
from eoq3.domainwrappers import DomainToProcessWrapper, DomainPool
from eoq3.domainwithmdb import DomainWithMdb
from eoq3.util import GenerateSessionId
# mdb
from eoq3pyecoremdb import __version__ as pyEcoreMdbVersion
from eoq3pyecoremdb import PyEcoreMdb
# access control
from eoq3pyaccesscontroller import __version__ as pyAccessControllerVersion
from eoq3pyaccesscontroller import PyAccessController, UserRecord, GenericPermission
from eoq3pyecoreutils.pyecorepatch import EnableEObjectAnnotationsPatch
# web socket server
from eoq3autobahnws import __version__ as autobahnWsVersion
from eoq3autobahnws.autobahnwsdomainhost import AutobahnWsDomainHost
# eoq cli commons
from ..cli.common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, PrintCliArgumentValues, ExitHard
from ..cli.commonws import PrepareSslServerContextFactory
from .common import PrintServiceReadyMessage, ServiceMenuLoop, ShallRun,  ConfigFileOpenFunc, WriteConfigFileIfGiven
# external imports
import configargparse #like argparse but allows for config files in addition to command line parameters
import json #required for user and permissions file
import traceback
import sys
# type annotations
from typing import List, Dict, Any

MODULE_NAME = "eoq3utils.services.wsdomaincli"

### DOMAIN FACTORY ###

def DomainFactory(domainFactoryArgs:Dict[str,Any]):
    """The function that is called in the process to create the domain
    """
    #prepare the config based on the domain args
    config = domainFactoryArgs['config']
    if(domainFactoryArgs['enableEObjectAnnotationsPatch']):
        EnableEObjectAnnotationsPatch()
    #create the mdb
    mdb = PyEcoreMdb(config)
    domain = None
    if(domainFactoryArgs['enableAccessControl']):
        #generate user dict for ac initialization
        users = [UserRecord(u['user'] , u['passhash'], u['groups'], u['events'], u['superevents']) for u in domainFactoryArgs['usersDict']]       
        #create default permissions 
        permissions = [GenericPermission(g['classId'] , g['feature'], g['owner'], g['group'], g['permission']) for g in domainFactoryArgs['permissionsDict']]       
        #initialize the access controller
        ac = PyAccessController(users=users,genericPermissions=permissions,superAdminPasshash=domainFactoryArgs['superAdminPasshash'],config=config)
        domain = DomainWithMdb(mdb,ac,config=config)
        #if interactive user management is desired, connect access controller and domain
        if(domainFactoryArgs['interactiveAccessControl']):
            domain.Do(Hel(domainFactoryArgs['accessControllerUser'],domainFactoryArgs['accessControllerPw']),domainFactoryArgs['accessControllerSession']) 
            ac.Connect(domain,domainFactoryArgs['accessControllerSession'])
    else:
        domain = DomainWithMdb(mdb,config=config)
    return domain

### LOAD USERS ###

def LoadUsers(filepath:str)->List[Dict[str,Any]]:
    #load from json if existing
    usersDict = []
    with open(filepath, 'r') as f:
        usersDict = json.load(f)
        #check the content for correctness
        if(not isinstance(usersDict,list)):
            raise RuntimeError('%s has wrong JSON format. Expected an array of user objects'%(filepath))
        i = 0
        for u in usersDict:
            if('user' not in u):
                raise RuntimeError('User %d is missing entry "user"'%(i))
            else:
                uname = u['user']
                if('groups' not in u):
                    raise RuntimeError('User %s is missing entry "groups"'%(uname))
                elif('events' not in u):
                    raise RuntimeError('User %s is missing entry "events"'%(uname))
                elif('superevents' not in u):
                    raise RuntimeError('User %s is missing entry "superevents"'%(uname))
            i += 1
    return usersDict

def LoadPermissions(filepath:str)->List[Dict[str,Any]]:
    #load from json if existing
    permissionsDict = []
    with open(filepath, 'r') as f:
        permissionsDict = json.load(f)
        #check the content for correctness
        if(not isinstance(permissionsDict,list)):
            raise RuntimeError('%s has wrong JSON format. Expected an array of permission objects'%(filepath))
        i = 0
        for e in permissionsDict:
            if('classId' not in e):
                raise RuntimeError('User %d is missing entry "classId"'%(i))
            elif('feature' not in e):
                raise RuntimeError('User %d is missing entry "feature"'%(i))
            elif('owner' not in e):
                raise RuntimeError('User %d is missing entry "owner"'%(i))
            elif('group' not in e):
                raise RuntimeError('User %d is missing entry "group"'%(i))
            elif('permission' not in e):
                raise RuntimeError('User %d is missing entry "permission"'%(i))
            e['permission'] = int(e['permission'],base=16) #permissions are saved as str, because JSON does not support hex
            i += 1
    return permissionsDict

def WsDomainCli(argv:List[Any])->int:
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'config',
        'configout',
        'connectTimeout',
        'remoteFrmTxSerializer',
        'remoteCmdTxSerializer',
        'remoteFrmRxSerializer',
        'remoteCmdRxSerializers',
        'wsHost',
        'wsPort',
        'enableSsl',
        'sslCertificatePem',
        'sslCertificateKeyPem',
        'sslCertificatePassword',
        'domainType',
        'nDomainWorkers',
        'maxChanges',
        'enableStatistics',
        'enableEObjectAnnotationsPatch',
        'enableAccessControl',
        'superAdminPasshash',
        'usersFile',
        'permissionsFile',
        'interactiveAccessControl',
        'accessControllerUser',
        'accessControllerPw',
        'logToConsole',
        'logToFile',
        'logLevel',
        'logDir',
        'logFileName',
        'logFileSplit',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
        'enableTcp',
        'tcpHost',
        'tcpPort',
    ])
    # use configargparse to parse the command line arguments
    parser = configargparse.ArgParser(description='An eoq3 domain listening for commands on a web socket.',default_config_files=[argDefs['config'].default] if argDefs['config'].default else [], config_file_open_func=ConfigFileOpenFunc)
    for a in argDefs.values():
        parser.add_argument('--'+a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key, is_config_file=a.isConfigFile)
    #read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME,version,{"eoq3":eoqVersion, "eoq3pyecoremdb":pyEcoreMdbVersion,"eoq3autobahnws":autobahnWsVersion, "eoq3pyaccesscontroller":pyAccessControllerVersion},shallPrint=args.printHeader)
    #print args
    PrintCliArgumentValues(args,argDefs,args.printArgs)
    #write config file if desired
    WriteConfigFileIfGiven(args, parser)
    #create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    #initialize a session ID for the access controller
    accessControllerSession = GenerateSessionId()
    usersDict = []
    permissionsDict = []
    if(args.enableAccessControl):
        usersDict = LoadUsers(args.usersFile)
        permissionsDict = LoadPermissions(args.permissionsFile)
    #initialize variables to make sure they are defined in the finally block
    domain = None
    server = None
    tcpServer = None
    returnCode = 0 #success
    try:
        #create the domain as parallel working processes 
        print("Creating domain... ",end="")
        domainFactoryArgs = { 
                              'superAdminPasshash' : args.superAdminPasshash,
                              'enableEObjectAnnotationsPatch' : args.enableEObjectAnnotationsPatch,
                              'enableAccessControl' : args.enableAccessControl,
                              'interactiveAccessControl' : args.interactiveAccessControl,
                              'accessControllerSession' : accessControllerSession,
                              'accessControllerUser' : args.accessControllerUser,
                              'accessControllerPw' : args.accessControllerPw,
                              'usersDict' : usersDict,
                              'permissionsDict' : permissionsDict,
                              'config' : config,
                            }
        domain = DomainPool([DomainToProcessWrapper(DomainFactory,domainFactoryArgs,config=config) for i in range(args.nDomainWorkers)], shallForwardSerializedCmds=True, config=config)
        print("ready")
        #create and start the web socket server
        print("Starting WS Server... ",end="")
        sslContextFactory, sslContextFactoryArgs = PrepareSslServerContextFactory(args)
        server = AutobahnWsDomainHost(domain, True, args.wsHost, args.wsPort, sslContextFactory, sslContextFactoryArgs, args.nDomainWorkers, config)
        print("ready")
        print("WS listening on %s:%d (SSL %s)"%(args.wsHost,args.wsPort,"on" if args.enableSsl else "off"))
        # start additional TCP-Server, if desired
        if(args.enableTcp):
            from eoq3tcp.tcpdomainhost import TcpDomainHost #only import if TCP is desired
            tcpServer = TcpDomainHost(domain,True,args.tcpHost,args.tcpPort,2**20,b'\x00',config)
            print("TCP listening on %s:%d"%(args.tcpHost,args.tcpPort))
        # initialization finished. enter the endless loop        
        shallRun = True
        #show quit information.
        print("Domain ready!")
        PrintServiceReadyMessage()
        ServiceMenuLoop(ShallRun(), None,'q')
    except Exception as e:
        print("ERROR: %s"%(str(e)))
        traceback.print_exc()
        returnCode = 1 #make sure all processes are killed
    finally:
        # shut down
        if(tcpServer):
            print("Stopping TCP Server... ", end="")
            tcpServer.Stop()
            print("ok")
        if(server):
            print("Stopping WS Server... ", end="")
            server.Stop()
            print("ok")
        if(domain):
            print("Closing domain... ", end="")
            domain.Close()
            print("ok")
        print('Domain says goodbye!')
    return returnCode
        
        
'''
MAIN: Execution starts here
'''            
if __name__ == "__main__":
    MODULE_NAME = "eoq3utils.services.wsdomaincli"
    code = WsDomainCli(sys.argv[1:])
    ExitHard(code)
    