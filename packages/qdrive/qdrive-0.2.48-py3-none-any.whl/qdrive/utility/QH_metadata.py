from typing import List, Dict,  Union

from qcodes.instrument import Instrument
from qcodes.parameters import Parameter

def validate_parameter(parameter: Parameter) -> Parameter:
    """
    Validate that a parameter is an instance of qcodes.Parameter and its value is int or float.

    Args:
        parameter (Parameter): The qcodes.Parameter to validate.

    Raises:
        ValueError: If the parameter is not a qcodes.Parameter, or if its current value is not a float or int.
        ValueError: If the parameter value cannot be retrieved (wrapped).

    Returns:
        Parameter: The original parameter if validation succeeds.
    """
    if not isinstance(parameter, Parameter):
        raise ValueError(f"Invalid parameter type: {type(parameter)}, expected qcodes.Parameter.")

    try:
        value = parameter.get()
        if not isinstance(value, (float, int)):
            raise ValueError(
                f"Invalid parameter value type: {type(value)}, "
                f"expected float or int (Parameter: {parameter.name})."
            )
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Could not get value from parameter: {parameter.name}") from e

    return parameter


class QHMetaDataManager(Instrument):
    """
    A QCoDeS Instrument subclass that manages key metadata for a dataset within the QHarbor framework.

    This manager stores a set of important QCoDeS Parameters (numeric), as well as static and dynamic
    labels and attributes for advanced metadata tracking. The metadata is exposed through two read-only
    parameters: 'labels' and 'attributes', enabling integration with measurement frameworks.
    """

    def __init__(self, important_parameters: List[Parameter] = [],
                       static_labels: List[str] = [],
                       static_attributes: Dict[str, str] = {}):
        """
        Initialize a QHMetaDataManager instance.

        Args:
            important_parameters (List[Parameter]): A list of qcodes.Parameter instances that
                will be included in the metadata. Each parameter's value is retrieved at snapshot.
            static_labels (List[str]): A list of static labels that are always included in
                the metadata. These labels remain after the reset method is called.
            static_attributes (Dict[str, str]): A dictionary of static attributes that are
                always included in the metadata. These attributes remain after the reset method is called.
        """
        super().__init__("qh_meta")
        
        for param in important_parameters:
            validate_parameter(param)
        self._important_parameters = important_parameters

        self._static_labels = static_labels
        self._static_attributes = static_attributes

        self._dynamic_labels = []
        self._dynamic_attributes = {}

        self.add_parameter("labels", get_cmd=self.__get_labels)
        self.add_parameter("attributes", get_cmd=self.__get_attributes)

    def add_important_parameter(self, parameter: Parameter) -> None:
        """
        Add an additional important parameter to the metadata.

        Args:
            parameter (Parameter): The parameter to add. Must be numeric and valid.

        Raises:
            ValueError: If the parameter is not valid or its value is not numeric.
        """
        validate_parameter(parameter)
        self._important_parameters.append(parameter)

    def add_labels(self, labels: List[str]) -> None:
        """
        Add dynamic labels to the metadata. These labels will be cleared upon reset.

        Args:
            labels (List[str]): A list of labels to add.
        """
        self._dynamic_labels.extend(labels)

    def add_attributes(self, attributes: Dict[str, str]) -> None:
        """
        Add dynamic attributes to the metadata. These attributes will be cleared upon reset.

        Args:
            attributes (Dict[str, str]): A dictionary of key-value pairs to add as attributes.
        """
        self._dynamic_attributes.update(attributes)

    def reset(self) -> None:
        """
        Clear all dynamic labels and attributes.

        This does not affect static labels or attributes, nor the list of important parameters.
        """
        self._dynamic_labels.clear()
        self._dynamic_attributes.clear()

    def __get_labels(self) -> List[str]:
        """
        Return a combined list of static and dynamic labels.

        Returns:
            List[str]: The current list of labels (static + dynamic).
        """
        return self._static_labels + self._dynamic_labels

    def __get_attributes(self) -> Dict[str, Union[Dict, str]]:
        """
        Return a combined dictionary containing static, dynamic attributes, and parameter values.

        Returns:
            Dict[str, Dict]: A dictionary with:
                - static attributes (key -> str)
                - dynamic attributes (key -> str)
                - important parameter data (key -> {'value': numeric_value, 'extra': {'unit': param.unit}})
        """
        parameter_data = {}
        for param in self._important_parameters:
            parameter_data[param.name] = {
                "value": param.get(),
                "extra": {"unit": param.unit},
            }

        return { **self._static_attributes,
                 **self._dynamic_attributes,
                 **parameter_data, }
    
    def get_idn(self):
        return {'vendor': 'QHarbor', 'model': 'QHarbor Metadata Manager', 'serial': None, 'firmware': None}