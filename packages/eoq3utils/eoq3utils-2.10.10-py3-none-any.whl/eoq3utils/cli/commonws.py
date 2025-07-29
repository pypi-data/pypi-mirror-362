"""
 Common functions used for Web Socket CLI modules
 Bjoern Annighoefer 2024
"""
from eoq3autobahnws.util.ssl import SelfSignedServerSslContextFactoryArg, SelfSignedServerSslContextFactory, ClientSslContextForSelfSignedServerCertFromFileFactoryArg, ClientSslContextForSelfSignedServerCertFromFileFactory
# type annotations
from typing import Any, Tuple, Callable

def PrepareSslServerContextFactory(args:Any)->Tuple[Any,Any]:
    """Creates SSL context factory and arguments for a server.
    """
    sslContextFactory = None
    sslContextFactoryArgs = None
    if (args.enableSsl):
        sslContextFactory = SelfSignedServerSslContextFactory
        sslContextFactoryArgs = SelfSignedServerSslContextFactoryArg(args.sslCertificatePem, args.sslCertificateKeyPem, args.sslCertificatePassword)
    return sslContextFactory, sslContextFactoryArgs

def PrepareSslClientContextFactory(args:Any)->Tuple[Any,Any]:
    """Creates SSL context factory and arguments for a client.
    """
    sslContextFactory = None
    sslContextFactoryArgs = None
    if (args.enableSsl):
        sslContextFactory = ClientSslContextForSelfSignedServerCertFromFileFactory
        sslContextFactoryArgs = ClientSslContextForSelfSignedServerCertFromFileFactoryArg(args.sslCertificatePem)
    return sslContextFactory, sslContextFactoryArgs