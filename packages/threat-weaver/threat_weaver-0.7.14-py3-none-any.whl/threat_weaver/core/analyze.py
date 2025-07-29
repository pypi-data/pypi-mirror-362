import os

import yaml
import itertools
from importlib.resources import path

from ..call.indexes import DictTable
from ..call import pattern


class LogicAnalyzer:
    '''
        兼容HornClause，"L :-L1, L2, L3, ...")格式
        [拓展],L可以不止一个。
    '''
    def __init__(self, yaml_path='interaction.yaml'):
        if os.path.isfile(yaml_path):
            facts, rules = self._configure_(yaml_path)
        else:
            facts, rules = self._resource_(yaml_path)
        self.pairs = {word: attr for word, attr in facts}  # 实体-属性字典
        self.table = DictTable(facts)  # 快速索引表
        self.patterns = self._pattern_(rules)  # 交互规则库
        self.fact2id = {}  # 事实索引值
        self.id2fact = {}
        self.update_graph_lock = True

    def _resource_(self, filename: str) -> (list, list):
        with path('threat_weaver.kb', filename) as file_path:
            return self._configure_(file_path)

    def _configure_(self, file_path: str) -> (list, list):
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
        facts = [self._literal_(fact) for fact in yaml_data['primitive']]
        facts.extend([self._literal_(fact) for fact in yaml_data['derived']])
        rules = yaml_data['interaction']
        return facts, rules

    def _literal_(self, text: str) -> (str, list):
        word, content = text.split("(", 1)
        tokens = content.rsplit(")", 1)[0].split(",")
        return word, [t.strip() for t in tokens if t]

    def _pattern_(self, interactions: list) -> list:
        outputs = []
        for record in interactions:
            attack_pattern = pattern.PrologRule(
                desc=record['description'].strip(),
                clause=record['rule'].strip())
            outputs.append(attack_pattern)
        return outputs

    def add_fact(self, predicate: str, attributes: tuple):
        if len(attributes) != len(self.pairs[predicate]):
            raise ValueError(f"The number of attributes does not match the number of attributes in the predicate.")
        if not isinstance(attributes, tuple):
            raise TypeError(f"attributes must be a tuple, but got {type(attributes).__name__}")
        if self.fact2id.get((predicate, attributes)):
            return self.fact2id[(predicate, attributes)]

        fact_id = self.table.append({
            'word': predicate,
            **{k: v for k, v in zip(self.pairs[predicate], attributes)}
        })
        self.fact2id.setdefault((predicate, attributes), fact_id)
        self.id2fact.setdefault(fact_id, (predicate, attributes))
        return fact_id

    def _reasoning_(self, attack_pattern, cur_state_id):
        predicate, attributes = self.id2fact[cur_state_id]
        outputs, combinations = [], []
        # 查找关联事实
        conditions = attack_pattern.condition(predicate, attributes)
        for condition in conditions:
            relations = self.table.search(
                predicate=condition[0],
                where={self.pairs[condition[0]][k]: v for k, v in condition[1].items() if v != '_'})
            if not relations:  # 空值阻断
                return []
            combinations.append(relations)
        # 进行逻辑推理
        for fact_ids in itertools.product(*combinations):  # 组合推理
            body_fact_ids = list(fact_ids) + [cur_state_id]
            body_facts = [self.id2fact[fid] for fid in fact_ids]
            body_facts.append((predicate, attributes))
            head_fact_ids = []
            for head_fact in attack_pattern.deduce(body_facts):
                head_fact_id = self.fact2id.get(head_fact)
                if not head_fact_id:
                    head_fact_id = self.table.append({
                        'word': head_fact[0],  # 注册派生事实
                        **{k: v for k, v in zip(self.pairs[head_fact[0]], head_fact[1])}
                    })
                    self.id2fact[head_fact_id] = head_fact    # 注册事实
                    self.fact2id[head_fact] = head_fact_id    # 标记事实
                head_fact_ids.append(head_fact_id)
            if not head_fact_ids:
                continue
            outputs.append((body_fact_ids, attack_pattern.rule_desc, head_fact_ids))
        return outputs

    def _deducing_(self, pattern, cur_fact_id):
        head_fact_ids = list()
        head_facts = pattern.deduce([self.id2fact[cur_fact_id]])
        for head_fact in head_facts:
            head_fact_id = self.fact2id.get(head_fact)
            if not head_fact_id:
                head_fact_id = self.table.append({
                    'word': head_fact[0],  # 注册派生事实
                    **{k: v for k, v in zip(self.pairs[head_fact[0]], head_fact[1])}
                })
                self.id2fact[head_fact_id] = head_fact  # 注册事实
                self.fact2id[head_fact] = head_fact_id  # 标记事实

            head_fact_ids.append(head_fact_id)

        if not head_fact_ids:
            return []
        return [([cur_fact_id], pattern.rule_desc, head_fact_ids)]

    def _inference_(self, init_fact_ids):
        queue = list(init_fact_ids)  # 要满足单调性
        while queue:
            cur_state_id = queue.pop(0)  # 队列
            max_stack_id = self.table.index  # 记录栈顶索引
            for attack_pattern in self.patterns:    # 攻击模式识别
                if self.id2fact[cur_state_id][0] not in attack_pattern.clause.body:  # todo:对rule建立索引。
                    continue
                elif len(attack_pattern.clause.body) == 1:
                    steps = self._deducing_(attack_pattern, cur_state_id)
                else:
                    steps = self._reasoning_(attack_pattern, cur_state_id)

                for body, iff, head in steps:
                    yield body, iff, head
                    queue.extend([fid for fid in head if fid > max_stack_id])

    def _clause_(self, body, iff, head):
        outputs = [[], "", []]
        for fact_id in body:
            literal = f"{self.id2fact[fact_id][0]}({','.join(self.id2fact[fact_id][1])})"
            outputs[0].append(literal)
        outputs[1] = iff
        for fact_id in head:
            literal = f"{self.id2fact[fact_id][0]}({','.join(self.id2fact[fact_id][1])})"
            outputs[2].append(literal)
        return outputs

    def generate(self, attackerLocated="attackerLocated"):
        ''' 一次生成：需要去重 '''
        init_fact_ids = self.table.search(predicate=attackerLocated, where={})
        if not init_fact_ids:
            raise ValueError("No attackerLocated fact found.")
        self.update_graph_lock = False

        trace, unique = [], set()
        for body, iff, head in self._inference_(init_fact_ids):
            step = self._clause_(body, iff, head)
            trace.append(step)
        return trace

    def update(self, predicate: str, attributes: tuple):
        ''' 实时生成，不应该关心重复性问题 '''
        if not isinstance(attributes, tuple):
            raise TypeError(f"attributes must be a tuple, but got {type(attributes).__name__}")
        if self.fact2id.get((predicate, attributes)):
            return []   # 重复信息

        fact_id = self.table.append({
            'word': predicate,
            **{k: v for k, v in zip(self.pairs[predicate], attributes)}
        })
        self.id2fact.setdefault(fact_id, (predicate, attributes))
        self.fact2id.setdefault((predicate, attributes), fact_id)

        trace, unique = [], set()
        for body, iff, head in self._inference_([fact_id]):
            step = self._clause_(body, iff, head)
            trace.append(step)
        return trace
