from agilix_api_fr8train.models.users import CreateUserDefinition


def build_create_user_payload(new_user_list: list[CreateUserDefinition]):
    return {"requests": {"user": list(map(lambda x: dict(x), new_user_list))}}
