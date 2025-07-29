import agilix_api_fr8train.factories.api as ApiFactory
import agilix_api_fr8train.factories.domain as DomainFactory

from agilix_api_fr8train.models.connection import Connection

from agilix_api_fr8train.models.courses import (
    UpdateCourseDefinition,
    CopyCourseDefinition,
)
from agilix_api_fr8train.models.domains import (
    CreateDomainDefinition,
    ListDomainDefinition,
)


class Api:
    _conn: Connection

    def __init__(self):
        self._conn = ApiFactory.build_api_connection()

        # PACKAGED MODULAR SCOPES
        self.courses = self.Courses(self._conn)
        self.domains = self.Domains(self._conn)
        self.utils = self.Utils(self._conn)

    def get_home_domain_id(self) -> int:
        return self._conn.home_domain_id

    class Courses:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def list_courses(
            self,
            domain_id: str = "",
            include_descendant_domains: bool = False,
            text: str = None,
        ) -> list:
            query_params = {
                "domainid": Api.get_domain_id(
                    domain_id=domain_id, connection=self._conn
                ),
                "includedescendantdomains": include_descendant_domains,
            }

            if text:
                query_params["text"] = text

            response = self._conn.get("listcourses", query_params)

            return response.get("response", {}).get("courses", {}).get("course", [])

        def get_course(self, course_id: str, select: list = []) -> dict:
            params = {"courseid": course_id}

            if select:
                params["select"] = ",".join(select)

            response = self._conn.get("getcourse2", params)

            return response.get("response", {}).get("course", {})

        def copy_courses(self, course_list: list[CopyCourseDefinition]) -> list:
            payload = {"requests": {"course": course_list}}

            response = self._conn.post("copycourses", payload=payload)

            course_responses = list(
                map(
                    lambda x: (
                        x.get("course", {}).get("courseid")
                        if x.get("code") == "OK"
                        else x.get("message", "Generic Error")
                    ),
                    response.get("response", {})
                    .get("responses", {})
                    .get("response", []),
                )
            )

            return course_responses

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

        def list_domains(self, domain: ListDomainDefinition) -> list:
            response = self._conn.get("listdomains", params=dict(domain))

            return response.get("response", {}).get("domains", {}).get("domain", [])

        def create_domains(self, domain_list: list[CreateDomainDefinition]) -> list:
            payload = DomainFactory.build_create_domain_payload(domain_list)

            response = self._conn.post("createdomains", payload=payload)

            return response.get("response", {}).get("responses", {}).get("response", [])

    class Utils:
        _conn: Connection

        def __init__(self, connection: Connection):
            self._conn = connection

        def build_domain_tree(self, top: int, domain_list: list) -> dict:
            hung_on_tree = {}
            domain_tree = {
                "domain_id": top,
                "name": "Home Domain",
                "children": {},
            }

            for domain in domain_list:
                parent_id = int(domain.get("parentid"))

                # FIRST ROW
                if parent_id == top:
                    domain_tree["children"][domain.get("id")] = {
                        "domain_id": domain.get("id"),
                        "name": domain.get("name"),
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
                        )
                    )

            return domain_tree

        def __build_domain_tree_recursive(
            self, _children: dict, _domain: dict, _hung_on_tree: dict
        ) -> tuple:
            # GO THROUGH ALL THE CHILDREN TO MATCH THE DOMAIN WITH THEM AS THE PARENT
            # WE'RE NEXT LEVEL DOWN, SO "CHILDREN" ARE POSSIBLE PARENTS
            for id, child in _children.items():
                # IF THE DOMAIN'S PARENTID IS THIS CHILD'S ID ADD AND RETURN
                if _domain.get("parentid") == id:
                    _children[id]["children"][_domain.get("id")] = {
                        "domain_id": _domain.get("id"),
                        "name": _domain.get("name"),
                        "children": {},
                    }
                    _hung_on_tree[_domain.get("id")] = _domain.get("name")

                    return _children, _hung_on_tree

                # IF THE CHILD HAS CHILDREN NEXT GEN THIS SUCKER
                if len(child["children"].items()) > 0:
                    _children[id]["children"], _hung_on_tree = (
                        self.__build_domain_tree_recursive(
                            child["children"], _domain, _hung_on_tree
                        )
                    )

            return _children, _hung_on_tree
