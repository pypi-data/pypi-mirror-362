ryry Python Tool
===============================================
The ryry Python Tool is a official tool, you can use it to **Register** device to ryry server, other person can use **ryry Application** assign tasks to you for implementation

Installation
------------

The ryry requires [Python](http://www.python.org/download) 3.10.6 or later.

##### Installing
    pip install ryry-cli

##### Uninstalling
    pip uninstall ryry-cli

Use
------------
##### 1. Running
    $ ryry service start
start a process to wait for the server to issue tasks. **Please do not close it**

Module Developer
------------
    $ ryry widget init

in empty folder, use above command craete a ryry module, structure is like 
    
    [widget folder]
        |-- config.json     //*required, do not change*
        |-- main.py         //*required, do not change* 
        |-- run.py

if other person share widget code to you , you can add widget path in your computer to ryry environment

    $ ryry widget add [path_with_widget_code]

you can modify script and h5 file yourself, then publish to ryry sever 
    
    $ ryry widget publish

get ryry status
    $ ryry services status