import os
import inspect
import importlib


with open("tg/session.py", "w") as f:
    f.write("from . import methods\n")
    f.write("from .types import *\n")
    f.write("import aiohttp\n")
    f.write("\n")
    f.write("\n")
    f.write("class Session:\n")
    f.write("\n    def __init__(self, token: str):\n")
    f.write("        self._session = aiohttp.ClientSession()\n")
    f.write("        object.__setattr__(self._session, 'token', token)\n")
    f.write("\n")

    for file in os.listdir("tg/methods"):
        if file.endswith(".py") and not file.startswith("__") and "BaseMethod.py" != file:
            mod = importlib.import_module(f"tg.methods.{file[:-3]}", package=file[:-3])
            method = getattr(mod, file[:-3])
            name = file[:-3]
            print(name)

            f.write(f"    async def {name}(self,")
            caller = method.__call__
            rdoc = caller.__doc__

            if rdoc is None:
                rdoc = method.__doc__.replace('\n', '\n    ')

            doc = f"        '''{rdoc.replace('\n', '\n        ')}'''\n"

            sig = inspect.signature(caller)

            anns = caller.__annotations__
            rtype = str(anns.pop("return")).split(".")[-1]

            for i in range(rtype.count("]")):
                rtype = "list[" + rtype
            
            if ">" in rtype:
                print(rtype)
                if "<class" in rtype:
                    rtype = rtype.split("'", 1)[1]
                rtype = rtype.split("'")[0]

            args = []

            for aname, ann in anns.items():
                s = "\n"

                ann = _ann = str(ann)
                ann = ann.split(".")[-1]

                if "." in _ann:
                    for i in range(ann.count("]")-1):
                        ann = "list[" + ann
                    if ann.count("]") == 1:
                        ann = "list[" + ann
                
            
                if ">" in ann:
                    if "<class" in ann:
                        ann = ann.split("'", 1)[1]
                    ann = ann.split("'")[0]

                s += f"            {aname}: {ann}"

                # check for default value presence
                param = sig.parameters.get(aname)
                if param.default is not inspect.Parameter.empty:
                    s += " = "
                    s += repr(param.default)
                    args.append(s)
                else:
                    args = [s, *args]
            
            f.write(",".join(args))
            
            f.write(f") -> {rtype}:\n")

            f.write(doc)

            f.write(f"        return await methods.{name}().request(self._session,\n")

            for name, ann in anns.items():
                f.write(f"            {name}={name},\n")
            
            f.write("        )\n\n")
    
    f.write("\n")
