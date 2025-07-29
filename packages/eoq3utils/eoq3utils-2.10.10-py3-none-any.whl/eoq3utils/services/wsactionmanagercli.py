"""
This is a management script to configure and start services of an
EOQ3 action manager client and connect it to a domain via web socket.
The action manager extends the domain with the ability to register and execute
custom actions.

See EOQ User Manual for more information: https://gitlab.com/eoq/doc

2024 Bjoern Annighoefer
"""

from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoqVersion
from eoq3.command import Hel
from eoq3.util import GenerateSessionId
# action manager
from eoq3pyactions import __version__ as pyActionsVersion
from eoq3pyactions.actionmanager import ActionManager
# web socket
from eoq3autobahnws import __version__ as autobahnWsVersion
from eoq3autobahnws.autobahnwsdomainclient import AutobahnWsDomainClient
# eoq cli commons
from ..cli.common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, LogginIfDesired, PrintCliArgumentValues, ExitHard
from ..cli.commonws import PrepareSslClientContextFactory
from .common import PrintServiceReadyMessage, ServiceMenuLoop, ShallRun, ConfigFileOpenFunc, WriteConfigFileIfGiven
# external imports
import configargparse #like argparse but allows for config files in addition to command line parameters
import traceback
import sys
#type checking 
from typing import List, Dict, Any

MODULE_NAME = "eoq3utils.services.wsactionmanagercli"

def WsActionManagerCli(argv:List[Any])->int:
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
        'user',
        'password',
        'enableSsl',
        'sslCertificatePem',
        'logToConsole',
        'logToFile',
        'logLevel',
        'logDir',
        'logFileName',
        'logFileSplit',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
    ])
    # modify predefined arguments
    argDefs['user'].default = 'ama'
    argDefs['password'].default = 'ama0948&'
    # use configargparse to parse the command line arguments
    parser = configargparse.ArgParser(description='An eoq3 action manager connecting via web socket to a domain.',default_config_files=[argDefs['config'].default] if argDefs['config'].default else [],config_file_open_func=ConfigFileOpenFunc)
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key, is_config_file=a.isConfigFile)
    #read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version,{"eoq3": eoqVersion, "eoq3pyactions": pyActionsVersion, "eoq3autobahnws": autobahnWsVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args,argDefs,args.printArgs)
    #write config file if desired
    WriteConfigFileIfGiven(args, parser)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    try:
        #create the domain as parallel working processes 
        print("Connecting to domain... ",end="")
        sslContextFactory, sslContextFactoryArgs = PrepareSslClientContextFactory(args)
        domain = AutobahnWsDomainClient(args.wsHost,args.wsPort,sslContextFactory=sslContextFactory,sslFactoryArgs=sslContextFactoryArgs,config=config)
        print("ready")
        #create and ...
        print("Creating Action Manager... ",end="")
        ama = ActionManager(config)
        print("ready")
        #... connect the action manager
        print("Connecting Action Manager to domain... ",end="")
        sessionId = LogginIfDesired(domain, args.user, args.password)
        ama.Connect(domain, sessionId)
        print("ready")
        PrintServiceReadyMessage()
        ServiceMenuLoop(ShallRun(), "Action Manager running.", 'q')
        #shut down 
        print("Closing Action Manager... ",end="")
        ama.Close()
        print("ok")
        print("Closing domain connection... ",end="")
        domain.Close()
        print("ok")
        print('Action Manager says goodbye!')
        return 0 #no failure
    except Exception as e:
        print("ERROR: %s"%(str(e)))
        traceback.print_exc()
        return 1 #make sure all processes are killed


'''
MAIN: Execution starts here
'''            
if __name__ == "__main__":
    code = WsActionManagerCli(sys.argv[1:])
    ExitHard(code)
    