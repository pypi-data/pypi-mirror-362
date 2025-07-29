# eoq3pyecorempl - A model persistance layer for EOQ3 based on pyecore 

This is a model persitancy layer (MPL) based on pyecore. 
This MPL behaves similar to a WorkspaceDomain in EOQ2. 
A workspace directory containing M2 and M1 models in 

* <modelname>.ecore and <user model>.<modelname>
* *.xml

format is parsed and uploaded to a domain as a workspace model.
		
## Usage

Imports:

    from eoq3pyecorempl import PyEcoreWorkspaceMpl

Init and connect the MPL:

    mpl = PyEcoreWorkspaceMpl(WORKSPACE_PATH)
	
Load the workspace directory:

	mpl.Load()
	
Connect to the domain and upload the workspace model:

    mpl.Connect(domain)
	
	
Accessing a M2 model:

    res = domain.Do( Get(Cls("workspacemdbmodel__Resource").Sel(Pth("name").Equ("oaam.ecore"))) )
		
Accessing a M2 model:

	res = domain.Do( Get(Cls("workspacemdbmodel__Resource").Sel(Pth("name").Equ("MinimalFlightControl.oaam"))) )
	
Accessing the model content:

    res = domain.Do( Get(Cls("workspacemdbmodel__Resource").Sel(Pth("name").Equ("MinimalFlightControl.oaam")).Idx(0).Pth("content")) )
	
See also pyeoq/Test/Eoq3/test_pyecorempl.py for working code.

## Workspace

A valid WORKSPACE_PATH could look like

* Meta

  * oaam.ecore

* MinimalFlightControl.oaam
* Library.xml

Subfolders are not mandatory.

Such a workspace directory can be found at pyeoq/Test/Eoq3/testdata/Workspace.

## Documentation

For more information see EOQ3 documentation: https://eoq.gitlab.io/doc/eoq3/

## Author

2024 Bjoern Annighoefer