"""
Can be used to convert an ecore file to an eoq file.
2024 Bjoern Annighoefer
"""
from .. import __version__ as version
# eoq3 imports
from eoq3 import __version__ as eoq3version
from eoq3pyecoreutils import __version__ as eoq3pyecoreutilsVersion
from eoq3pyecoreutils.ecorefiletoeoqfile import EcoreFileToEoqFile
# eoq cli commons
from .common import PrintCliHeader, GetCliPredefinedArguments, ArgparseToEoqConfig, PrintCliArgumentValues, ExitGraceful
from .commonpyecore import ArgparseToEcoreConversionOptions
# external imports
import argparse
import sys
import traceback
from typing import List, Any

MODULE_NAME = "eoq3utils.cli.ecorefiletoeoqfilecli"

def EcoreFileToEoqFileCli(argv:List[Any])->int:
    # get predefined commandline arguments
    argDefs = GetCliPredefinedArguments([
        'printHeader',
        'printArgs',
        'infile',
        'outfile',
        'metafile',
        'm1modelname',
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
    argDefs['infile'     ].Set({'default': 'model.ecore','description':'The ecore M1 or M2 file to be converted'})
    argDefs['outfile'    ].Set({'default': 'model.eoq3' ,'description':'The output eoq file'})
    argDefs['metafile'   ].Set({'default': None         ,'description':'The M2 .ecore file. Only necessary if infile is an M1 model.'})
    argDefs['m1modelname'].Set({'default':'m1model'     ,'description':'M1 model name is loaded. Only if an M1 model is loaded.'})
    # use argparse to parse the command line arguments
    parser = argparse.ArgumentParser(description='Converts and ecore file to an eoq file.')
    for a in argDefs.values():
        parser.add_argument('--' + a.key, metavar=a.key, type=a.typ, default=a.default, help=a.description, dest=a.key)
    # read the arguments
    args = parser.parse_args(argv)
    # print header
    PrintCliHeader(MODULE_NAME, version, {"eoq3":eoq3version,"eoq3pyecoreutils":eoq3pyecoreutilsVersion}, shallPrint=args.printHeader)
    # print args
    PrintCliArgumentValues(args, argDefs, args.printArgs)
    # create an eoq3 config structure
    config = ArgparseToEoqConfig(args)
    # set conversions options
    options = ArgparseToEcoreConversionOptions(args)
    try:
        EcoreFileToEoqFile(args.infile,args.outfile,args.metafile,args.m1modelname,args.checksyntax,options,config)
        print("Conversion complete.")
        return 0
    except Exception as e:
        print("ERROR: %s" % (str(e)))
        traceback.print_exc()
        return 1
        
    
'''
MAIN: Execution starts here
'''
if __name__ == '__main__':
    code = EcoreFileToEoqFileCli(sys.argv[1:])
    ExitGraceful(code) #Graceful exit is required for the last line to be printed