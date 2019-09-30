# `dependent_property`

A package for defining dependencies between class attributes

```python
from dependent_property import Dependable, dependent_property, dependent_method


class Person:
    name = Dependable()
    
    @dependent_property(name)
    def honorific(self) -> str:
        return 'Professor ' + self.name
        
    @dependent_method(honorific)
    def adjust_honorific(self, kind: str) -> str:
        if kind == 'yell':
            return self.honorific.upper()
        return self.honorific.lower()
```
