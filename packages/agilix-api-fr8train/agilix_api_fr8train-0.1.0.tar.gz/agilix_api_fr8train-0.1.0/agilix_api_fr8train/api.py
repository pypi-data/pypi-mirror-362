from agilix.models.connection import Connection
from agilix.factories.api import build_api_connection

from agilix.models.courses import UpdateCourseDefinition, CopyCourseDefinition


class Api:
    _conn: Connection

    def __init__(self):
        self._conn = build_api_connection()

        # PACKAGED MODULAR SCOPES
        self.courses = self.Courses(self._conn)
        self.domains = self.Domains(self._conn)

    @staticmethod
    def get_domain_id(domain_id: str, connection: Connection) -> str:
        return domain_id if domain_id else connection.home_domain_id

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

        def list_domains(
            self,
            domain_id: str = "",
            include_descendant_domains: bool = False,
            limit: int = 100,
        ) -> list:
            response = self._conn.get(
                "listdomains",
                {
                    "domainid": Api.get_domain_id(
                        domain_id=domain_id, connection=self._conn
                    ),
                    "includedescendantdomains": include_descendant_domains,
                    "limit": limit,
                },
            )

            return response.get("response", {}).get("domains", {}).get("domain", [])
