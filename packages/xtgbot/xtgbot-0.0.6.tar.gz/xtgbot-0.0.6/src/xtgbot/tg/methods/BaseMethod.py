from aiohttp import ClientSession
from dataclasses import is_dataclass
from typing import Any, Dict
from logging import getLogger
from ..types import Message, InaccessibleMessage, MaybeInaccessibleMessage


class obj:
    def __init__(self, d: dict[str, Any]):
        self.__dict__.update(d)


def _to_dict(obj: Any) -> dict[str, Any]:
    if is_dataclass(obj):
        d = {}
        for k, v in obj.to_dict().items():
            if v is None:
                continue
            if k == "from_":
                d["from"] = _to_dict(v)
            else:
                d[k] = _to_dict(v)
        return d
    elif isinstance(obj, list):
        return [_to_dict(v) for v in obj if v is not None]
    elif isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items() if v is not None}
    else:
        return obj


class BaseMethod:
    _session: ClientSession
    _url: str

    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        
    async def request(self, session: ClientSession, **kwargs) -> Any | Dict[str, Any]:
        _url = "https://api.telegram.org/bot" + session.token + "/" + self.__class__.__name__
        self.log.debug(_url)
        
        kwargs = _to_dict(kwargs)
        
        rv = await session.post(_url, json=kwargs)

        self.log.debug(f"Response status: {rv.status}")

        if not (await rv.json())["ok"]:
            self.log.warning(f"Request failed: {(await rv.json())['description']}")
            return {}

        # get return type
        annotations = getattr(self.__call__, '__annotations__', {})
        return_type = annotations.get('return', None)
        
        if return_type is None:
            return await rv.json()["result"]
        
        if is_dataclass(return_type):
            if return_type is MaybeInaccessibleMessage:
                if (await rv.json())["result"]["date"] == 0:
                    return return_type(**(await rv.json())["result"])
                else:
                    return Message(**(await rv.json())["result"])
            else:
                return return_type(**(await rv.json())["result"])
        
        if hasattr(return_type, '__name__'):
            if return_type.__name__ in (
                "list", "List", "tuple", "Tuple", "set", "Set"
            ):
                base_type = getattr(return_type, '__args__', (int))[0]
                
                rrv = []

                for item in (await rv.json())["result"]:
                    if is_dataclass(base_type):
                        try:
                            rrv.append(base_type(**item))
                        except Exception as e:
                            if base_type is MaybeInaccessibleMessage:
                                if item["date"] == 0:
                                    rrv.append(InaccessibleMessage(**item))
                                else:
                                    rrv.append(Message(**item))
                            else:
                                self.log.error(f"Error parsing object {base_type.__name__}: {e}")
                                return (await rv.json())["result"]
                    else:
                        rrv.append(item)
                
                return rrv
    
    async def __call__(self, **kwargs) -> dict[str, Any]:
        return await self.request(**kwargs)
