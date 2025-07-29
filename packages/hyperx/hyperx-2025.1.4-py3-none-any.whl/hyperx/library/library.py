"""
References the HyperX scripting library.
"""

import os
import errno
from pathlib import Path
from types import ModuleType

from .find import AutoDetectInstallFolder
from ..version import major, minor, revision, __version__


def FindExecutableFolder() -> Path:
    '''
    Returns the path for the Executable folder
    inside the auto-detected HyperX install directory
    '''
    installFolder = AutoDetectInstallFolder()
    libFolder = Path(installFolder) / 'Executable'
    return libFolder

def ReferenceLibrary():
    '''
    Adds references to the C# HyperX scripting library.
    '''
    libFolder = FindExecutableFolder()

    scriptingDll = libFolder / 'HyperX.Scripting.dll'
    typesDll = libFolder / 'HyperX.Types.dll'
    runtimeConfig = libFolder / 'HyperX.Scripting.runtimeconfig.json'

    if not scriptingDll.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), scriptingDll)
        
    if not typesDll.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), typesDll)
        
    if not runtimeConfig.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), runtimeConfig)

    from clr_loader import get_coreclr
    from pythonnet import set_runtime

    runtime = get_coreclr(runtime_config=str(runtimeConfig))
    set_runtime(runtime)

    import clr

    # Allow importing `HyperX.Scripting`
    # import HyperX.Scripting as hxapi
    clr.AddReference(str(scriptingDll))
    clr.AddReference(str(typesDll))

    # Allow C#-compatible types.
    # from System.Collections.Generic import List
    clr.AddReference('System.Collections')
    
    # Enable dashboard features
    clr.AddReference('System.Security.Cryptography.ProtectedData')

def ValidateDatabaseVersion(applicationVersion: str) -> None:
    '''
    Validates the wrapper version against the executing HyperX application.
    Prints warning message to console if these versions do not match
    '''
    versionComponents = applicationVersion.split(".")
    if len(versionComponents) < 3:
        PrintWarning([f'Could not parse HyperX version number',
                      f'to validate against wrapper version.',
                      f'Expected at least 3 period-delimited numbers.',
                      f'Got: {applicationVersion}'])
        return

    # Splitting this up to ignore differences in patch number
    hxMajor = int(versionComponents[0])
    hxMinor = int(versionComponents[1])
    hxRevision = int(versionComponents[2])
    if hxMajor != major or hxMinor != minor or hxRevision != revision:
        PrintWarning([f'Wrapper version ({__version__}) does not match the version of the',
                      f'executing HyperX application ({applicationVersion}).',
                      f'Wrapper installed here:',
                      f'\t{Path(__file__).parent.parent}',
                      f'HyperX API assemblies found here:',
                      f'\t{FindExecutableFolder()}',
                      f'Either install wrapper version {applicationVersion}, or use',
                      f'the {__version__} version of HyperX to run your database.'])

def PrintWarning(innerWarning: list[str]):
    print()
    print("====================================")
    print("WARNING")
    print()
    for line in innerWarning:
        print(line)
    print("====================================")
    print()
    