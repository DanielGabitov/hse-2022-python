import ast
import graphviz

color_map = {
    'Module': '#15D6DC',
    'FunctionDef': '#003BC6М',
    'Arguments': '#FD8F00',
    'Arg': '#85D079',
    'Body': '#FD0000',
    'Assign': '#0FA938',
    'If': '#788491',
    'Comparator': '#9AB7D8',
    'Exception': '#A60616',
    'Return': '#FF00E6',
    'Value': '#FDFD00',
    'For': '#0C0566',
    'Call': '#FD00FD',
    'Expr': '#1AB224',
    'List': '#92681D',
    'Constant': '#E9C9C9',
    'Name': '#C9E9E8',
    'Compare': '#735A6F',
    'Attribute': '#0A6213',
    'BinOp': '#6B3DA8',
    'Subscript': '#15D6DC',
    'Slice': '#1AB224',
    'Add': '#B399D5',
    'Sub': '#A60616',
    'Index': '#DB69DF'
}

comparators = {
        ast.Lt: '<',
        ast.Gt: '>',
        ast.Eq: '==',
        ast.GtE: '>=',
        ast.LtE: '<=',
        ast.NotEq: '!='
}


class AstTreeBuilder:
    def __init__(self):
        self.G = graphviz.Digraph()
        self.node_cnt = 0

    def __get_next_cnt__(self):
        res = str(self.node_cnt)
        self.node_cnt += 1
        return res

    def __get_cnt__(self):
        return str(self.node_cnt)

    def build(self, ast_object):
        if type(ast_object) == ast.Module:
            self.build_module_node(ast_object)
        elif type(ast_object) == ast.FunctionDef:
            self.build_function_def_node(ast_object)
        elif type(ast_object) == ast.arg:
            self.build_arg_node(ast_object)
        elif type(ast_object) == ast.Assign:
            self.build_assign_node(ast_object)
        elif type(ast_object) == ast.If:
            self.build_if_node(ast_object)
        elif type(ast_object) == ast.Raise:
            self.build_raise_node(ast_object)
        elif type(ast_object) == ast.Return:
            self.build_return_node(ast_object)
        elif type(ast_object) == ast.Call:
            self.build_call_node(ast_object)
        elif type(ast_object) == ast.For:
            self.build_for_node(ast_object)
        elif type(ast_object) == ast.Constant:
            self.build_constant_node(ast_object)
        elif type(ast_object) == ast.Name:
            self.build_name_node(ast_object)
        elif type(ast_object) == ast.Expr:
            self.build_expr_node(ast_object)
        elif type(ast_object) == ast.List:
            self.build_list_node(ast_object)
        elif type(ast_object) == ast.Attribute:
            self.build_attribute_node(ast_object)
        elif type(ast_object) == ast.BinOp:
            self.build_bin_op_node(ast_object)
        elif type(ast_object) == ast.Add:
            self.build_add_node(ast_object)
        elif type(ast_object) == ast.Sub:
            self.build_sub_node(ast_object)
        elif type(ast_object) == ast.Subscript:
            self.build_subscript_node(ast_object)
        elif type(ast_object) == ast.Index:
            self.build_index_node(ast_object)
        else:
            print(type(ast_object))
            return

    def build_sub_node(self, ast_object: ast.Sub):
        self.G.node(self.__get_next_cnt__(), label=f'Sub', style='filled', shape='rectangle',
                    color=color_map['Sub'])

    def build_add_node(self, ast_object: ast.Add):
        self.G.node(self.__get_next_cnt__(), label=f'Add', style='filled', shape='rectangle',
                    color=color_map['Add'])

    def build_index_node(self, ast_object: ast.Index):
        index_node = self.__get_next_cnt__()
        self.G.node(index_node, label=f'Index', style='filled', shape='rectangle', color=color_map['Index'])

        value_node = self.__get_cnt__()
        self.build(ast_object.value)
        self.G.edge(index_node, value_node)

    def build_slice_node(self, ast_object: ast.Slice):
        slice_node = self.__get_next_cnt__()
        self.G.node(slice_node, label=f'Slice', style='filled', shape='rectangle', color=color_map['Slice'])

        upper_node = self.__get_cnt__()
        self.build(ast_object.upper)
        self.G.edge(slice_node, upper_node)

        step_node = self.__get_cnt__()
        self.build(ast_object.step)
        self.G.edge(slice_node, step_node)

    def build_subscript_node(self, ast_object: ast.Subscript):
        subscript_node = self.__get_next_cnt__()
        self.G.node(subscript_node, label=f'Subscript', style='filled', shape='rectangle', color=color_map['Subscript'])

        value_node = self.__get_cnt__()
        self.build(ast_object.value)
        self.G.edge(subscript_node, value_node)

        slice_node = self.__get_cnt__()
        self.build(ast_object.slice)
        self.G.edge(subscript_node, slice_node)

    def build_bin_op_node(self, ast_object: ast.BinOp):
        bin_op_node = self.__get_next_cnt__()
        self.G.node(bin_op_node, label=f'BinOp', style='filled', shape='rectangle', color=color_map['BinOp'])

        left_node = self.__get_cnt__()
        self.build(ast_object.left)
        self.G.edge(bin_op_node, left_node)

        op_node = self.__get_cnt__()
        self.build(ast_object.op)
        self.G.edge(bin_op_node, op_node)

        right_node = self.__get_cnt__()
        self.build(ast_object.right)
        self.G.edge(bin_op_node, right_node)

    def build_list_node(self, ast_object: ast.List):
        list_node = self.__get_next_cnt__()
        self.G.node(list_node, label=f'List', style='filled', shape='rectangle', color=color_map['List'])
        for elem in ast_object.elts:
            elem_node = self.__get_cnt__()
            self.build(elem)
            self.G.edge(list_node, elem_node)

    def build_constant_node(self, ast_object: ast.Constant):
        constant_node = self.__get_next_cnt__()
        self.G.node(constant_node, label=f'Constant {ast_object.value}', style='filled', shape='rectangle',
                    color=color_map['Constant'])

    def build_name_node(self, ast_object: ast.Name):
        name_node = self.__get_next_cnt__()
        self.G.node(name_node, label=f'Name {ast_object.id}', style='filled', shape='rectangle',
                    color=color_map['Name'])

    def build_expr_node(self, ast_object: ast.Expr):
        expr_node = self.__get_next_cnt__()
        self.G.node(expr_node, label='Expr', style='filled', shape='rectangle', color=color_map['Expr'])

        value_node = self.__get_cnt__()
        self.build(ast_object.value)
        self.G.edge(expr_node, value_node)

    def build_module_node(self, ast_object: ast.Module):
        module_node = self.__get_next_cnt__()
        self.G.node(module_node, label='Module', style='filled', shape='rectangle', color=color_map['Module'])
        for i, elem in enumerate(ast_object.body):
            body_elem_node = self.__get_cnt__()
            self.build(elem)
            self.G.edge(module_node, body_elem_node)

    def build_function_def_node(self, ast_object: ast.FunctionDef):
        func_def_node = self.__get_next_cnt__()
        self.G.node(func_def_node, label=f'<{ast_object.name}> Function Definition',
                    style='filled', shape='rectangle', color=color_map['FunctionDef'])
        arguments_node = self.__get_next_cnt__()
        self.G.node(arguments_node, label=f'<{ast_object.name}> Function Arguments',
                    style='filled', shape='rectangle', color=color_map['Arguments'])
        self.G.edge(func_def_node, arguments_node)
        for i, elem in enumerate(ast_object.args.args):
            arg_node = self.__get_cnt__()
            self.build(elem)
            self.G.edge(arguments_node, arg_node)
        body_node = self.__get_cnt__()
        self.build_body_node(ast_object.body)
        self.G.edge(func_def_node, body_node)

    def build_arg_node(self, ast_object: ast.arg):
        var_name = ast_object.arg
        var_type = ast_object.annotation.id
        self.G.node(self.__get_next_cnt__(), label=f'{var_name}: {var_type}',
                    style='filled', shape='rectangle', color=color_map['Arg'])

    def build_assign_node(self, ast_object: ast.Assign):
        assign_node = self.__get_next_cnt__()
        self.G.node(assign_node, label=f'ASSIGN', style='filled', shape='rectangle', color=color_map['Assign'])

        target_node = self.__get_cnt__()
        self.build(ast_object.targets[0])
        self.G.edge(assign_node, target_node)

        value_node = self.__get_cnt__()
        self.build(ast_object.value)
        self.G.edge(assign_node, value_node)

    def build_body_node(self, body):
        body_node = self.__get_next_cnt__()
        self.G.node(body_node, label=f'Body',
                    style='filled', shape='rectangle', color=color_map['Body'])
        for i, elem in enumerate(body):
            body_elem_cnt = self.__get_cnt__()
            self.build(elem)
            self.G.edge(body_node, body_elem_cnt)

    def build_if_node(self, ast_object: ast.If):
        if_node = self.__get_next_cnt__()
        self.G.node(if_node, label=f'If', style='filled', shape='rectangle', color=color_map['If'])

        left_node = self.__get_next_cnt__()
        self.G.node(left_node, label=f'{self.__get_value__(ast_object.test.left)}', style='filled', shape='rectangle',
                    color=color_map['Value'])
        self.G.edge(if_node, left_node)

        comparator_node = self.__get_next_cnt__()
        cmp = comparators[type(ast_object.test.ops[0])]
        self.G.node(comparator_node, label=f'Comparator: {cmp}', style='filled',
                    shape='rectangle', color=color_map['Comparator'])
        self.G.edge(if_node, comparator_node)

        right_node = self.__get_next_cnt__()
        value = self.__get_value__(ast_object.test.comparators[0])
        self.G.node(right_node, label=f'{value}', style='filled',
                    shape='rectangle', color=color_map['Value'])
        self.G.edge(if_node, right_node)

        body_node = self.__get_cnt__()
        self.build_body_node(ast_object.body)
        self.G.edge(if_node, body_node)

    def build_raise_node(self, ast_object: ast.Raise):
        raise_node = self.__get_next_cnt__()
        self.G.node(raise_node, label='Exception', style='filled', shape='rectangle', color=color_map['Exception'])
        exception_name = ast_object.exc.func.id
        exception_name_node = self.__get_next_cnt__()
        self.G.node(exception_name_node, label=f'{exception_name}', style='filled',
                    shape='rectangle', color=color_map['Value'])
        self.G.edge(raise_node, exception_name_node)

    def __get_value__(self, ast_object):
        if ast_object is None:
            return None
        if type(ast_object) == ast.Subscript:
            var_name = ast_object.value.id
            lower = self.__get_value__(ast_object.slice.lower)
            upper = self.__get_value__(ast_object.slice.upper)
            step = self.__get_value__(ast_object.slice.step)
            if lower is None and step is None and upper:
                return f"{var_name}[:{upper}]"
            return f"{var_name}[{lower}:{upper}:{step}]"
        elif type(ast_object) == ast.Constant:
            return "CONST " + str(ast_object.value)
        elif type(ast_object) == ast.Name:
            return "VAR " + str(ast_object.id)

    def build_return_node(self, ast_object: ast.Return):
        return_node = self.__get_next_cnt__()
        self.G.node(return_node, label='Return', style='filled', shape='rectangle', color=color_map['Return'])

        value = self.__get_value__(ast_object.value)
        value_node = self.__get_next_cnt__()
        self.G.node(value_node, label=f'{value}', style='filled', shape='rectangle', color=color_map['Value'])

        self.G.edge(return_node, value_node)

    def build_call_node(self, ast_object: ast.Call):
        call_node = self.__get_next_cnt__()
        self.G.node(call_node, label=f'Call', style='filled', shape='rectangle', color=color_map['Call'])

        func_node = self.__get_cnt__()
        self.build(ast_object.func)
        self.G.edge(call_node, func_node)

        args_node = self.__get_next_cnt__()
        self.G.node(args_node, label='arguments', style='filled', shape='rectangle', color=color_map['Arguments'])
        self.G.edge(call_node, args_node)

        for elem in ast_object.args:
            arg_node = self.__get_cnt__()
            self.build(elem)
            self.G.edge(args_node, arg_node)

    def build_attribute_node(self, ast_object: ast.Attribute):
        attribute_node = self.__get_next_cnt__()
        self.G.node(attribute_node, label='Attribute', style='filled', shape='rectangle', color=color_map['Attribute'])

        value_node = self.__get_cnt__()
        self.build(ast_object.value)
        self.G.edge(attribute_node, value_node)

        attr_node = self.__get_next_cnt__()
        self.G.node(attr_node, label=f'attr: {ast_object.attr}', style='filled', shape='rectangle',
                    color=color_map['Attribute'])
        self.G.edge(attribute_node, attr_node)

    def build_for_node(self, ast_object: ast.For):
        for_node = self.__get_next_cnt__()
        self.G.node(for_node, label='For', style='filled', shape='rectangle', color=color_map['For'])

        target_node = self.__get_next_cnt__()
        target = self.__get_value__(ast_object.target)
        self.G.node(target_node, label=f'{target}', style='filled', shape='rectangle', color=color_map['Value'])
        self.G.edge(for_node, target_node)

        iter_node = self.__get_cnt__()
        self.build(ast_object.iter)
        self.G.edge(for_node, iter_node)

        body_node = self.__get_cnt__()
        self.build_body_node(ast_object.body)
        self.G.edge(for_node, body_node)
