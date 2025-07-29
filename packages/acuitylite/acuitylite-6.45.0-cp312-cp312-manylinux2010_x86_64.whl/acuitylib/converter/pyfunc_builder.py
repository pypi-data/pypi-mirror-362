import functools
import traceback

def function_builder(function_str):
    global_variables = dict(globals())
    exec(function_str)
    global_variables2 = dict(globals())
    local_variables = dict(locals())

    function_count = len([1 for x in local_variables if callable(local_variables[x])])
    if function_count == 0:
        local_variables = {x: global_variables2[x]  for x in global_variables2 if x not in global_variables}
        function_count = len([1 for x in local_variables if callable(local_variables[x])])

    if function_count != 1:
        raise ValueError('{} functions found! only 1 function is allowed'.format(function_count))
    for key in local_variables:
        if callable(local_variables[key]):
            rule_func_additional_args = local_variables.get('__rule_func_additional_args', {})
            return functools.partial(local_variables[key], **rule_func_additional_args)

def pyfunc_call(self, func, node, tensor):
    func_str = func
    func_str_line_number = func

    if type(func) is list:
        func_str = '\n'.join(func)
        func_str_line_number = '\n'.join(['{:3d} {}'.format(i + 1, line) for i, line in enumerate(func)])
    try:
        return function_builder(func_str)(self, node, tensor)
    except Exception as e:
        print('pyfunc exception: {}\n{}\n{}'.format(e, traceback.format_exc(), func_str_line_number))
        raise e
