
from aimmspy.model.enums.me_identifier_types import IdentifierType
from aimmspy.model.enums.me_attribute_types import AttributeType
from aimmspy.model.identifiers.identifier import Identifier

class Index(Identifier):
    def __init__(self, parent_me_handle, name, range= None, **kwargs):
        
        super().__init__(
            name=name,
            parent_me_handle=parent_me_handle,
            identifier_type=IdentifierType.INDEX.value,
            **kwargs
        )
        
        self.range = None
        self.me_handle = kwargs.get("model_reflection_handle") # type: ignore

     
    def fill_range(self):
        range_str = self.project.aimms_api.get_attribute(self.me_handle, AttributeType.RANGE.value)
        
        if range_str == "":
            return
        
        # get the handle of the range
        identifier_info = self.project.find_identifier_info(range_str, False)
        # find in the reflected identifiers the range with corresponding handle
        for identifier in self.project.reflected_identifiers:
            if identifier.me_handle == identifier_info.me_handle:
                self.range = identifier
                break
        
    def __str__(self):
        return self.name