from dataclasses import dataclass, fields

@dataclass(init=False)
class BaseModel:
    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)
