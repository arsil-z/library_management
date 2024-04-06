from src.library.apis import Circulation, MemberStats


LIBRARY_ROUTES = [
    ('/api/library/circulation', Circulation),
    ('/api/library/member/stats', MemberStats)
]
