"""
Can be used to load an ecore file to a TCP domain.
2024 Bjoern Annighoefer
"""
from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoq3version
from eoq3pyecoreutils import __version__ as eoq3pyecoreutilsVersion
from eoq3pyecoreutils.loadecorefile import LoadEcoreFile
# web socket imports
from eoq3autobahnws import __version__ as eoq3autobahnwsVersion
from eoq3autobahnws.autobahnwsdomainclient import AutobahnWsDomainClient
# eoq cli commons
from .common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, LogginIfDesired, PrintCliArgumentValues, ExitGraceful
from .commonpyecore import ArgparseToEcoreConversionOptions
from .commonws import PrepareSslClientContextFactory
# external imports
import argparse
import sys
import traceback
from typing import List, Any

MODULE_NAME = "eoq3utils.cli.loadecorefilewscli"

def LoadEcoreFileWsCli(argv:List[Any])->int:
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'infile',
        'metafile',
        'm1modelname',
        'loadmetamodel',
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
        'checksyntax',
        'fileSerializer',
        'printExpectedExceptionTraces',
        'printUnexpectedExceptionTraces',
        'subpackages',
        'enums',
        'documentation',
        'constraints',
        'permissions',
        'muteupdate',
        'maxstrlen',
        'maxstrtrunsym',
        'translatechars',
        'translatetable',
        'packageidfeat',
    ])
    # modify predefined arguments
    argDefs['infile'     ].Set({'default': 'model.ecore','description':'The ecore M1 or M2 file to be uploaded'})
    argDefs['metafile'   ].Set({'default': None         ,'description':'The M2 .ecore file. Only necessary if infile is an M1 model.'})
    argDefs['m1modelname'].Set({'default':'m1model'     ,'description':'M1 model name is loaded. Only if an M1 model is loaded.'})
    # use argparse to parse the command line arguments
    parser = argparse.ArgumentParser(description='Loads an ecore file into a TCP domain.')
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key)
    # read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version, {"eoq3":eoq3version,"eoq3pyecoreutils":eoq3pyecoreutilsVersion, "eoq3autobahnws":eoq3autobahnwsVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args, argDefs, args.printArgs)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    # create conversions options
    options = ArgparseToEcoreConversionOptions(args)
    # create client
    sslContextFactory, sslContextFactoryArgs = PrepareSslClientContextFactory(args)
    domain = AutobahnWsDomainClient(args.wsHost,args.wsPort,sslContextFactory=sslContextFactory,sslFactoryArgs=sslContextFactoryArgs,config=config)
    try:
        #login if desired
        sessionId = LogginIfDesired(domain,args.user,args.password)
        LoadEcoreFile(args.infile,domain,sessionId,args.metafile,args.checksyntax,args.loadmetamodel,args.m1modelname,options,config)
        print('Upload complete.')
    finally:
        #close domain
        domain.Close()
        
'''
MAIN: Execution starts here
'''
if __name__ == '__main__':
    code = LoadEcoreFileWsCli(sys.argv[1:])
    ExitGraceful(code) #Graceful exit is required for the last line to be printed