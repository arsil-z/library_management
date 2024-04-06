from flask import request
from flask.views import MethodView

from src.library.utils import circulation_helper, member_stats_helper


class Circulation(MethodView):
    def post(self):
        try:
            request_data = request.get_json()
        except Exception as err:
            return {'error': 'Request data missing'}

        if not request_data:
            return {'error': 'Request data missing'}

        return circulation_helper(request_data)


class MemberStats(MethodView):
    def get(self):
        member_id = request.args.get('member_id')
        if not member_id:
            return {'error': 'member id not present'}

        return member_stats_helper(member_id)
