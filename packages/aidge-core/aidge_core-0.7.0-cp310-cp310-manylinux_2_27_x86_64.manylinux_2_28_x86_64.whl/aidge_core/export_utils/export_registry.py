from typing import Dict, List
import aidge_core
from aidge_core.export_utils import ExportNode


class classproperty:
    """Helper class to define class-level properties.

    Equivalent to applying both the ``@property`` and ``@classmethod`` decorators,
    allowing methods to be accessed as class properties. These two decorators
    are otherwise incompatible prior to Python 3.12.

    See discussion: https://discuss.python.org/t/add-a-supported-read-only-classproperty-decorator-in-the-stdlib/18090/12
    """

    def __init__(self, fget):
        """
        :param fget: Function to be wrapped as a class property.
        :type fget: Callable
        """
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)


class ExportLib(aidge_core.OperatorImpl):
    """Aidge export library that manages a registry for operators and static files.

    This class provides a structure for registering different operator types and
    export nodes, facilitating access and management of these elements.

    :ivar _name: The name of the export library, used for namespacing.
    :ivar static_files: A dictionary mapping paths of static files to their target locations relative to the export root.
    """
    # PUBLIC
    # Lib name useful ?
    # Help define namespace
    _name: str = None
    # key: Path where static file is
    # Value: Path where to copy the file relative to the export root
    static_files: Dict[str, str] = {}
    # key: Path where static folder is
    # Value: Path where to copy the folder relative to the export root
    static_folders: Dict[str, str] = {}
    # Main memory section
    mem_section = None
    # Custom forward generation jinja file
    forward_template: str = None
    forward_header_template: str = None
    # PRIVATE
    # Registry of exportNode, class level dictionary, shared across all ExportLib
    _cls_export_node_registry = {}

    def __init__(self, operator):
        super(ExportLib, self).__init__(operator, self._name)
        if self._name is None:
            raise ValueError("ExportLib  {self.__class__.__name__} does not define the attribute ``_name``.")

        # TODO: This is a patch, setBackend method is used to set an ExportLib as an Implementation.
        # But it also set the backend of the Tensor and we don't define a backend for Tensor.
        # The following code block associate to the export backend the "cpu" implementation.
        # This is tracked by the issue :
        #         https://gitlab.eclipse.org/eclipse/aidge/aidge_core/-/issues/178

        aidge_core.register_Tensor([self._name, aidge_core.dtype.float64],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.float64]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.float32],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.float32]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.float16],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.float16]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.int8],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.int8]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.int16],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.int16]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.int32],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.int32]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.int64],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.int64]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.uint8],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.uint8]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.uint16],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.uint16]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.uint32],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.uint32]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.uint64],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.uint64]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.int4],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.int4]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.uint4],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.uint4]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.dual_int4],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.dual_int4]))
        aidge_core.register_Tensor([self._name, aidge_core.dtype.dual_uint4],
                                    aidge_core.get_key_value_Tensor(["cpu", aidge_core.dtype.dual_uint4]))

    @classproperty
    def _export_node_registry(cls) -> Dict[str, List['ExportNode']]:
        """Define as a class property to access the registry at class level while keeping it at instance level.

        :return: The export node registry specific to the class
        :rtype: Dict[str, List[ExportNode]]
        """
        return cls._cls_export_node_registry.setdefault(cls, {})

    def get_available_impl_specs(self) -> List[aidge_core.ImplSpec]:
        """Override the virtual OperatorImpl method, in order to provide available
        implementation specifications.

        :return: List of implementation specification available for the type of operator.
        :rtype: List[aidge_core.ImplSpec]
        """
        if self.get_operator().type() in self._export_node_registry:
            spec_vec = [i for i, _ in self._export_node_registry[self.get_operator().type()]]
            return spec_vec
        else:
            return []

    def get_export_node(self, spec: aidge_core.ImplSpec) -> ExportNode:
        """Given an aidge_core.ImplSpec, return the ExportNode that is the closest match.

        :param spec: Implementation specification to match
        :type spec: aidge_core.ImplSpec
        :return: The class ExportNode that is the closest match
        :rtype: aidge_core.ImplSpec
        """
        for registered_spec, export_node in self._export_node_registry[self.get_operator().type()]:
            if registered_spec == spec:

                return export_node
        return None

    @classmethod
    def register(cls, op_type, spec: aidge_core.ImplSpec, prod_conso: aidge_core.ProdConso = aidge_core.ProdConso.default_model):
        """Decorator to register an operator implementation for a specified operator type.

        Registers an operator under a given operator type and specification,
        adding it to the export library registry. This method supports both
        single operator types (str) and lists of types (List[str]).

        :param op_type: The operator type(s) to register.
        :type op_type: Union[str, List[str]]
        :param spec: Implementation specification for the operator.
        :type spec: :py:class:``aidge_core.ImplSpec``
        :return: A wrapper class that initializes the registered operator.
        :rtype: Callable
        """
        def decorator(operator):
            type_list = []
            if isinstance(op_type, list):
                type_list = op_type
            elif isinstance(op_type, str):
                type_list = [op_type]
            else:
                raise TypeError("Argument type of register method should be of type 'List[str]' or 'str', got {type(type)}")

            for type_name in type_list:
                if (type_name not in cls._export_node_registry):
                    cls._export_node_registry[type_name] = []
                cls._export_node_registry[type_name].append((spec, operator))

                register_func: str = f"register_{type_name}Op"
                # If operator is not defined, then it means we try to register a MetaOperator
                if register_func not in dir(aidge_core):
                    raise ValueError(f"Operator of type: {type_name} is not declared as registrable!\nHint: If you try to register a MetaOperator use register_metaop instead.")
                else:
                    # Equivalent to aidge_core.register_ConvOp("ExportLibX", ExportLibX)
                    aidge_core.__getattribute__(register_func)(cls._name, cls)
                    aidge_core.register_ProdConso([cls._name, type_name], prod_conso)
            return operator
        return decorator

    @classmethod
    def register_metaop(cls, op_type, spec: aidge_core.ImplSpec, prod_conso: aidge_core.ProdConso = aidge_core.ProdConso.default_model):
        """Decorator to register a MetaOperator with the export library.

        Registers a MetaOperator under a given operator type and specification. This decorator
        is intended for operator types that are grouped as meta operators.

        :param op_type: Operator type(s) to register as a ``MetaOperator``.
        :type op_type: Union[str, List[str]]
        :param spec: Implementation specification for the MetaOperator.
        :type spec: aidge_core.ImplSpec
        :return: A wrapper class that initializes the registered MetaOperator.
        :rtype: Callable
        """
        def decorator(operator):
            type_list = []
            if isinstance(op_type, list):
                type_list = op_type
            elif isinstance(op_type, str):
                type_list = [op_type]
            else:
                raise TypeError("Argument 'op_type' of register method should be of type 'List[str]' or 'str', got {type(type)}")
            for type_name in type_list:
                if (type_name not in cls._export_node_registry):
                    cls._export_node_registry[type_name] = []
                cls._export_node_registry[type_name].append((spec, operator))
                aidge_core.register_MetaOperatorOp([cls._name, type_name], cls)
                aidge_core.register_ProdConso([cls._name, type_name], prod_conso)
            return operator
        return decorator


    @classmethod
    def register_generic(cls, op_type, spec: aidge_core.ImplSpec, prod_conso: aidge_core.ProdConso = aidge_core.ProdConso.default_model):
        """Decorator to register a GenericOperator with the export library.

        Registers a GenericOperator under a given operator type and specification. This decorator
        is intended for operator types that are grouped as meta operators.

        :param op_type: Operator type(s) to register as a ``GenericOperator``.
        :type op_type: Union[str, List[str]]
        :param spec: Implementation specification for the GenericOperator.
        :type spec: aidge_core.ImplSpec
        :return: A wrapper class that initializes the registered GenericOperator.
        :rtype: Callable
        """
        def decorator(operator):
            type_list = []
            if isinstance(op_type, list):
                type_list = op_type
            elif isinstance(op_type, str):
                type_list = [op_type]
            else:
                raise TypeError("Argument 'op_type' of register method should be of type 'List[str]' or 'str', got {type(type)}")
            for type_name in type_list:
                if (type_name not in cls._export_node_registry):
                    cls._export_node_registry[type_name] = []
                cls._export_node_registry[type_name].append((spec, operator))
                aidge_core.register_GenericOperatorOp([cls._name, type_name], cls)
                aidge_core.register_ProdConso([cls._name, type_name], prod_conso)
            return operator
        return decorator
