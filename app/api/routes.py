from flask_restful import Resource
from app.api.user_project_stats import ProjectData, UserProjectStats


class UserStat(Resource):
    def get(self, stat_field, user_id):
        if hasattr(UserProjectStats, stat_field):
            if ProjectData.is_user(user_id):
                return getattr(UserProjectStats(user_id), stat_field)
            else:
                return {'error': "user doesn't exists"}, 410
        return {'error': "method doesn't exists"}, 410