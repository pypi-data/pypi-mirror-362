"""
Takes one or more files with eoq content and uploads it to a websocket domain.
2024 Bjoern Annighoefer
"""
from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoq3version
from eoq3.command import Get
from eoq3.serializer import TextSerializer
from eoq3.util.eoqfile import SaveEoqFile
from eoq3.util import GenerateSessionId
# web socket imports
from eoq3autobahnws import __version__ as eoq3autobahnwsVersion
from eoq3autobahnws.autobahnwsdomainclient import AutobahnWsDomainClient
# eoq cli commons
from .common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, CliArgument, LogginIfDesired, PrintCliArgumentValues, ExitGraceful
from .commonws import PrepareSslClientContextFactory
# external imports
import argparse
import sys
import traceback
from typing import List, Any

MODULE_NAME = "eoq3utils.cli.saveeoqfilewscli"

def LoadEoqFileWsCli(argv:List[Any])->int:
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'outfile',
        'rootobj',
        'connectTimeout',
        'remoteFrmTxSerializer',
        'remoteCmdTxSerializer',
        'remoteFrmRxSerializer',
        'remoteCmdRxSerializers',
        'wsHost',
        'wsPort',
        'user',
        'password',
        'enableSsl',  # currently not implemented
        'sslCertificatePem',
        'fileSerializer',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
    ])
    # modify predefined arguments
    argDefs['outfile'     ].Set({'default': 'model.eoq3','description':'The file to be downloaded'})
    # use argparse to parse the command line arguments
    parser = argparse.ArgumentParser(description='Reads an Mdb, M1 or M2 model and stores to an eoq file.')
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key)
    # read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version, {"eoq3":eoq3version,"eoq3autobahnwsVersion":eoq3autobahnwsVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args, argDefs, args.printArgs)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    # check the query syntax
    qrySerializer = TextSerializer()
    rootQry = qrySerializer.DesQry(args.rootobj)
    # create client
    sslContextFactory, sslContextFactoryArgs = PrepareSslClientContextFactory(args)
    domain = AutobahnWsDomainClient(args.wsHost,args.wsPort,sslContextFactory=sslContextFactory,sslFactoryArgs=sslContextFactoryArgs,config=config)
    try:
        # login if desired
        sessionId = LogginIfDesired(domain, args.user, args.password)
        # obtain the root obj
        rootObj = domain.Do( Get(rootQry), sessionId)
        SaveEoqFile(args.outfile,rootObj,domain,sessionId)
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
    code = LoadEoqFileWsCli(sys.argv[1:])
    ExitGraceful(code)  # Graceful exit is required for the last line to be printed