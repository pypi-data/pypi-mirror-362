from python_sdk_remote.our_object import OurObject

ENTITY_NAME = "FieldLocal"


class FieldLocal(OurObject):

    # TODO Add all FieldLocal
    FieldLocal = {
        "FieldLocal_id",
        "display_as",
    }

    def __init__(self, entity_name=ENTITY_NAME, **kwargs):
        super().__init__(entity_name, **kwargs)

    # Mandatory pure virtual method from OurObject
    def get_name(self):
        print(f"{ENTITY_NAME} get_name() self.FieldLocal.display_as={self.FieldLocal.display_as}")
        return self.FieldLocal.display_as
