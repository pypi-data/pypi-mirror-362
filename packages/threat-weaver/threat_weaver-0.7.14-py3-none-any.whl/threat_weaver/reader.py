


class MulVALLoader():
    def __init__(self, host_file):
        self.facts = self._load_file_data(host_file)

    def _load_file_data(self, file_path):
        facts = set()
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                fact = line.strip()
                if not fact:
                    continue
                if fact.startswith('attackGoal'):
                    continue
                facts.add(fact)
        return facts

    def _split_fact_(self, text: str) -> (str, list):
        predicate, description = text.split("(", 1)
        variables = description.rsplit(")", 1)[0].split(",")
        return predicate, tuple([t.strip() for t in variables if t])

    def next_fact(self):
        outputs = []
        for fact in self.facts:
            outputs.append(self._split_fact_(fact))
        return outputs