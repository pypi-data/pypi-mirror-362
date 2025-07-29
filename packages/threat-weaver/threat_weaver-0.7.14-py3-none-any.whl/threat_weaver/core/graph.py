import networkx as nx
import graphviz as viz


class MulVALGraph:

    def __init__(self, name=None):
        self.name = name
        self.nodes = {}  # 有点重复存储的意思
        self.index = 0
        self.graph = nx.DiGraph()

    def _fact_(self, text):
        if not self.nodes.get(text):
            self.index += 1
            self.nodes[text] = self.index
            return str(self.index)
        else:
            return str(self.nodes[text])

    def _action_(self, text):
        self.index += 1     # TODO：动作加一
        self.nodes[str(self.index)] = text
        return str(self.index)

    def insert(self, clause):
        conditions, rule_desc, results = clause
        rule_id = str(self._action_(rule_desc))  # 动作编号
        self.graph.add_node(rule_id, fact=rule_desc, dtype='AND')
        for fact in results:    # 结果
            fact_id = str(self._fact_(fact)) # 事实编号
            self.graph.add_node(fact_id, fact=fact, dtype='OR')
            self.graph.add_edge(rule_id, fact_id)
        for fact in conditions:    # 条件
            fact_id = self._fact_(fact)
            self.graph.add_node(fact_id, fact=fact)
            self.graph.nodes[fact_id].setdefault('dtype', 'LEAF')
            self.graph.add_edge(fact_id, rule_id)

    def update(self, clauses):
        for clause in clauses:
            self.insert(clause)

    def to_pdf(self, name=None):
        name = name or self.name or 'AttackGraph'
        dot = viz.Digraph(comment='Intranets of Attack Graph')
        # 设置节点类型
        for nid, attr in self.graph.nodes(data=True):
            cont = f"{nid}::{attr['fact']}"
            if attr['dtype'] == 'AND':
                dot.node(nid, shape='ellipse', label=cont, style='filled')
            elif attr['dtype'] == 'OR':
                dot.node(nid, shape='diamond', label=cont, style='filled')
            elif attr['dtype'] == 'LEAF':
                dot.node(nid, shape='box', label=cont, style='filled')
            else:
                raise NotImplementedError

        for src_id, dst_id, attr in self.graph.edges(data=True):
            if self.graph.nodes[dst_id]['dtype'] == 'AND':
                dot.edge(src_id, dst_id, label='and')
            elif self.graph.nodes[dst_id]['dtype'] == 'OR':
                dot.edge(src_id, dst_id, label='or')
            else:
                raise NotImplementedError

        dot.render(f"{name}", view=False, cleanup=True)
        return True

    def to_gml(self, name=None):
        name = name or self.name
        nx.write_graphml(self.graph, f"{name}.gml")

