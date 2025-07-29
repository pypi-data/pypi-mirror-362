"""
Can be used to send a command via the command-line to a TCP domain.
2024 Bjoern Annighoefer
"""
from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoq3version
from eoq3.serializer import CreateSerializer
# tcp imports
from eoq3tcp import __version__ as eoq3tcpVersion
from eoq3tcp.tcpdomainclient import TcpDomainClient
# eoq cli commons
from .common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, CliArgument, LogginIfDesired, PrintCliArgumentValues, ExitGraceful
# external imports
import argparse
import sys
import traceback
from typing import List, Any

MODULE_NAME = "eoq3utils.cli.domaindotcpcli"

def DomainDoTcpCli(argv:List[Any]):
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'connectTimeout',
        'remoteFrmTxSerializer',
        'remoteCmdTxSerializer',
        'remoteFrmRxSerializer',
        'remoteCmdRxSerializers',
        'tcpHost',
        'tcpPort',
        'user',
        'password',
        'enableSsl', #currently not implemented
        'sslCertificatePem',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
        'remoteFrmTxSerializer',
        'remoteCmdTxSerializer',
    ])
    # modify predefined arguments
    argDefs['printHeader'].default = 0
    argDefs['printArgs'].default = 0
    # add custom arguments
    argDefs['cmd'] = CliArgument('cmd', 'Command', typ=str, default='GET (/*MDB)', description='The command to be executed')
    argDefs['serializer'] = CliArgument('serializer', 'Serializer', typ=str, default='TXT', description='The command and result serialization')
    # use argparse to parse the command line arguments
    parser = argparse.ArgumentParser(description='Executes a command on a remote TCP domain.')
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key)
    # read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version, {"eoq3":eoq3version,"eoq3tcp":eoq3tcpVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args,argDefs,args.printArgs)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    #convert the command
    serializer = CreateSerializer(args.serializer)
    cmd = serializer.DesCmd(args.cmd)
    # create client
    # TODO: SSL support
    domain = TcpDomainClient(args.tcpHost,args.tcpPort,2**20,b'\x00',config)
    try:
        #login if desired
        sessionId = LogginIfDesired(domain,args.user,args.password)
        # issue the command
        res = domain.Do(cmd, sessionId)
        # print the result
        resStr = serializer.SerVal(res)
        print(resStr, end="")
        # close the domain
        domain.Close()
        return 0
    except Exception as e:
        print("ERROR: %s" % (str(e)))
        traceback.print_exc()
        domain.Close()
        return 1  # make sure all processes are killed
        
'''
MAIN: Execution starts here
'''
if __name__ == '__main__':
    code = DomainDoTcpCli(sys.argv[1:])
    ExitGraceful(code) #Graceful exit is required for the last line to be printed