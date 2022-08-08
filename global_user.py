import source.prototype.global_list as gl


class GlobalUser:
    def __init__(self):
        gl.test_list.append('added from user')
