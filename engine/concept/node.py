import io, sys, time
from typing import Union
from .utils import mergeDicts

class IoMap:
    def __init__(self, name: int, type: str, required: bool = False, default: str = None):
        self.type = type
        self.name = name
        self.required = required
        self.default = default

class Command:
    def __init__(self, node, inputs: list = None):
        self.node = node
        self.inputs = inputs
        
class InputReferenceConversor:
    def __init__(self, parentInputName: str, childInputName: str):
        self.parent = parentInputName
        self.child = childInputName

class Node:    
    def __init__(self,
        id: str,
        name: str,
        inputsMap: list = None,
        outputsMap: list = None,
        script: Union[str, list] = None,
        author: str = None,
        exception: str = None,
    ) -> None:
        self.id = id
        self.name = name
        self.inputsMap = inputsMap
        self.outputsMap = outputsMap
        self.script = script,
        self.author = author
        self.exeption = exception
        self.kind = None
        self.currStep = 0
        
        self.currOutputs = None
        self.firstInputs = None
        
        if isinstance(script, str):
            self.kind = "Script"
        elif isinstance(script, list):
            self.kind = "Group"
            self.script = script
            
        self.this = {}
        
    
    # def exec_with_output(self, code, variables):
    #     namespace = variables
    #     exec(code, namespace)
    #     return namespace
    
    def exec_with_output(self, code, variables):
        namespace = variables
        stdout = io.StringIO()
        sys.stdout = stdout  # Redirecionar a saída padrão para o buffer
        start_time = time.time()
        status = "starting"
        
        try:
            exec(code, namespace)
            output = stdout.getvalue()  # Obter a saída do buffer
            status = "success"
        except Exception as e:
            output = f"Error: {str(e)}"
            status = "error"
        finally:
            sys.stdout = sys.__stdout__  # Restaurar a saída padrão
        
        end_time = time.time()
        duration = end_time - start_time
        namespace['__execution__params__'] = {} #output  # Adicionar a saída como uma variável no namespace
        namespace['__execution__params__']['terminal_output'] = output
        namespace['__execution__params__']['execution_duration'] = duration
        namespace['__execution__params__']['status'] = status
        
        return namespace
        
    def run(self, internal_engine_inputs = None) -> Union[list, None]:
        if self.kind == "Script":
            _output_dict = self.runScript(internal_engine_inputs)
            return _output_dict
        elif self.kind == "Group":
            self.runGroup(internal_engine_inputs)
            return self.currOutputs
        
    def runGroup(self, internal_engine_inputs):
        # Executa a sequência dos scripts
        for i, curr_command in enumerate(self.script):
                curr_command: Command = curr_command
                # Se for o primeiro node ele define os inputs padrão 
                if(i == 0 and internal_engine_inputs):
                    self.currOutputs = internal_engine_inputs
                    self.firstInputs = self.currOutputs
                    internal_engine_inputs = None
                    
                # Define a ordem dos outputs para cada tipo de node (script/group)
                # Se for group a preferencia dos parametros de input é do node inicial 
                # Se for script a preferencia dos paramentros de input é do output do node anterior
                if curr_command.inputs and len(curr_command.inputs) > 0:
                    for conversor_input in curr_command.inputs:
                        conv: InputReferenceConversor = conversor_input
                        if curr_command.node.kind == 'Script':
                            self.currOutputs[conv.child] = mergeDicts(self.firstInputs, self.currOutputs)[conv.parent] 
                        elif curr_command.node.kind == 'Group':
                            self.currOutputs[conv.child] = mergeDicts(self.currOutputs, self.firstInputs)[conv.parent]
                
                # Executa o próximo node levando em consideração a condição de agrupamento complexo
                outputs = curr_command.node.run(self.currOutputs)
                self.currOutputs = outputs
    
    def runScript(self, internal_engine_inputs):
        this = {}
        this[self.id]: dict = {
            'inputs': {},
            'outputs': {}
        }
        
        # Mapeamento de inputs e tipos 
        # //TODO - Melhorar função de tipagem para considerar todos os tipos possíveis)
        for _inpIndex, _input in enumerate(self.inputsMap):
            _inpIndex: int = _inpIndex
            _input: IoMap = _input
            this[self.id]['inputs'][_input.name] = internal_engine_inputs[_input.name] if _input.name in internal_engine_inputs else _input.default
            if _input.type == 'str':
                this[self.id]['inputs'][_input.name] = str(this[self.id]['inputs'][_input.name])
            elif _input.type == 'float' or _input.type == 'number':
                this[self.id]['inputs'][_input.name] = float(this[self.id]['inputs'][_input.name])
            elif _input.type == 'int' or _input.type == 'integer':
                this[self.id]['inputs'][_input.name] = int(this[self.id]['inputs'][_input.name])
                
                
        # Formatação de script para ser executado em tempo de execução de forma isolada recebendo somente os inputs que precisar para rodar
        # //TODO - Encontrar uma lógica para resolver todos os problemas de indentação e melhorar o encapsulamento
        if(type(self.script) == list or type(self.script) == tuple):
            self.script = self.script[0]
        self.script = self.script.replace('  ', '').replace('\n  ', '\n')
        _exec_outputs = self.exec_with_output(self.script, this[self.id]['inputs'])
        
        this[self.id]['outputs']['__execution__params__'] = _exec_outputs['__execution__params__']
        
        if _exec_outputs['__execution__params__']['status'] == 'success':
            # Mapeamento dos outputs de acordo com o que foi processado no script
            for _output in self.outputsMap:
                this[self.id]['outputs'][_output.name] = _exec_outputs[_output.name] if (_output.name in _exec_outputs) else None
        
        
        _output_dict = this[self.id]['outputs']
        return _output_dict