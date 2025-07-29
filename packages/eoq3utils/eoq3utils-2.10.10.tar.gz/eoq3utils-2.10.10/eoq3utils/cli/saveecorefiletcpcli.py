"""
Downloads content from TCP domain and saves to an ecore file.
2024 Bjoern Annighoefer
"""
from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoq3version
from eoq3.command import Get
from eoq3.serializer import TextSerializer
from eoq3pyecoreutils import __version__ as eoq3pyecoreutilsVersion
from eoq3pyecoreutils.saveecorefile import SaveEcoreFile
# tcp imports
from eoq3tcp import __version__ as eoq3tcpVersion
from eoq3tcp.tcpdomainclient import TcpDomainClient
# eoq cli commons
from .common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, LogginIfDesired, PrintCliArgumentValues, ExitGraceful
from .commonpyecore import ArgparseToEcoreConversionOptions
# external imports
import argparse
import sys
import traceback
from typing import List, Any

MODULE_NAME = "eoq3utils.cli.saveecorefiletcpcli"

def LoadEcoreFileTcpCli(argv:List[Any])->int:
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'outfile',
        'metafile',
        'rootobj',
        'savemetamodel',
        'connectTimeout',
        'remoteFrmTxSerializer',
        'remoteCmdTxSerializer',
        'remoteFrmRxSerializer',
        'remoteCmdRxSerializers',
        'tcpHost',
        'tcpPort',
        'user',
        'password',
        'enableSsl',  # currently not implemented
        'sslCertificatePem',
        'fileSerializer',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
    ])
    # modify predefined arguments
    argDefs['outfile'     ].Set({'default': 'model.ecore','description':'The file to be downloaded'})
    argDefs['metafile'    ].Set({'default': None         ,'description':'The M2 .ecore file. Only if saving an M1 model. If savemetamodel 1, this is the M2 .ecore file created. Otherwise, it is the input path. In this case, the local M2 model must be identical to the one in the MDB.'})
    # use argparse to parse the command line arguments
    parser = argparse.ArgumentParser(description='Saves TCP domain content to ecore file.')
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key)
    # read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version, {"eoq3":eoq3version,"eoq3pyecoreutils":eoq3pyecoreutilsVersion,"eoq3tcp":eoq3tcpVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args, argDefs, args.printArgs)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    # set conversions options
    options = ArgparseToEcoreConversionOptions(args)
    # check the query syntax
    qrySerializer = TextSerializer()
    rootQry = qrySerializer.DesQry(args.rootobj)
    # create client
    # TODO: SSL support
    domain = TcpDomainClient(args.tcpHost, args.tcpPort, 2 ** 20, b'\x00', config)
    try:
        # login if desired
        sessionId = LogginIfDesired(domain, args.user, args.password)
        # obtain the root obj
        rootObj = domain.Do( Get(rootQry), sessionId)
        SaveEcoreFile(args.outfile,rootObj,domain,sessionId,args.metafile,args.savemetamodel,options)
        print('Download complete.')
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
    code = LoadEcoreFileTcpCli(sys.argv[1:])
    ExitGraceful(code)  # Graceful exit is required for the last line to be printed