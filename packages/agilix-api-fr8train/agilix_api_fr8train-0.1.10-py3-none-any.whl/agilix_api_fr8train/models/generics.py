class ListDefinition:
    domain_id: int
    include_descendant_domains: bool
    limit: int
    show: str
    text: str

    def __init__(
        self,
        domain_id: int,
        include_descendant_domains: bool = False,
        limit: int = 100,
        show: str = "current",
        text: str = "",
    ):
        self.domain_id = domain_id
        self.include_descendant_domains = include_descendant_domains
        self.limit = limit
        self.show = show
        self.text = text

    def __iter__(self):
        yield "domainid", self.domain_id
        yield "includedescendantdomains", self.include_descendant_domains
        yield "limit", self.limit
        yield "show", self.show
        yield "text", self.text
