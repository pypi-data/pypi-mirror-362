import json
import string
from enum import Enum
from typing import Any, Dict, List

from flamapy.core.models.ast import Node
from flamapy.core.transformations import ModelToText
from flamapy.metamodels.fm_metamodel.models import (
    Constraint,
    Feature,
    FeatureModel,
    Attribute
)


class JSONFeatureType(Enum):
    FEATURE = 'FEATURE'
    XOR = 'XOR'
    OR = 'OR'
    MUTEX = 'MUTEX'
    CARDINALITY = 'CARDINALITY'
    OPTIONAL = 'OPTIONAL'
    MANDATORY = 'MANDATORY'


class JSONWriter(ModelToText):

    @staticmethod
    def get_destination_extension() -> str:
        return 'json'

    def __init__(self, path: str, source_model: FeatureModel):
        self.path = path
        self.source_model = source_model

    def transform(self) -> str:
        json_object = to_json(self.source_model)
        if self.path is not None:
            with open(self.path, 'w', encoding='utf8') as file:
                json.dump(json_object, file, indent=4)
        return json.dumps(json_object, indent=4)


def to_json(feature_model: FeatureModel) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    result['features'] = get_tree_info(feature_model.root)
    result['constraints'] = get_constraints_info(feature_model.get_constraints())
    return result


def get_tree_info(feature: Feature) -> Dict[str, Any]:
    feature_info: Dict[str, Any] = {}
    feature_info['name'] = safename(feature.name)
    feature_info['abstract'] = str(feature.is_abstract)

    relations: List[Dict[str, Any]] = []
    for relation in feature.get_relations():
        relation_info: Dict[str, Any] = {}
        relation_type = JSONFeatureType.FEATURE.value
        if relation.is_alternative():
            relation_type = JSONFeatureType.XOR.value
        elif relation.is_or():
            relation_type = JSONFeatureType.OR.value
        elif relation.is_mutex():
            relation_type = JSONFeatureType.MUTEX.value
        elif relation.is_cardinal():
            relation_type = JSONFeatureType.CARDINALITY.value
        elif relation.is_mandatory():
            relation_type = JSONFeatureType.MANDATORY.value
        elif relation.is_optional():
            relation_type = JSONFeatureType.OPTIONAL.value
        relation_info['type'] = relation_type
        relation_info['card_min'] = relation.card_min
        relation_info['card_max'] = relation.card_max
        children: List[Dict[str, Any]] = []
        for child in relation.children:
            children.append(get_tree_info(child))
        relation_info['children'] = children
        relations.append(relation_info)

    feature_info['relations'] = relations

    # Attributes
    attributes_info = get_attributes_info(feature.get_attributes())
    if attributes_info:
        feature_info['attributes'] = attributes_info
    return feature_info


def get_attributes_info(attributes: List[Attribute]) -> List[Dict[str, Any]]:
    attributes_info: List[Dict[str, Any]] = []
    for attribute in attributes:
        attr_info: Dict[str, Any] = {}
        attr_info['name'] = safename(attribute.name)
        if attribute.default_value is not None:
            attr_info['value'] = attribute.default_value
        attributes_info.append(attr_info)
    return attributes_info


def get_constraints_info(constraints: List[Constraint]) -> List[Dict[str, Any]]:
    constraints_info: List[Dict[str, Any]] = []
    for ctc in constraints:
        ctc_info: Dict[str, Any] = {}
        ctc_info['name'] = ctc.name
        ctc_info['expr'] = ctc.ast.pretty_str()
        ctc_info['ast'] = get_ctc_info(ctc.ast.root)
        constraints_info.append(ctc_info)
    return constraints_info


def get_ctc_info(ast_node: Node) -> Dict[str, Any]:
    ctc_info: Dict[str, Any] = {}
    if ast_node.is_term():
        ctc_info['type'] = JSONFeatureType.FEATURE.value
        ctc_info['operands'] = [safename(str(ast_node.data))]
    else:
        ctc_info['type'] = ast_node.data.value
        operands: List[Dict[str, Any]] = []
        left = get_ctc_info(ast_node.left)
        operands.append(left)
        if ast_node.right is not None:
            right = get_ctc_info(ast_node.right)
            operands.append(right)
        ctc_info['operands'] = operands
    return ctc_info


def safename(name: str) -> str:
    return f'"{name}"' if any(char not in safecharacters() for char in name) else name


def safecharacters() -> str:
    return string.ascii_letters + string.digits + '_'
