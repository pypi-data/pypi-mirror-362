import agilix_api_fr8train.factories.api as ApiFactory
import agilix_api_fr8train.factories.domain as DomainFactory
import agilix_api_fr8train.factories.user as UserFactory
import agilix_api_fr8train.factories.course as CourseFactory

from agilix_api_fr8train.models.connection import Connection

from agilix_api_fr8train.models.courses import (
    UpdateCourseDefinition,
    CopyCourseDefinition,
    ListCourseDefinition,
)
from agilix_api_fr8train.models.domains import (
    CreateDomainDefinition,
    ListDomainDefinition,
    UpdateDomainDefinition,
)
from agilix_api_fr8train.models.users import ListUserDefinition, CreateUserDefinition


class Api:
    _conn: Connection

    def __init__(self):
        self._conn = ApiFactory.build_api_connection()

        # PACKAGED MODULAR SCOPES
        self.courses = self.Courses(self._conn)
        self.domains = self.Domains(self._conn)
        self.users = self.Users(self._conn)
        self.rights = self.Rights(self._conn)
        self.utils = self.Utils(self._conn)

    def get_home_domain_id(self) -> int:
        return self._conn.home_domain_id

    class Courses:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def list_courses(self, list_courses: ListCourseDefinition) -> list:
            response = self._conn.get("listcourses", params=dict(list_courses))

            return response.get("response", {}).get("courses", {}).get("course", [])

        def get_course(self, course_id: str, select: list = []) -> dict:
            params = {"courseid": course_id}

            if select:
                params["select"] = ",".join(select)

            response = self._conn.get("getcourse2", params)

            return response.get("response", {}).get("course", {})

        def copy_courses(self, course_list: list[CopyCourseDefinition]):  # -> list:
            payload = CourseFactory.build_copy_course_payload(course_list)

            response = self._conn.post("copycourses", payload=payload)

            return response.get("response", {}).get("responses", {}).get("response", [])

        def update_courses(self, course_list: list[UpdateCourseDefinition]) -> list:
            payload = {"requests": {"course": course_list}}

            response = self._conn.post("updatecourses", payload=payload)

            course_responses = list(
                map(
                    lambda x: (
                        x.get("code") == "OK"
                        if x.get("code") == "OK"
                        else x.get("message", "Generic Error")
                    ),
                    response.get("response", {})
                    .get("responses", {})
                    .get("response", []),
                )
            )

            return course_responses

        def delete_courses(self, course_id: list):
            payload = {
                "requests": {"course": list(map(lambda x: {"courseid": x}, course_id))}
            }

            response = self._conn.post("deletecourses", payload=payload)

            course_responses = list(
                map(
                    lambda x: (
                        x.get("code") == "OK"
                        if x.get("code") == "OK"
                        else x.get("message", "Generic Error")
                    ),
                    response.get("response", {})
                    .get("responses", {})
                    .get("response", []),
                )
            )

            return course_responses

    class Domains:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def list_domains(self, list_domain: ListDomainDefinition) -> list:
            response = self._conn.get("listdomains", params=dict(list_domain))

            return response.get("response", {}).get("domains", {}).get("domain", [])

        def create_domains(self, domain_list: list[CreateDomainDefinition]) -> list:
            payload = DomainFactory.build_create_domain_payload(domain_list)

            response = self._conn.post("createdomains", payload=payload)

            return response.get("response", {}).get("responses", {}).get("response", [])

        def update_domains(self, domain_list: list[UpdateDomainDefinition]) -> list:
            payload = DomainFactory.build_update_domain_payload(domain_list)

            response = self._conn.post("updatedomains", payload=payload)

            return response.get("response", {}).get("responses", {}).get("response", [])

    class Users:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def list_users(self, list_users: ListUserDefinition) -> list:
            response = self._conn.get("listusers", params=dict(list_users))

            return response.get("response", {}).get("users", {}).get("user", [])

        def create_users(self, user_list: list[CreateUserDefinition]) -> list:
            payload = UserFactory.build_create_user_payload(user_list)

            response = self._conn.post("createusers2", payload=payload)

            return response.get("response", {}).get("responses", {}).get("response", [])

    class Rights:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def list_roles(self, domain_id: int) -> list:
            response = self._conn.get("listroles", params={"domainid": domain_id})

            return response.get("response", {}).get("roles", {}).get("role", [])

    class Utils:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def build_domain_tree(self, top: int, domain_list: list) -> dict:
            hung_on_tree = {}
            domain_tree = {
                "domain_id": top,
                "name": "Home Domain",
                "userspace": None,
                "children": {},
            }

            for domain in domain_list:
                parent_id = int(domain.get("parentid"))

                # FIRST ROW
                if parent_id == top:
                    domain_tree["children"][domain.get("id")] = {
                        "domain_id": domain.get("id"),
                        "name": domain.get("name"),
                        "userspace": domain.get("userspace"),
                        "children": {},
                    }
                    hung_on_tree[domain.get("id")] = domain.get("name")
                    continue

            while len(hung_on_tree.items()) < len(domain_list):
                for domain in domain_list:
                    domain_tree["children"], hung_on_tree = (
                        self.__build_domain_tree_recursive(
                            _children=domain_tree["children"],
                            _domain=domain,
                            _hung_on_tree=hung_on_tree,
                            finish_total=len(domain_list),
                        )
                    )

                    if len(hung_on_tree.items()) == len(domain_list):
                        break

            return domain_tree

        def __build_domain_tree_recursive(
            self, _children: dict, _domain: dict, _hung_on_tree: dict, finish_total: int
        ) -> tuple:
            # GO THROUGH ALL THE CHILDREN TO MATCH THE DOMAIN WITH THEM AS THE PARENT
            # WE'RE NEXT LEVEL DOWN, SO "CHILDREN" ARE POSSIBLE PARENTS
            domain_parent_id = _domain.get("parentid")
            if domain_parent_id in _children:
                # IF THE DOMAIN'S PARENTID IS THIS CHILD'S ID ADD AND RETURN
                _children[domain_parent_id]["children"][_domain.get("id")] = {
                    "domain_id": _domain.get("id"),
                    "name": _domain.get("name"),
                    "userspace": _domain.get("userspace"),
                    "children": {},
                }
                _hung_on_tree[_domain.get("id")] = _domain.get("name")

                return _children, _hung_on_tree
            else:
                for id, child in _children.items():
                    # IF THE CHILD HAS CHILDREN NEXT GEN THIS SUCKER
                    if len(child["children"].items()) > 0:
                        _children[id]["children"], _hung_on_tree = (
                            self.__build_domain_tree_recursive(
                                child["children"], _domain, _hung_on_tree, finish_total
                            )
                        )

                        if len(_hung_on_tree.items()) == finish_total:
                            return _children, _hung_on_tree

            return _children, _hung_on_tree
