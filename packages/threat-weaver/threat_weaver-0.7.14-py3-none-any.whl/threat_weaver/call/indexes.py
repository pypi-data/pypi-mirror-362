import copy


class DictTable():
    def __init__(self, indexes):
        self.table = {}     # 字典 pred|slot: {value: {pred.uuid}}
        self.index = 0      # 表字段
        self.sign = False
        self._create_(indexes)

    def _create_(self, indexes:list):
        for predicate, attributes in indexes:
            self.table.setdefault('word', dict())
            self.table['word'].setdefault(predicate, set())
            for attr_name in attributes:
                self.table.setdefault(attr_name, dict())
        self.sign = True   # 打开标识位

    def _select_(self, record: dict)->set:
        results = None  # TODO: 固定标识
        for slot, value in record.items():
            if not results:
                if results == None:
                    results = copy.deepcopy(
                        self.table[slot].get(value, set()) | self.table[slot].get('_', set()))
                else:
                    return set()
            else: # 有值
                results &= self.table[slot].get(value, set()) | self.table[slot].get('_', set())
        return results

    def search(self, predicate:str, where: dict)->set:
        condition = {'word': predicate, **where}
        return self._select_(condition)

    def _insert_(self, index: int, record: dict):
        for slot, value in record.items():
            if value.startswith('_'):
                value = '_'
            self.table[slot].setdefault(value, set())
            self.table[slot][value].add(index)
        return True

    def append(self, record: dict)->int:
        self.index += 1
        self._insert_(self.index, record)
        return self.index