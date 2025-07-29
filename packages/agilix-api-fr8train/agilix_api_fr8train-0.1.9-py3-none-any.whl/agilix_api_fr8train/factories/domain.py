from agilix_api_fr8train.models.domains import CreateDomainDefinition


def build_create_domain_payload(new_domain_list: list[CreateDomainDefinition]) -> dict:
    return {"requests": {"domain": list(map(lambda x: dict(x), new_domain_list))}}
