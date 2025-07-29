"""
 Common functions used for pyecore CLI modules
 Bjoern Annighoefer 2024
"""
from eoq3pyecoreutils.ecoreconversionoptions import EcoreConversionOptions
from .common import RegisterCliArgument

def ArgparseToEcoreConversionOptions(args)->EcoreConversionOptions:
    """Converts argparse arguments to EcoreConversionOptions
    """
    options = EcoreConversionOptions()
    if(hasattr(args,'subpackages')):
        options.includeSubpackes = bool(args.subpackages)
    if(hasattr(args,'enums')):
        options.includeEnums = bool(args.enums)
    if(hasattr(args,'documentation')):
        options.includeDocumentation = bool(args.documentation)
    if(hasattr(args,'constraints')):
        options.includeConstraints = bool(args.constraints)
    if(hasattr(args,'permissions')):
        options.includePermissions = bool(args.permissions)
    if(hasattr(args,'muteupdate')):
        options.muteUpdate = bool(args.muteupdate)
    if(hasattr(args,'maxstrlen')):
        options.maxStrLen = args.maxstrlen
    if(hasattr(args,'maxstrtrunsym')):
        options.maxStrTruncationSymbol = args.maxstrtrunsym
    if(hasattr(args,'translatechars') and hasattr(args,'translatetable')):
        options.translateChars = bool(args.translatechars)
        if(args.translatechars):
            if(len(args.translatetable)%2 != 0 ):
                raise ValueError("translatetable must have even length.")
            #create tuples from char pairs
            options.translateTable = [(args.translatetable[i],args.translatetable[i+1]) for i in range(len(args.translatetable)-1)]
    if(hasattr(args,'packageidfeat')):
        options.packageIdFeature = args.packageidfeat
    return options

# ecore cli spedific arguments
RegisterCliArgument('loadmetamodel',  'Load meta-model?',      typ=int,         default=0,             description='Load also the M2. Only if an M1 is loaded.')
RegisterCliArgument('savemetamodel',  'Save meta-model?',      typ=int,         default=0,             description='Save also the M2 model. Only if an M1 model is saved.)')
# ecore conversion options
RegisterCliArgument('subpackages',    'Incl. subpackages?',    typ=int,         default=1,             description='Conversion options: include subpackages')
RegisterCliArgument('enums',          'Incl. enums?',          typ=int,         default=1,             description='Conversion options: include enums')
RegisterCliArgument('documentation',  'Incl. documentation?',  typ=int,         default=1,             description='Conversion options: include documentation')
RegisterCliArgument('constraints',    'Incl. constraints?',    typ=int,         default=0,             description='Conversion options: include constraints')
RegisterCliArgument('permissions',    'Incl. permissions?',    typ=int,         default=0,             description='Conversion options: include permissions')
RegisterCliArgument('muteupdate',     'Mute update cmds?',     typ=int,         default=0,             description='If 1, UPD commands are muted')
RegisterCliArgument('maxstrlen',      'Max str length',        typ=int,         default=-1,            description='Limit the length of strings, -1=infinite')
RegisterCliArgument('maxstrtrunsym',  'Str. truncation sym',   typ=str,         default='...',         description='Is added at the end of the string if truncated')
RegisterCliArgument('translatechars', 'Translate chars?',      typ=int,         default=0,             description='If 1, given characters in strings are replaced')
RegisterCliArgument('translatetable', 'Translate table',       typ=str,         default=" _:_\n#-%\r_\t_,_/_(_)_[_]_{_}_;_\\_=_", description='A sequence of chars to be replaced. Each two consecutive chars are a pair of search and replacement char.')
RegisterCliArgument('packageidfeat',  'Package ID feature n.', typ=str,         default='name',        description='eFeature name used as package ID in EOQ. Can be name or nsURI')
