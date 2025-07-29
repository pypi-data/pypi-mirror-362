"""
 Common functions used for services
 Bjoern Annighoefer 2024
"""

from ..cli.common import RegisterCliArgument, GetInModuleFileAbsPath, none_or_str
# type annotations
from typing import Dict, Callable, Tuple, Any

# Service constants
SERVICES_MODULE_NAME = 'eoq3utils.services'
CONFIG_PATH = 'config'
SERVICE_READY_MESSAGE = 'Service startup completed.'


def PrintServiceReadyMessage():
    """Prints the service ready message
    """
    print(SERVICE_READY_MESSAGE)

class ShallRun:
    """A class to signal the service to run.
    This is used to allow other processes to
    stopp the service.
    """
    def __init__(self):
        self.shallRun:bool = True

def ServiceMenuLoop(shallRun:ShallRun, message:str=None, quitCommand:str='q', customCommands:Dict[str,Tuple[str,Callable[[],None]]]=None):
    """Loops until the user types a quit command.
    In addition, other commands can be used registered.
    """
    #show quit information.
    if(None!=message):
        print(message)
    while(shallRun.shallRun):
        userInput = input("Please enter command or %s to quit:\n"%(quitCommand))
        if(quitCommand == userInput):
            shallRun.shallRun = False
        elif('help' == userInput):
            print("q: exit")
            print("help: show help")
            if(None != customCommands):
                for(k,v) in customCommands.items():
                    print("%s: %s"%(k,v[0]))
        elif(None!= customCommands and userInput in customCommands):
            try:
                customCommands[userInput][1]()
            except Exception as e:
                print("ERROR: %s"%(str(e)))
        else:
            print("Unknown command %s. Enter help for to list commands."%(userInput))

def ConfigFileOpenFunc(file, mode='r'):
    """Opens a config file and returns the file object.
    This wraps the build in open function to allow for
    the same file endings on all platforms.
    """
    return open(file, mode, newline="\n")

def WriteConfigFileIfGiven(args:Any, parser:Any):
    """Writes a config file using the ConfigArgParser if args.configout is not None.
    """
    if (args.configout):
        outPath = args.configout
        args.config = None  # remove. Otherwise, the config file path is stored, which makes no sence.
        args.configout = None  # remove. Otherwise, the config file overrides itself on being used.
        parser.write_config_file(args, [outPath])

### REGISTER COMMON SERVICE ARGUMENTS ###
# Config files
RegisterCliArgument('config',                 "Config",               typ=none_or_str, default=None, description='Path to a config file', isConfigFile=True)
RegisterCliArgument('configout',              "Config out",           typ=none_or_str, default=None, description='If given, a config file with the current settings is written')
# Web Socket connection (advanced)
RegisterCliArgument('sslCertificateKeyPem',   "SSL key",              typ=none_or_str, default=GetInModuleFileAbsPath(SERVICES_MODULE_NAME, CONFIG_PATH, 'sslKey_DO_NOT_USE_IN_PRODUCTION.pem'), description='Path to the private key pem file of the SSL server')
RegisterCliArgument('sslCertificatePassword', "SSL cert PW",          typ=none_or_str, default='ILS-admin', description='Pass phrase used for the certificate or key pem', isSecret=True)
# TCP connection (advanced)
RegisterCliArgument('enableTcp',              "Enable TCP",           typ=int,         default=0, description='Open a TCP-port for accessing the domain? (0=no, 1=yes)')
# Domain type
RegisterCliArgument('domainType',             "Domain type",          typ=int,         default=1, description='The type of domain to be created: 1=local single-thread, 2=process wrapped single-thread, 3=domain-pool multi-thread, 4=domain-pool multi-process')
# MDB setup
RegisterCliArgument('nDomainWorkers',         "Nb. workers",          typ=int,         default=2, description='The number of parallel processes processing domain requests')
RegisterCliArgument('maxChanges',             "Max changes",          typ=int,         default=100, description='How many changes shall be remembered until the oldest change is forgotten (1 to 1000000)')
RegisterCliArgument('enableStatistics',       "Statistics",           typ=int,         default=0, description='Measure the time for queries and commands and write log when closed? (0=no, 1=yes)')
RegisterCliArgument('enableEObjectAnnotationsPatch', "EAnnot. patch", typ=int,         default=1, description='Enables any EObject to have EAnnotations. Breaks compatibility with EMF. This is must be enabled if enableAccessControl is used. (0=no, 1=yes)')
# Access control
RegisterCliArgument('enableAccessControl',    "Access ctrl.",         typ=int,         default=1, description='Shall access to the MDB be protected based on user rights? (0=no, 1=yes)')
RegisterCliArgument('superAdminPasshash',     "Super admin PH",       typ=str,         default='7mjDFTt6Jrwov+beGIeSIJVWxLsooD8Q5gLxDXLW5OHeQHV6vWKsrBB/M6GK+eVdancrryEc2uZRekW/yqZdKQ==', description='Use eoq3pyaccesscontoller/util/generatepashash.py --pw "pw" to generate (default pw -> DAMMMMN!#)', isSecret=True)
RegisterCliArgument('usersFile',              "Users",                typ=none_or_str, default=GetInModuleFileAbsPath(SERVICES_MODULE_NAME, CONFIG_PATH, 'users_DO_NOT_USE_IN_PRODUCTION.json'), description='The path to the user definition JSON file')
RegisterCliArgument('permissionsFile',        "Permissions",          typ=none_or_str, default=GetInModuleFileAbsPath(SERVICES_MODULE_NAME, CONFIG_PATH, 'permissions_DO_NOT_USE_IN_PRODUCTION.json'), description='The path to the generic permission definitions JSON file')
RegisterCliArgument('interactiveAccessControl',"Log dir",             typ=int,         default=1, description='Users and generic permissions are managed in the MDB and can be modified')
RegisterCliArgument('accessControllerUser',   "Access ctrl. user",    typ=none_or_str, default='aco', description='The user for the access controller. Is required if interactive user management is desired')
RegisterCliArgument('accessControllerPw',     "Access ctrl. user PW", typ=none_or_str, default='aha1289?', description='The password of the access controller. Is required if interactive user management is desired', isSecret=True)

