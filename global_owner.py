import source.prototype.global_list as gl
import global_user


class GlobalOwner:
    def __init__(self):
        gl.test_list.append('added from owner')
        global_user.GlobalUser()
        print(gl.test_list)


def main():
    go = GlobalOwner()


if __name__ == '__main__':
    main()