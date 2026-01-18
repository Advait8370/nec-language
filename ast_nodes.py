class Let:
    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

class Print:
    def __init__(self, value, line):
        self.value = value
        self.line = line

class Data:
    def __init__(self, name, source, line):
        self.name = name
        self.source = source
        self.line = line

class Model:
    def __init__(self, name, model_type, line):
        self.name = name
        self.model_type = model_type
        self.line = line

class Train:
    def __init__(self, model, dataset, line):
        self.model = model
        self.dataset = dataset
        self.line = line

class Use:
    def __init__(self, package, line):
        self.package = package
        self.line = line
