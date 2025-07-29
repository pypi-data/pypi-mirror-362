# eoq3utils - Swiss Army knife package for EOQ3

Contains API, CLI and service utils that ease the working with EOQ3. 

Furthermore, installing this will all EOQ3 packages at once, i.e. 
, eoq3
, eoq3conceptsgen
, eoq3pyaccesscontroller
, eoq3pyactions
, eoq3pyecoreutils 
, eoq3pyecoremdb
, eoq3pyecorempl
, eoq3autobahnws
, eoq3tcp.

## Usage

### API

#### Domain Factory

To create and close different kind of domains easily, CreateDomain and CleanUpDOmain can be used. 
The example shows how to create and clean up different types of domains with the same commands.
Parameters are individual.

    from eoq3utils import DOMAIN_TYPES, CreateDomain, CleanUpDomain
	
	PARAMS = []
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.LOCAL                  ,"domainSettings": {}})); #PyecoreMdb
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.LOCALPROCESS           ,"domainSettings": {}})); #DomainToProcessWrapper 
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.MULTITHREAD_DOMAINPOOL ,"domainSettings": {"numberOfDomainWorkers" : 2}})); #DomainPool
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.MULTIPROCESS_DOMAINPOOL,"domainSettings": {"numberOfDomainWorkers" : 2}})); #DomainPool in process
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.TCPCLIENT              ,"domainSettings": {"host": "127.0.0.1", "port": 6141, "startServer": False }})); # TCP client only
	PARAMS.append( ParameterSet(n,{"kindOfDomain" : DOMAIN_TYPES.WSCLIENT               ,"domainSettings": {"host": "127.0.0.1", "port": 5141, "startServer": True }})); # WS client and host (server is also cleaned up automatically with CleanUpDomain)
	
	for p in PARAMS:
	    domain = CreateDomain(p.kindOfDomain, p.domainSettings)
	    #TODO: do something with the domain
	    CleanUpDomain(resource.domain)


### CLI

Modules to interact with files and remote domains such as TCP and WS from the command line.

#### Commands

##### eoq3utils.cli.domaindotcpcli

Send a command to a TCP domain:

    python -m eoq3utils.cli.domaindotcpcli --cmd "GET (/*M2MODELS:l0)" --tcpHost "127.0.0.1" --tcpPort 6141
	
##### eoq3utils.cli.domaindowscli

Send a command to a WebSocket domain:

    python -m eoq3utils.cli.domaindowscli --cmd "GET (/*M2MODELS:l0)" --wsHost "127.0.0.1" --wsPort 5141

#### EOQ files

Uploading and downloading model information to EOQ files.

##### eoq3utils.cli.loadeoqfiletcpcli

Upload an eoq file to a TCP host:

    python -m python -m eoq3utils.cli.loadeoqfiletcpcli --infile "m2model.eoq" --tcpHost "127.0.0.1" --tcpPort 6141

    python -m python -m eoq3utils.cli.loadeoqfiletcpcli --infile "m1model.eoq" --tcpHost "127.0.0.1" --tcpPort 6141


#### eoq3utils.cli.loadeoqfilewscli

Upload eoq files to a WebSocket host:

    python -m python -m eoq3utils.cli.loadeoqfilewscli --infile "m2model.eoq" --wsHost "127.0.0.1" --wsPort 6141
     
    python -m python -m eoq3utils.cli.loadeoqfilewscli --infile "m1model.eoq" --wsHost "127.0.0.1" --wsPort 6141


#### eoq3utils.cli.saveeoqfiletcpcli

Download M2 model as eoq file from TCP host:

    python -m eoq3utils.cli.saveeoqfiletcpcli --outfile "m2model.ecore" --rootobj "(/*MDB/*M2MODELS:0)"  --tcpHost "127.0.0.1" --tcpPort 6141
	
The same for M1 model:

	python -m eoq3utils.cli.saveeoqfiletcpcli --outfile "m1model.ecore" --rootobj "(/*MDB/*M1MODELS:0)"  --tcpHost "127.0.0.1" --tcpPort 6141


#### eoq3utils.cli.saveeoqfilewscli

Download M2 model as eoq file from WebSocket host:

    python -m eoq3utils.cli.saveeoqfilewscli --outfile "m2model.eoq" --rootobj "(/*MDB/*M2MODELS:0)" -savemetamodel 1 --host "127.0.0.1"  --port 5141
	
The same for M1 model:

	python -m eoq3utils.cli.saveeoqfilewscli --outfile "m1model.ecore" --rootobj "(/*MDB/*M1MODELS:0)"  --tcpHost "127.0.0.1" --tcpPort 6141


#### ECORE Files

Uploading, downloading and converting ecore files.

##### eoq3utils.cli.ecorefiletoeoqfilecli

Eoq to ecore file conversion:

    python -m eoq3utils.cli.ecorefiletoeoqfilecli --infile "m2model.ecore" --outfile "m2model.eoq"
    
    python -m eoq3utils.cli.ecorefiletoeoqfilecli --infile "m1model.ecore" --outfile "m1model.eoq" --metafile "m2model.ecore"
	

##### eoq3utils.cli.ecorefiletoeoqfilecli
	
Eoq to ecore file conversion:
   
    python -m eoq3utils.cli.eoqfiletoecorefilecli --infile "m2model.eoq" --outfile "m2model.ecore"
	
    python -m eoq3utils.cli.eoqfiletoecorefilecli --infile "m1model.eoq" --outfile "m1model.eoq" --metafile "m2model.ecore"


##### eoq3utils.cli.saveecorefiletcpcli 

Ecore file from TCP host downloading:

    python -m eoq3utils.cli.saveecorefiletcpcli --outfile "m2model.ecore" --rootobj "(/*MDB/*M2MODELS:0)"  --tcpHost "127.0.0.1" --tcpPort 6141
	

##### eoq3utils.cli.saveecorefilewscli

Ecore file from WebSocket host downloading:

	python -m eoq3utils.cli.saveecorefilewscli --outfile "m1model.xmi" --rootobj "(/*MDB/*M1MODELS:0)"  --metafile "m2model.ecore" -savemetamodel 1 --host "127.0.0.1"  --port 5141
	

##### eoq3utils.cli.loadecorefiletcpcli
	
Ecore file to TCP host uploading:
	
	python -m eoq3utils.cli.loadecorefiletcpcli --infile "m2model.ecore" --tcpHost "127.0.0.1" --tcpPort 6141
	
	python -m eoq3utils.cli.loadecorefiletcpcli --infile "m1model.xmi" --metafile "m2model.ecore" --tcpHost "127.0.0.1" --tcpPort 6141
	

##### eoq3utils.cli.loadecorefilewscli
	
Ecore file to WebSocket host uploading:

    python -m eoq3utils.cli.loadecorefilewscli --infile "m2model.ecore" --wsHost "127.0.0.1" --wsPort 6141

    python -m eoq3utils.cli.loadecorefilewscli --infile "m1model.xmi" --metafile "m2model.ecore" --wsHost "127.0.0.1" --wsPort 6141


### Services

Services to start a domain, MPL or action manager via WebSocket.
Services can be configured using ini files.
Ini files are loaded using the `--config` option.
Ini files can be generated using the `--configout` option.

#### eoq3utils.services.wsdomaincli

Start a server offering a domain via WebSocket:

    python -m eoq3utils.services.wsdomaincli --wsHost "127.0.0.1" --wsPort 6141

Optionally, a TCP server enabled in addition::

    python -m eoq3utils.services.wsdomaincli --wsHost "127.0.0.1" --wsPort 6141 --enableTcp 1 --tcpHost "127.0.0.1" --tcpPort 6141

#### eoq3utils.services.wsmplcli:

Start an MPL service connecting via WebSocket to a domain:

    python -m eoq3utils.services.wsmplcli --workspace "./Workspace" --wsHost "127.0.0.1" --wsPort 6141
	
#### eoq3utils.services.wsactionmanagercli:

Start an action manager service connecting via WebSocket to a domain:

    python -m eoq3utils.services.wsactionmanagercli --wsHost "127.0.0.1" --wsPort 6141

#### eoq3utils.services.wsactionhandlercli:

Start an action handler service connecting via WebSocket to a domain:

    python -m eoq3utils.services.wsactionhandlercli --actionsdir "./Actions" --wsHost "127.0.0.1" --wsPort 6141

#### eoq3utils.services.wsservercli:

Start a WebSocket server including a selection of domain, MPL, action manager and action handler services:

    python -m eoq3utils.services.wsservercli --enableDomain 1 --enableMpl 1 --enableActionManager 0 --enableActionHandler 0

The services are configured by individual ini files, which can be specified using options:

    python -m eoq3utils.services.wsservercli --enableDomain 1 --domainConfig "./wsdomain.ini" --enableMpl 1 --mplConfig "./wsmpl.ini" --enableActionManager 1 --actionManagerConfig "./wsactionmanager.ini" --enableActionHandler 1 --actionHandlerConfig "./wsactionhandler.ini"

## Documentation

For more information see EOQ3 documentation: https://eoq.gitlab.io/doc/eoq3/

## Author

2024 Bjoern Annighoefer
