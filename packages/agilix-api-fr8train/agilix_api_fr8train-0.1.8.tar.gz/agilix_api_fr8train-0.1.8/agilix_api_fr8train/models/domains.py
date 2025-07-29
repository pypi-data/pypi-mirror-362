class CreateDomainDefinition:
    name: str
    userspace: str
    parent_id: int
    reference: str

    def __init__(self,
                 name: str,
                 userspace: str,
                 parent_id: int,
                 reference: str = ''):
        self.name = name
        self.userspace = userspace
        self.parent_id = parent_id
        self.reference = reference

    def __iter__(self):
        yield "name", self.name
        yield "userspace", self.userspace
        yield "parentid", self.parent_id
        yield "reference", self.reference