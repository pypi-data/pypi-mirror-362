'''
    author: Gchl
    提取MulVAl交互规则中变量之间的依赖关系
'''


class HornClause:
    '''
        提取语句中隐含的关系
    '''

    def __init__(self, clause):
        self.head = {}
        self.body = {}
        self.params = {}
        self.matrix = []
        self.consts = []

        self._detect_(clause)
        self._matrix_(clause)

    def _detect_(self, clause):
        'todo:检查输入的语句是否为well-formed'
        if '\n' not in clause:
            raise ValueError('clause must be a well-formed statement')

    def _matrix_(self, clause: str):
        literals = [l.strip() for l in clause.split('\n')]  # TODO：必须是换行符
        word_num = len(literals)  # TODO 容易出错，检查
        _unique_attr_dict = dict()
        for literal in literals[::-1]:  # TODO: 必须是头在前，体在后
            predicate, attributes = self._literal_(literal)
            _list = self.body   # 软连接
            if literal.endswith(':-'):
                _list = self.head

            _list[predicate] = (len(self.head) + len(self.body), len(attributes))
            for _attr_idx_, attr_name in enumerate(attributes):
                if attr_name[0].isupper():  # 首字母大写，该变量为实体
                    if attr_name not in _unique_attr_dict:
                        _unique_attr_dict[attr_name] = len(_unique_attr_dict)
                        self.matrix.append([-1] * word_num)
                    self.matrix[_unique_attr_dict[attr_name]][_list[predicate][0]] = _attr_idx_
                elif attr_name[0] == '_':
                    continue
                else:  # 首字母小写或数字，该变量为变量
                    self.consts.append((_list[predicate][0], _attr_idx_, attr_name))

        self.params = _unique_attr_dict
        return

    def _literal_(self, text: str) -> (str, list):
        word, content = text.split("(", 1)
        tokens = content.rsplit(")", 1)[0].split(",")
        return word, [t.strip() for t in tokens if t]



class PrologRule:
    '''
        根据clause中记录的隐含关系，进行逻辑推理、查询等综合操作。
    '''
    def __init__(self, desc:str, clause:str):
        self.clause = HornClause(clause)
        self.rule_desc = desc

    def relations(self)->list:
        return self.clause.matrix

    def constants(self)->list:
        return self.clause.consts

    def condition(self, predicate, attributes)->(str, list):
        _map, outputs = {}, {}
        # 校验信息准确性
        pred_id, attr_num = self.clause.body.get(predicate)
        if attr_num != len(attributes):
            raise ValueError('condition fail')
        # 获取查询条件
        for _, relation in enumerate(self.relations()):
            # 解析变量”_“的fact依赖关系
            if relation[pred_id] == -1:
                continue    # 无效信息跳过
            for _lidx_, word in enumerate(self.clause.body):
                _map.setdefault(_lidx_, word)
                if word != predicate:
                    outputs.setdefault(word, {})
                    if relation[_lidx_] != -1:
                        outputs[word][relation[_lidx_]] = attributes[relation[pred_id]]

        _length = len(self.clause.body)
        for pred_id, _aidx_, const_value in self.constants():
            if pred_id < _length and _map.get(pred_id) != predicate:
                outputs[_map.get(pred_id)][_aidx_] = const_value
        return outputs.items()  # 组合关系

    def deduce(self, combination: list) -> list:
        output, _map = {}, {}
        reshape = [[0]] * len(combination)
        for pred, attrs in combination:
            reshape[self.clause.body[pred][0]] = attrs
        # 构造输出格式
        for predicate, (_lidx_, attr_num) in self.clause.head.items():
            _map.setdefault(_lidx_, predicate)
            output[predicate] = ['_'] * attr_num
        # 检查变量关联性
        _length = len(self.clause.body)
        for relation in self.relations():  # TODO 时间复杂度与变量个数
            last_value = None
            for _lidx_, _point_ in enumerate(relation[:_length]):
                cur_value = reshape[_lidx_][_point_]
                if _point_ >= 0:    # 判别有效
                    if last_value and cur_value != last_value:
                        if "_" not in (cur_value, last_value) :
                            return []  # TODO；踢出无法匹配对应关系的条件
                    last_value = last_value if cur_value == '_' else cur_value  # 用确定值代替非确定值
            for predicate, (_lidx_, _) in self.clause.head.items():
                if relation[_lidx_] == -1:
                    continue  # 不能为空
                output[predicate][relation[_lidx_]] = last_value or '_'
        # 检查常数一致性
        for _lidx_, _pidx_, value in self.constants():
            if _lidx_ < _length:
                if value != reshape[_lidx_][_pidx_]:
                    return []  # 未匹配上则剔除
            else:
                output[_map[_lidx_]][_pidx_] = value
        return [(word, tuple(attrs)) for word, attrs in output.items()]