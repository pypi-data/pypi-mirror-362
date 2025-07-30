import ast
import json
import base64
import inspect
import inspect
import typing
import pydantic
import importlib
import json
from ailice.common.ADataType import AImage, AImageLocation, AVideo, AVideoLocation

class AJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return {"_type": "bytes", "value": base64.b64encode(obj).decode('utf-8')}
        elif isinstance(obj, AImage):
            return {"_type": "AImage", "value": obj.ToJson()}
        elif isinstance(obj, AImageLocation):
            return {"_type": "AImageLocation", "value": obj.ToJson()}
        elif isinstance(obj, AVideo):
            return {"_type": "AVideo", "value": obj.ToJson()}
        elif isinstance(obj, AVideoLocation):
            return {"_type": "AVideoLocation", "value": obj.ToJson()}
        elif isinstance(obj, pydantic.BaseModel):
            return {"_type": obj.__class__.__name__, "value": obj.model_dump_json()}
        else:
            return super(AJSONEncoder, self).default(obj)

class AJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        try:
            if "_type" not in obj:
                return obj
            type = obj["_type"]
            if type == "bytes":
                return base64.b64decode(obj['value'].encode('utf-8'))
            elif type == "AImage":
                return AImage.FromJson(obj["value"])
            elif type == 'AImageLocation':
                return AImageLocation.FromJson(obj["value"])
            elif type == 'AVideo':
                return AVideo.FromJson(obj["value"])
            elif type == 'AVideoLocation':
                return AVideoLocation.FromJson(obj["value"])
            else:
                ModelType = pydantic.create_model(obj["_type"], **obj["value"])
                return ModelType().model_validate_json(obj["value"])
        except Exception as e:
            print("AJSONDecoder Exception. ", str(e))
            return obj

TYPE_NAMESPACE = {
    'bool': bool,
    'int': int,
    'float': float,
    'complex': complex,
    'str': str,
    'bytes': bytes,
    'bytearray': bytearray,
    'None': None,
    'tuple': tuple,
    'list': list,
    'dict': dict,
    'set': set,
    'Optional': typing.Optional,
    'Union': typing.Union,
    'Generator': typing.Generator,
    'AImage': AImage,
    'AImageLocation': AImageLocation,
    'AVideo': AVideo,
    'AVideoLocation': AVideoLocation
}

def SignatureFromString(sig_str: str) -> inspect.Signature:
    funcDefNode = ast.parse(f"def f{sig_str}:\n    pass", mode='exec').body[0]
    
    def BuildArg(arg, kind):
        annotation = BuildTypeFromAST(arg.annotation, TYPE_NAMESPACE) if arg.annotation else inspect.Parameter.empty
        return inspect.Parameter(name=arg.arg, kind=kind, annotation=annotation)

    parameters = []
    for arg in funcDefNode.args.args:
        parameters.append(BuildArg(arg, inspect.Parameter.POSITIONAL_OR_KEYWORD))

    if funcDefNode.args.vararg:
        parameters.append(BuildArg(funcDefNode.args.vararg, inspect.Parameter.VAR_POSITIONAL))
    
    if funcDefNode.args.kwarg:
        parameters.append(BuildArg(funcDefNode.args.kwarg, inspect.Parameter.VAR_KEYWORD))
    
    defaults = funcDefNode.args.defaults
    if defaults:
        offset = len(parameters) - len(defaults)
        for i, default in enumerate(defaults):
            try:
                defaultValue = ast.literal_eval(default)
            except (ValueError, SyntaxError):
                defaultValue = inspect.Parameter.empty
                
            parameters[offset + i] = parameters[offset + i].replace(default=defaultValue)
    
    returnAnnotation = BuildTypeFromAST(funcDefNode.returns, TYPE_NAMESPACE) if funcDefNode.returns else inspect.Parameter.empty
    return inspect.Signature(parameters=parameters, return_annotation=returnAnnotation)


def BuildTypeFromAST(node, namespace):
    if isinstance(node, ast.Name):
        if node.id not in namespace:
            raise TypeError(f"BuildTypeFromAST(): Unsupported type {str(node.id)}.")
        return namespace[node.id]
    
    elif isinstance(node, ast.Attribute):
        attrChain = []
        current = node
        while isinstance(current, ast.Attribute):
            attrChain.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            attrChain.append(current.id)
        attrChain.reverse()
        
        baseModule = namespace.get(attrChain[0], None)
        if baseModule is None:
            if (attrChain[:3] == ["ailice", "common", "ADataType"]):
                baseModule = importlib.import_module(attrChain[0])
            else:
                raise TypeError(f"BuildTypeFromAST(): Unsupported type {str(attrChain)}.")
        
        currentObj = baseModule
        for i in range(1, len(attrChain)):
            currentObj = getattr(currentObj, attrChain[i])
        return currentObj
    elif isinstance(node, ast.Subscript):
        container = BuildTypeFromAST(node.value, namespace)
        
        args = node.slice
        if isinstance(args, ast.Tuple):
            type_args = [BuildTypeFromAST(arg, namespace) for arg in args.elts]
            return container[tuple(type_args)]
        else:
            type_arg = BuildTypeFromAST(args, namespace)
            return container[type_arg]
    elif isinstance(node, ast.Tuple):
        return tuple(BuildTypeFromAST(elt, namespace) for elt in node.elts)
    elif isinstance(node, ast.Constant) and node.value is None:
        return None
    else:
        raise TypeError(f"BuildTypeFromAST(): Unsupported type {str(node)}.")

def AnnotationsFromSignature(signature: inspect.Signature) -> dict:
    annotations = {}
    
    for param_name, param in signature.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            annotations[param_name] = param.annotation
    
    if signature.return_annotation is not inspect.Parameter.empty:
        annotations['return'] = signature.return_annotation
    return annotations
