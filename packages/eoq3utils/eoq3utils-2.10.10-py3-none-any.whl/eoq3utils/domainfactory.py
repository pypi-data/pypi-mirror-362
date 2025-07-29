"""
 DomainFactory offers help to create different kinds of domains with the same interface
 Bjoern Annighoefer 2024
"""

from eoq3pyecoremdb import PyEcoreMdb

from eoq3.domainwrappers import DomainToProcessWrapper,DomainPool
from eoq3.domain import Domain
from eoq3.domainwithmdb import DomainWithMdb
from eoq3.config import Config,EOQ_DEFAULT_CONFIG
from eoq3.error import EOQ_ERROR_INVALID_VALUE, EOQ_ERROR_DOES_NOT_EXIST, EOQ_ERROR_RUNTIME

from typing import Dict, Any, Union, Callable, Type

class DOMAIN_TYPES:
    """Pre-defined domain types
    More can be added by if needed
    """
    LOCAL = 1
    LOCALPROCESS = 2
    MULTITHREAD_DOMAINPOOL = 3
    MULTIPROCESS_DOMAINPOOL = 4
    TCPCLIENT = 5
    WSCLIENT = 6
    EXT_TCP_SERVER = 7
    ADAEOQ = 8

### DOMAIN CREATION REGISTRY ###

class DomainInfo:
    def __init__(self, domainType:int, creationHandler:Callable[[Config,Dict[str,Any]],Domain], closeHandler:Callable[[Domain],None], settingsDefinition:Dict[str,Union[Type[str],Type[int],Type[float],Type[bool]]]):
        self.domainType = domainType
        self.settingsDefinition = settingsDefinition
        self.creationHandler = creationHandler
        self.closeHandler = closeHandler

CREATEDOMAIN_REGISTRY = {}

def RegisterDomainTypeForCreation(domainType:int, creationHandler:Callable[[Config,Dict[str,Any]],Domain], closeHandler:Callable[[Domain],None], settingsDefinition:Dict[str,Union[Type[str],Type[int],Type[float],Type[bool]]])->None:
    if(domainType in CREATEDOMAIN_REGISTRY):
        raise ValueError("DomainType %s is already registered."%(str(domainType)))
    CREATEDOMAIN_REGISTRY[domainType] = DomainInfo(domainType, creationHandler, closeHandler, settingsDefinition)

def GetDomainInfoForCreation(domainType:int)->DomainInfo:
    try:
        return CREATEDOMAIN_REGISTRY[domainType]
    except KeyError as e:
        raise EOQ_ERROR_DOES_NOT_EXIST("Domain of type %d is unknown"%(domainType))

def ValidateDomainSettings(settingsDefinition:Dict[str,Union[Type[str],Type[int],Type[float],Type[bool]]], settings:Dict[str,Any])->None:
    for k,v in settings.items():
        if(k not in settingsDefinition):
            raise EOQ_ERROR_INVALID_VALUE("Unknown setting: %s"%(k))
        if(not isinstance(v,settingsDefinition[k])):
            raise EOQ_ERROR_INVALID_VALUE("Setting %s is %s but expected %s."%(k,str(type(v)),str(settingsDefinition[k])))
    for k,v in settingsDefinition.items():
        if(k not in settings):
            raise EOQ_ERROR_INVALID_VALUE("Missing setting: %s"%(k))

### DOMAIN CREATE AND CLOSE HANDLERS ###

# Domain with local command processor

def CreateLocalDomain(config:Config=EOQ_DEFAULT_CONFIG)->Domain:
    """Creates the simplest type of domain: a local 
    local command processor with MDB
    """
    mdb = PyEcoreMdb(config=config)
    domain = DomainWithMdb(mdb,config=config)
    return domain
    
def CreationHandlerLocalDomain(config:Config,domainSettings:Dict[str,Any])->Domain:
    return CreateLocalDomain(config)

def CloseLocalDomainHandler(domain:Domain)->None:
    """The default close handler for domains"""
    domain.Close()

RegisterDomainTypeForCreation(DOMAIN_TYPES.LOCAL,CreationHandlerLocalDomain,CloseLocalDomainHandler, {}) 

# Domain with process wrapper

def DomainFactory(domainFactoryArgs:Any):
    """The function that is called in the process to create the domain
    """
    return CreateLocalDomain(domainFactoryArgs)

def CreationHandlerLocalProcessDomain(config:Config,domainSettings:Dict[str,Any])->Domain:
    return DomainToProcessWrapper(DomainFactory,domainFactoryArgs=config,config=config)
RegisterDomainTypeForCreation(DOMAIN_TYPES.LOCALPROCESS,CreationHandlerLocalProcessDomain,CloseLocalDomainHandler,{})

# Domain with multi thread pool

def CreationHandlerMultiThreadDomainPool(config:Config,domainSettings:Dict[str,Any])->Domain:
    return DomainPool([DomainWithMdb(PyEcoreMdb(config=config),config=config) for i in range(domainSettings["numberOfDomainWorkers"])],shallForwardSerializedCmds=False)
RegisterDomainTypeForCreation(DOMAIN_TYPES.MULTITHREAD_DOMAINPOOL,CreationHandlerMultiThreadDomainPool,CloseLocalDomainHandler,{"numberOfDomainWorkers":int})

# Domain with multi process pool

def CreationHandlerMultiProcessDomainPool(config:Config,domainSettings:Dict[str,Any])->Domain:
    return DomainPool([DomainToProcessWrapper(DomainFactory,domainFactoryArgs=config,config=config) for i in range(domainSettings["numberOfDomainWorkers"])],shallForwardSerializedCmds=True)
RegisterDomainTypeForCreation(DOMAIN_TYPES.MULTIPROCESS_DOMAINPOOL,CreationHandlerMultiProcessDomainPool,CloseLocalDomainHandler,{"numberOfDomainWorkers":int})

# Domain with TCP client

def CreationHandlerTcpDomain(config:Config,domainSettings:Dict[str,Any])->Domain:
    from eoq3tcp.tcpdomainclient import TcpDomainClient
    if (domainSettings["startServer"]):  # for testing purpose it can be useful to start a matching host
        from eoq3tcp.tcpdomainhost import TcpDomainHost
        server = {}
        server["innerDomain"] = CreateLocalDomain(config)
        server["host"] = TcpDomainHost(server["innerDomain"], False, domainSettings["host"], domainSettings["port"],
                                       config=config)
        try:
            domain = TcpDomainClient(domainSettings["host"], domainSettings["port"], config=config)
            domain.createDomainData = server
        except Exception as e:
            # make sure the server is closed if client creating failed
            server["host"].Stop()
            server["innerDomain"].Close()
            raise e
    else:
        domain = TcpDomainClient(domainSettings["host"], domainSettings["port"], config=config)
    return domain

def CloseDomainWithServerHandler(domain:Domain)->None:
    """Close the domain gracefully.
    If a server is running, it will be stopped as well.
    """
    domain.Close()
    if(hasattr(domain,"createDomainData")):
        domain.createDomainData["host"].Stop()
        domain.createDomainData["innerDomain"].Close()

RegisterDomainTypeForCreation(DOMAIN_TYPES.TCPCLIENT,CreationHandlerTcpDomain,CloseDomainWithServerHandler,{"host":str,"port":int,"startServer":bool})

# Domain with WS client

def CreationHandlerWsDomain(config:Config,domainSettings:Dict[str,Any])->Domain:
    from eoq3autobahnws.autobahnwsdomainclient import AutobahnWsDomainClient
    if (domainSettings["startServer"]):  # for testing purpose it can be useful to start a matching host
        from eoq3autobahnws.autobahnwsdomainhost import AutobahnWsDomainHost
        server = {}
        server["innerDomain"] = CreateLocalDomain(config)
        server["host"] = AutobahnWsDomainHost(server["innerDomain"], False, domainSettings["host"],
                                              domainSettings["port"], config=config)
        try:
            domain = AutobahnWsDomainClient(domainSettings["host"], domainSettings["port"], config=config)
            domain.createDomainData = server #artificially attach the server infos to the domain
        except Exception as e:
            # make sure the server is closed if client creating failed
            server["host"].Stop()
            server["innerDomain"].Close()
            raise e
    else:
        domain = AutobahnWsDomainClient(domainSettings["host"], domainSettings["port"], config=config)
    return domain
RegisterDomainTypeForCreation(DOMAIN_TYPES.WSCLIENT,CreationHandlerWsDomain,CloseDomainWithServerHandler,{"host":str,"port":int,"startServer":bool})


# TCP client with external executable
def CreationHandlerTcpDomainWithExternalServer(config:Config,domainSettings:Dict[str,Any])->Domain:
    """Creates a TCP domain client and starts an external server by a given command
    e.g. AdaEOQ
    """
    from eoq3tcp.tcpdomainclient import TcpDomainClient
    import subprocess
    #import time
    # start external server
    cmd = domainSettings["cmd"]
    cwd = domainSettings["cwd"]
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdin=subprocess.PIPE)
    # wait for server to start
    try:
        p.wait(timeout=domainSettings["startTimeout"])
        raise EOQ_ERROR_RUNTIME("Server start failed, return code: %d"%(p.returncode))
    except subprocess.TimeoutExpired: #this is good, because the server is still running
        # now try to connect the client
        try:
            domain = TcpDomainClient(domainSettings["host"], domainSettings["port"], domainSettings["maxMsgSize"], domainSettings["msgSep"], config=config)
            domain.createDomainData = {"process":p,"stopTimeout":domainSettings["stopTimeout"]}
            return domain
        except Exception as e:
            # make sure the server is closed if client creating failed
            p.kill()
            raise e

def CloseDomainWithExternalServerHandler(domain:Domain)->None:
    """Close the domain gracefully.
    If a server is running, it will be stopped as well.
    """
    import time
    domain.Close()
    if(hasattr(domain,"createDomainData")):
        domain.createDomainData["process"].terminate()
        time.sleep(domain.createDomainData["stopTimeout"]) #make sure all subprocesses are closed

RegisterDomainTypeForCreation(DOMAIN_TYPES.EXT_TCP_SERVER,CreationHandlerTcpDomainWithExternalServer,CloseDomainWithExternalServerHandler,{"host":str,"port":int,"maxMsgSize":int,"msgSep":bytes,"cmd":str,"cwd":str,"startTimeout":float,"stopTimeout":float})

# ADAEOQ with TCP client
def CreationHandlerTcpAdaeoq(config:Config,domainSettings:Dict[str,Any])->Domain:
    """Creates a TCP domain client and starts an external server by a given command
    e.g. AdaEOQ
    """
    import os
    ENV_ADAEOQ_PATH = "ADAEOQPATH"
    ENV_ADAEOQ_CMD = "ADAEOQCMD"
    try:
        cmd = os.path.join(os.environ[ENV_ADAEOQ_PATH],os.environ[ENV_ADAEOQ_CMD])
        cwd = os.environ[ENV_ADAEOQ_PATH]
        domainSettings["cmd"] = cmd
        domainSettings["cwd"] = cwd
        return CreationHandlerTcpDomainWithExternalServer(config,domainSettings)
    except KeyError as e:
        raise EOQ_ERROR_RUNTIME("Environment variables %s or % s not set."%(ENV_ADAEOQ_PATH,ENV_ADAEOQ_CMD))

RegisterDomainTypeForCreation(DOMAIN_TYPES.ADAEOQ,CreationHandlerTcpAdaeoq,CloseDomainWithExternalServerHandler,{"host":str,"port":int,"maxMsgSize":int,"msgSep":bytes,"startTimeout":float,"stopTimeout":float})

### MAIN FUNCTIONS ###

def CreateDomain(domainType:int, domainSettings:Dict[str,Any], config:Config=EOQ_DEFAULT_CONFIG)->Domain:
    """ Creates a domain with the given type and settings
    """
    domainInfo = GetDomainInfoForCreation(domainType)
    ValidateDomainSettings(domainInfo.settingsDefinition,domainSettings)
    domain = domainInfo.creationHandler(config,domainSettings)
    domain.createDomainType = domainType
    return domain


def CleanUpDomain(domain)->None:
    """Close the domain gracefully by calling the close handler
    """
    domainInfo = GetDomainInfoForCreation(domain.createDomainType)
    domainInfo.closeHandler(domain)
        