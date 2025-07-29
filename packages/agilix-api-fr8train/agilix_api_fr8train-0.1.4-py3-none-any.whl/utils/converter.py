from agilix_api_fr8train.models.domains import CreateDomainDefinition


def create_domain_list_to_payload(domain_list: list[CreateDomainDefinition]) -> dict:
    return {"requests": {"domain": list(map(lambda x: dict(x), domain_list))}}
