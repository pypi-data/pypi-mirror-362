class UpdateCourseDefinition:
    course_id: str
    domain_id: str
    title: str
    reference: str

    def __init__(self,
                 course_id: str,
                 domain_id: str,
                 title: str,
                 reference: str):
        self.course_id = course_id
        self.domain_id = domain_id
        self.title = title
        self.reference = reference


    def __iter__(self):
        yield "courseid", self.course_id
        yield "domainid", self.domain_id
        yield "title", self.title
        yield "reference", self.reference


class CopyCourseDefinition:
    course_id: str
    domain_id: str
    action: str
    reference: str
    status: int

    def __init__(self,
                 course_id: str,
                 domain_id: str,
                 action: str = 'StaticCopy',
                 reference: str = '',
                 status: int = 0):
        self.course_id = course_id
        self.domain_id = domain_id
        self.action = action
        self.reference = reference
        self.status = status