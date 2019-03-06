# wfAlert-web2py
This is a web version of WFqqbot, tell me if you wanna use this program as a productive Env.
## How to use
1. Download web2py from http://www.web2py.com/
2. Download source code.
3. Drag wfTracker into ../web2py/applications/
4. For windows: click ../web2py/web2py.py|For linux: python ../web2py/web2py.py -i [IP usually 0.0.0.0] -p [PORT]

Note:
if you want to set web2py as a default application, add follow code into ../web2py/rotes.py

routers = dict(
    BASE = dict(
        default_application = "wfTracker",       
        default_controller = "default",
        default_function = "index",      
        )
)

Pay attention on indentation.

Or you can drag rotes.py into ../web2py/ directly.
