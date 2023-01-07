import json


class moderator:
    def __init__(self, ctx, user_id=0):
        self.ctx = ctx
        self.user_id = user_id

    def staffList(self):
        try:
            f = open('config/staff.json', 'r')
            try:
                data = json.load(f)
                return data['users']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def main(self):
        staffList = self.staffList()
        if (str(self.user_id) in staffList['moderator']):
            return True
        return False
