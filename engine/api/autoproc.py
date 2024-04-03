class Autoproc:
    def __init__(self,
        id: str,
        name: str,
        script: str = None,
        group: list = [],
        inputs: list = [],
        outputs: list = [],
        nexts: list = [],
        author: str = None,
        exception: str = None
    ) -> None:
        self.id = id
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.script = script
        self.group = group
        self.nexts = nexts
        self.author = author
        self.exeption = exception
        self.this = {}

    def run(self):
        try:
            self.this['inputs'] = self.inputs
            self.this['outputs'] = self.outputs
            this = self.this
            exec(self.script)
        except Exception as e:
            raise e
        
    def exceptionFunction(self, err):
        self.this['error'] = err
        this = self.this
        exec(self.exeption)