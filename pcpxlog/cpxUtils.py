"""
Save self-defined tools in this file
"""
import os


def create_conf_py_file():
    """
    This function is for package console scripts
    Copy the config demo file to work dir.
    """
    config_demo_py_path = os.path.dirname(os.path.abspath(__file__)) + '/configDemo.py'

    with open(config_demo_py_path, "rb") as f:
        data = f.read()

    with open('./cpxLogConfig.py', 'wb') as f:
        f.write(data)


# ------ Create annotation check_params begin 2019-5-14 ------ #
class CheckAnnotation(object):
    """
    eg:
    @CheckAnnotation.check_params
    def func(params: str) -> str:
        return ""
    func("")
    """

    @classmethod
    def init(cls):
        # todo: update_wrapper可以把属性赋值给被装饰函数上
        from functools import update_wrapper

        return update_wrapper


    @staticmethod
    def check_params(func):
        """
        注解检查(检查函数传入参数&返回值类型)
        :param func: 被装饰方法
        :return:
        """
        def inner(*args, **kwargs):
            rules = func.__annotations__  # 获取参数与返回值的注解

            for name, value in kwargs.items():  # 检查传入的关键字参数类型
                if not isinstance(value, rules[name]):
                    raise RuntimeError('%s want %s, but %s' % (name, rules[name], type(value)))
            back = func(*args, **kwargs)
            if 'return' in rules and not isinstance(back, rules['return']):  # 检查返回值类型
                raise RuntimeError('return want %s, but %s' % (rules['return'], type(back)))

            return back

        return inner


    @classmethod
    def accepts(cls, *types):
        """函数传入参数检查"""
        def check_accepts(f):
            def new_f(*args, **kwds):
                assert len(types) == (len(args) + len(kwds)), \
                    "args cnt %d does not match %d" % (len(args) + len(kwds), len(types))
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), \
                        "arg %r does not match %s" % (a, t)
                return f(*args, **kwds)

            cls.init()(new_f, f)
            return new_f

        return check_accepts


    @classmethod
    def returns(cls, rtype):
        """函数返回值检查"""
        def check_returns(f):
            def new_f(*args, **kwds):
                result = f(*args, **kwds)
                assert isinstance(result, rtype), \
                    "return value %r does not match %s" % (result, rtype)
                return result

            cls.init()(new_f, f)
            return new_f

        return check_returns

# ------ Create annotation check_params end 2019-5-15 ------ #


#############################################
class EmailSender:
    # TODO create a e-mail sender class
    pass
