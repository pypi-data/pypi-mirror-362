from metacat.mql import MQLQuery
query_text = "files from mengel:gen_cfg where size > 10 and x.foo == bar"
q = MQLQuery.parse(query_text )
print(repr(q))
