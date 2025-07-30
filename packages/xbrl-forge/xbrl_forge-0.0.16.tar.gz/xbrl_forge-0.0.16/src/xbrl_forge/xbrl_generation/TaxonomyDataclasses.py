import logging

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .PackageDataclasses import Tag, TagLocation


logger = logging.getLogger(__name__)

@dataclass
class TaxonomyDocument:
    priority: int
    prefix: str
    metadata: 'TaxonomyMetadata'
    namespaces: Dict[str, str]
    schema_imports: Dict[str, str]
    elements: List['TaxonomyElement']
    linkbase_imports: Dict[str, str]
    arc_roles_import: Dict[str, str]
    roles: List['TaxonomyRole']
    labels: Dict[str, List['LabelElement']]

    @property
    def rewrite_path(cls) -> List[str]:
        return [cls.metadata.publisher_url, "xbrl", cls.metadata.publication_date]

    @property
    def namespace(cls) -> str:
        return f"http://{'/'.join(cls.rewrite_path)}"
    
    @property
    def files_base_name(cls) -> str:
        return f"{cls.prefix}-{cls.metadata.publication_date}"

    @property
    def schema_url(cls) -> str:
        return f"{cls.namespace}/{cls.files_base_name}.xsd"
    
    @classmethod
    def new(
        cls,
        prefix: str, 
        metadata: 'TaxonomyMetadata',
        priority: int = 0,
        namespaces: Dict[str, str] = None,
        schema_imports: Dict[str, str] = None,
        elements: List['TaxonomyElement'] = None,
        linkbase_imports: Dict[str, str] = None,
        arc_roles_import: Dict[str, str] = None,
        roles: List['TaxonomyRole'] = None,
        labels: Dict[str, List['LabelElement']] = None
    ) -> 'TaxonomyDocument':
        taxonomy_namespaces: Dict[str, str] = {}
        if namespaces:
            taxonomy_namespaces = namespaces
        taxonomy_schema_imports: Dict[str, str] = {}
        if schema_imports:
            taxonomy_schema_imports = schema_imports
        taxonomy_elements: List['TaxonomyElement'] = []
        if elements:
            taxonomy_elements = elements
        taxonomy_linkbase_imports: Dict[str, str] = {}
        if linkbase_imports:
            taxonomy_linkbase_imports = linkbase_imports
        taxonomy_arc_roles_imports: Dict[str, str] = {}
        if arc_roles_import:
            taxonomy_arc_roles_imports = arc_roles_import
        taxonomy_roles: List['TaxonomyRole'] = []
        if roles:
            taxonomy_roles = roles
        taxonomy_labels: Dict[str, List['LabelElement']] = {}
        if labels:
            taxonomy_labels = labels
        return cls(
            priority=priority,
            prefix=prefix, 
            metadata=metadata,
            namespaces=taxonomy_namespaces,
            schema_imports=taxonomy_schema_imports,
            elements=taxonomy_elements,
            linkbase_imports=taxonomy_linkbase_imports,
            arc_roles_import=taxonomy_arc_roles_imports,
            roles=taxonomy_roles,
            labels=taxonomy_labels
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'TaxonomyDocument':
        return cls.new(
            priority=data.get("priority", 0),
            prefix=data.get("prefix"), 
            metadata=TaxonomyMetadata.from_dict(data.get("metadata", {})),
            namespaces=data.get("namespaces", {}),
            schema_imports=data.get("schema_imports", {}),
            elements=[TaxonomyElement.from_dict(element_data) for element_data in data.get("elements", [])],
            linkbase_imports=data.get("linkbase_imports", {}),
            arc_roles_import=data.get("arc_roles_import", {}),
            roles=[TaxonomyRole.from_dict(role_data) for role_data in data.get("roles", [])],
            labels={labels_lang:[LabelElement.from_dict(label_element) for label_element in labels_data] for labels_lang, labels_data in data.get("labels", {}).items()}
        )

    def add_taxonomy(target_taxonomy, new_taxonomy: "TaxonomyDocument") -> Dict[str, str]:
        # add namespaces if not already known
        target_taxonomy.namespaces = { **new_taxonomy.namespaces, **target_taxonomy.namespaces}
        # add schemas to import
        target_taxonomy.schema_imports = { **new_taxonomy.schema_imports, **target_taxonomy.schema_imports}
        # add new elements, check for name and change it if it already exists with differnt attributes
        element_update_map: Dict[str, str] = {}
        for new_element in new_taxonomy.elements:
            used_elements: Dict[str, TaxonomyElement] = {element.name:element for element in target_taxonomy.elements}
            if not new_element.name in used_elements:
                target_taxonomy.elements.append(new_element)
            else:
                if not used_elements[new_element.name].equals(new_element):
                    index: int = 0
                    new_name: str = f"{new_element.name}_{index}"
                    while new_name in used_elements:
                        index += 1
                        new_name = f"{new_element.name}_{index}"
                    logger.debug(f"Updating concept name because of inconsistent duplication {new_element.name} to {new_name}")  
                    element_update_map[new_element.name] = new_name
                    new_element.name = new_name
                    target_taxonomy.elements.append(new_element)
        # import linkbases if not already imported
        target_taxonomy.linkbase_imports = { **new_taxonomy.linkbase_imports, **target_taxonomy.linkbase_imports}
        # import arc roles if not already imported
        target_taxonomy.arc_roles_import = { **new_taxonomy.arc_roles_import, **target_taxonomy.arc_roles_import}
        # update element references in roles by element_update_map
        for new_role in new_taxonomy.roles:
            new_role.update_elements(element_update_map)
        # merge roles
        target_roles: Dict[str, TaxonomyRole] = {role.href(""):role for role in target_taxonomy.roles}
        for new_role in new_taxonomy.roles:
            new_role_href: str = new_role.href("")
            if new_role_href in target_roles:
                # combine roles
                logger.debug(f"Merging roles with uri {new_role.uri(target_taxonomy.namespace)}")
                target_roles[new_role_href].merge(new_role)
            else:
                # add new role to taxonomy
                target_taxonomy.roles.append(new_role)
        # update element references in labels by element_update_map
        for label_lang in new_taxonomy.labels:
            for label_element in new_taxonomy.labels[label_lang]:
                label_element.update_element(element_update_map)
        # merge labels
        for label_lang in new_taxonomy.labels:
            if not label_lang in target_taxonomy.labels:
                target_taxonomy.labels[label_lang] = []
            for new_label_element in new_taxonomy.labels[label_lang]:
                target_label_elements: Dict[str, LabelElement] = {tar_label_ele.uname:tar_label_ele for tar_label_ele in target_taxonomy.labels[label_lang]}
                # if element not already used for labels, add the element
                if not new_label_element.uname in target_label_elements:
                    target_taxonomy.labels[label_lang].append(new_label_element)
                else:
                    # combine with the existing label
                    target_label_elements[new_label_element.uname].combine(new_label_element)
        return element_update_map

    def to_dict(cls) -> dict:
        return {
            "priority": cls.priority,
            "prefix": cls.prefix,
            "metadata": cls.metadata.to_dict(),
            "namespaces": cls.namespaces,
            "schema_imports": cls.schema_imports,
            "linkbase_imports": cls.linkbase_imports,
            "elements": [element.to_dict() for element in cls.elements],
            "arc_roles_import": cls.arc_roles_import,
            "roles": [role.to_dict() for role in cls.roles],
            "labels": {labels_lang:[label_element.to_dict() for label_element in labels_data] for labels_lang, labels_data in cls.labels.items()}
        }

@dataclass
class TaxonomyMetadata:
    name: str
    description: str
    publisher: str
    publisher_url: str
    publication_date: str
    publisher_country: str
    entrypoints: List['Entrypoint']

    @classmethod
    def new(
        cls,
        name: str,
        description: str, 
        publisher: str,
        publisher_url: str,
        publisher_country: str,
        publication_date: str,
        entrypoints: List['Entrypoint']
    ) -> 'TaxonomyMetadata':
        return cls(
            name=name,
            description=description, 
            publisher=publisher,
            publisher_url=publisher_url,
            publisher_country=publisher_country,
            publication_date=publication_date,
            entrypoints=entrypoints
        )        

    @classmethod
    def from_dict(cls, data: dict) -> 'TaxonomyMetadata':
        return cls.new(
            name=data.get("name"),
            description=data.get("description"), 
            publisher=data.get("publisher"),
            publisher_url=data.get("publisher_url"),
            publisher_country=data.get("publisher_country"),
            publication_date=data.get("publication_date"),
            entrypoints=[Entrypoint.from_dict(entrypoint) for entrypoint in data.get("entrypoints", [])]
        )

    def to_dict(cls) -> dict:
        return {
            "name": cls.name,
            "description": cls.description,
            "publisher": cls.publisher,
            "publisher_url": cls.publisher_url,
            "publisher_country": cls.publisher_country,
            "publication_date": cls.publication_date,
            "entrypoints": [entrypoint.to_dict() for entrypoint in cls.entrypoints]
        }

@dataclass
class Entrypoint:
    name: str
    description: str
    documents: List[str]
    language: str

    @classmethod
    def new(
        cls,
        name: str,
        description: str,
        documents: List[str],
        language: str
    ) -> 'Entrypoint':
        return cls(
            name=name,
            description=description,
            documents=documents,
            language=language
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'Entrypoint':
        return cls.new(
            name=data.get("name"),
            description=data.get("description"),
            documents=data.get("documents", []),
            language=data.get("language")
        )

    def to_dict(cls) -> dict:
        return {
            "name": cls.name,
            "description": cls.description,
            "documents": cls.documents,
            "language": cls.language
        }

@dataclass
class TaxonomyElement:
    balance: str
    period_type: str
    name: str
    nillable: bool
    abstract: bool
    substitution_group: Tag
    type: Tag
    typed_domain_ref: TagLocation

    @classmethod
    def new(
        cls,
        name: str,
        type: Tag,
        nillable: bool = False,
        abstract: bool = False,
        balance: str = None,
        period_type: str = None,
        substitution_group: Tag = None,
        typed_domain_ref: TagLocation = None
    ) -> 'TaxonomyElement':
        return cls(
            balance=balance,
            period_type=period_type,
            name=name,
            nillable=nillable,
            abstract=abstract,
            substitution_group=substitution_group,
            type=type,
            typed_domain_ref=typed_domain_ref
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'TaxonomyElement':
        return cls.new(
            balance=data.get("balance"),
            period_type=data.get("period_type"),
            name=data.get("name"),
            nillable=data.get("nillable"),
            abstract=data.get("abstract"),
            substitution_group=Tag.from_dict(data.get("substitution_group")) if "substitution_group" in data else None,
            type=Tag.from_dict(data.get("type", {})),
            typed_domain_ref=TagLocation.from_dict(data.get("typed_domain_ref")) if "typed_domain_ref" in data else None
        )
    
    def to_uname(cls, namespace: str) -> str:
        return Tag(namespace=namespace, name=cls.name).to_uname()

    def equals(cls, compare_element: "TaxonomyElement") -> bool:
        if cls.balance != compare_element.balance:
            return False
        if cls.period_type != compare_element.period_type:
            return False
        if cls.nillable != compare_element.nillable:
            return False
        if cls.abstract != compare_element.abstract:
            return False
        if cls.substitution_group or compare_element.substitution_group:
            if not cls.substitution_group or not compare_element.substitution_group:
                return False
            if cls.substitution_group.to_uname() != compare_element.substitution_group.to_uname():
                return False
        if cls.type.to_uname() != compare_element.type.to_uname():
            return False
        if cls.typed_domain_ref or compare_element.typed_domain_ref:
            if not cls.typed_domain_ref or not compare_element.typed_domain_ref:
                return False
            if cls.typed_domain_ref.to_url() != compare_element.typed_domain_ref.to_url():
                return False
        return True

    def to_dict(cls) -> dict:
        return {
            "balance": cls.balance,
            "period_type": cls.period_type,
            "name": cls.name,
            "nillable": cls.nillable,
            "abstract": cls.abstract,
            "substitution_group": cls.substitution_group.to_dict() if cls.substitution_group else None,
            "type": cls.type.to_dict(),
            "typed_domain_ref": cls.typed_domain_ref.to_dict() if cls.typed_domain_ref else None
        }

@dataclass
class TaxonomyRole:
    role_name: str
    role_id: str
    role_uri: str
    schema_location: str
    presentation_linkbase: List['PresentationElement']
    definition_linkbase: List['DefinitionElement']
    calculation_linkbase: List['CalculationElement']

    @classmethod
    def new(
        cls,
        role_name: str,
        role_id: str,
        role_uri: str = None,
        schema_location: str = None,
        presentation_linkbase: List['PresentationElement'] = None,
        definition_linkbase: List['DefinitionElement'] = None,
        calculation_linkbase: List['CalculationElement'] = None
    ) -> 'TaxonomyRole':
        role_presentation_linkbase: List['PresentationElement'] = []
        if presentation_linkbase:
            role_presentation_linkbase = presentation_linkbase
        role_definition_linkbase: List['DefinitionElement'] = []
        if definition_linkbase:
            role_definition_linkbase = definition_linkbase
        role_calculation_linkbase: List['CalculationElement'] = []
        if calculation_linkbase:
            role_calculation_linkbase = calculation_linkbase
        return cls(
            role_name=role_name,
            role_id=role_id,
            role_uri=role_uri,
            schema_location=schema_location,
            presentation_linkbase=role_presentation_linkbase,
            definition_linkbase=role_definition_linkbase,
            calculation_linkbase=role_calculation_linkbase
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'TaxonomyRole':
        return cls.new(
            role_name=data.get("role_name"),
            role_id=data.get("role_id"),
            role_uri=data.get("role_uri"),
            schema_location=data.get("schema_location"),
            presentation_linkbase=[PresentationElement.from_dict(element) for element in data.get("presentation_linkbase", [])],
            definition_linkbase=[DefinitionElement.from_dict(element) for element in data.get("definition_linkbase", [])],
            calculation_linkbase=[CalculationElement.from_dict(element) for element in data.get("calculation_linkbase", [])]
        )

    def uri(cls, taxonomy_namespace: str) -> str:
        if not cls.role_uri:
            return f"{taxonomy_namespace.rstrip('/')}/roles/{cls.role_id}"
        return cls.role_uri
    
    def href(cls, file_base_name: str) -> str:
        if not cls.schema_location:
            return f"{file_base_name}.xsd#{cls.role_id}"
        return f"{cls.schema_location}#{cls.role_id}"

    def update_elements(cls, update_element_map: Dict[str, str]) -> None:
        # update presentation
        for pres_element in cls.presentation_linkbase:
            pres_element.update_elements(update_element_map)
        # update definition
        for def_element in cls.definition_linkbase:
            def_element.update_elements(update_element_map)
        # update calculation
        for calc_element in cls.calculation_linkbase:
            calc_element.update_elements(update_element_map)

    def merge(target_role, new_role: "TaxonomyRole") -> None:
        # update presentation linkbase
        new_presentations: List[PresentationElement] = []
        for pres_item in new_role.presentation_linkbase:
            new_presentations += pres_item.deconstruct()
        extsting_pres_relations: List[Tuple[str, str]] = []
        for pres_item in target_role.presentation_linkbase:
            extsting_pres_relations += pres_item.get_relations()
        # clean presentations from the new ones which already exist
        for new_presentation in new_presentations:
            cleaned_children: List[PresentationElement] = []
            # add chold to cleaned children if the relation is not alredy known
            for child in new_presentation.children:
                if not child.get_relation(new_presentation) in extsting_pres_relations:
                    cleaned_children.append(child)
            # replace role children with cleaned and if there are some left add it to the presentation linkbase
            new_presentation.children = cleaned_children
            if new_presentation.children:
                target_role.presentation_linkbase.append(new_presentation)
        # update defintion linkbase
        new_definitions: List[DefinitionElement] = []
        for def_item in new_role.definition_linkbase:
            new_definitions += def_item.deconstruct()
        existing_def_relations: List[Tuple[str, str]] = []
        for def_item in target_role.definition_linkbase:
            existing_def_relations += def_item.get_relations()
        # clean definition from the new ones which already exist
        for new_definition in new_definitions:
            cleaned_children: List[DefinitionElement] = []
            # add child to cleaned children if the relation is not alredy known
            for child in new_definition.children:
                if not child.get_relation(new_definition) in existing_def_relations:
                    cleaned_children.append(child)
            # replace role children and if there are children add to presentation
            new_definition.children = cleaned_children
            if new_definition.children:
                target_role.definition_linkbase.append(new_definition)
        # update calculation linkbase
        new_calculations: List[CalculationElement] = []
        for calc_item in new_role.calculation_linkbase:
            new_calculations += calc_item.deconstruct()
        extsting_calc_relations: List[Tuple[str, str]] = []
        for calc_item in target_role.calculation_linkbase:
            extsting_calc_relations += calc_item.get_relations()
        # if a calculation for a element already exists, do not interfere with it
        parent_calculation_ids: List[str] = [relation[0] for relation in extsting_calc_relations]
        for new_calc in new_calculations:
            if not new_calc.id in parent_calculation_ids:
                target_role.calculation_linkbase.append(new_calc)

    def to_dict(cls) -> dict:
        return {
            "role_name": cls.role_name,
            "role_id": cls.role_id,
            "schema_location": cls.schema_location,
            "presentation_linkbase": [element.to_dict() for element in cls.presentation_linkbase],
            "definition_linkbase": [element.to_dict() for element in cls.definition_linkbase],
            "calculation_linkbase": [element.to_dict() for element in cls.calculation_linkbase]
        }

@dataclass
class LinkbaseElement(TagLocation):
    arc_role: str
    children: List['LinkbaseElement']

    @classmethod
    def new(cls, element_id: str, children: List['LinkbaseElement'], schema_location: str = None, arc_role: str = None) -> 'LinkbaseElement':
        return cls(
            element_id=element_id,
            schema_location=schema_location,
            arc_role=arc_role,
            children=children
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'LinkbaseElement':
        return cls.new(
            element_id=data.get("element_id"),
            schema_location=data.get("schema_location"),
            arc_role=data.get("arc_role"),
            children=[LinkbaseElement.from_dict(child) for child in data.get("children", [])]
        )
    
    @property
    def id(cls) -> str:
        return f"{{{cls.schema_location}}}{cls.element_id}"

    @property
    def extended_id(cls) -> str:
        return cls.id
    
    def get_relation(cls, parent: "LinkbaseElement") -> Tuple[str, str]:
        return (parent.id, cls.extended_id)

    def get_relations(cls) -> List[Tuple[str, str]]:
        relationships: List[Tuple[str, str]] = []
        if cls.children:
            for child in cls.children:
                relationships.append(child.get_relation(cls))
                relationships += child.get_relations()
        return relationships

    def copy(cls, include_children: bool = True) -> "LinkbaseElement":
        raise Exception("The copy function was not implemented on the Base LinkbaseElement Class!")
    
    def deconstruct(cls) -> List["LinkbaseElement"]:
        raise Exception("The deconstruct function was not implemented on the Base LinkbaseElement Class!")
    
    def update_elements(cls, update_element_map: Dict[str, str]) -> None:
        if not cls.schema_location and cls.element_id in update_element_map:
            cls.element_id = update_element_map[cls.element_id]
        for child in cls.children:
            child.update_elements(update_element_map)
    
    def to_dict(cls) -> dict:
        return {
            "element_id": cls.element_id,
            "schema_location": cls.schema_location,
            "arc_role": cls.arc_role,
            "children": [child.to_dict() for child in cls.children]
        }
    
@dataclass
class PresentationElement(LinkbaseElement):
    order: int
    preferred_label: str
    children: List['PresentationElement']

    @classmethod
    def new(
        cls, 
        element_id: str, 
        children: List['PresentationElement'], 
        schema_location: str = None, 
        arc_role: str = None,
        preferred_label: str = None,
        order: int = 0
    ) -> 'PresentationElement':
        return cls(
            element_id=element_id,
            children=children,
            schema_location=schema_location,
            arc_role=arc_role,
            preferred_label=preferred_label,
            order=order
        )
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PresentationElement':
        return cls.new(
            element_id=data.get("element_id"),
            schema_location=data.get("schema_location"),
            arc_role=data.get("arc_role"),
            order=data.get("order", 0),
            preferred_label=data.get("preferred_label"),
            children=[PresentationElement.from_dict(child) for child in data.get("children", [])]
        )

    @property
    def extended_id(cls) -> str:
        return f"{cls.id}_{cls.preferred_label}"

    def copy(cls, include_children: bool = True, include_sub_children: bool = True, include_all_children: bool = True) -> "PresentationElement":
        children: List[PresentationElement] = []
        if include_children:
            children = [child.copy(include_sub_children, include_all_children, include_all_children) for child in cls.children]
        return PresentationElement(
            element_id=cls.element_id,
            schema_location=cls.schema_location,
            arc_role=cls.arc_role,
            order=cls.order,
            preferred_label=cls.preferred_label,
            children=children
        )

    def deconstruct(cls) -> List["PresentationElement"]:
        deconstructed: List["PresentationElement"] = []
        if cls.children:
            deconstructed = [cls.copy(True, False, False)]
            for child in cls.children:
                deconstructed += child.deconstruct()
        return deconstructed

    def to_dict(cls) -> dict:
        return {
            "element_id": cls.element_id,
            "schema_location": cls.schema_location,
            "arc_role": cls.arc_role,
            "order": cls.order,
            "preferred_label": cls.preferred_label,
            "children": [child.to_dict() for child in cls.children]
        }

@dataclass
class CalculationElement(LinkbaseElement):
    weight: int
    children: List['CalculationElement']

    @classmethod
    def new(
        cls, 
        element_id: str, 
        children: List['CalculationElement'], 
        schema_location: str = None, 
        arc_role: str = None,
        weight: int = 1
    ) -> 'CalculationElement':
        return cls(
            element_id=element_id,
            children=children,
            schema_location=schema_location,
            arc_role=arc_role,
            weight=weight
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'CalculationElement':
        return cls.new(
            element_id=data.get("element_id"),
            schema_location=data.get("schema_location"),
            arc_role=data.get("arc_role"),
            weight=data.get("weight", 1),
            children=[CalculationElement.from_dict(child) for child in data.get("children", [])]
        )

    def copy(cls, include_children: bool = True, include_sub_children: bool = True, include_all_children: bool = True) -> "CalculationElement":
        children: List[CalculationElement] = []
        if include_children:
            children = [child.copy(include_sub_children, include_all_children, include_all_children) for child in cls.children]
        return CalculationElement(
            element_id=cls.element_id,
            schema_location=cls.schema_location,
            arc_role=cls.arc_role,
            weight=cls.weight,
            children=children
        )

    def deconstruct(cls) -> List["CalculationElement"]:
        deconstructed: List["CalculationElement"] = []
        if cls.children:
            deconstructed = [cls.copy(True, False, False)]
            for child in cls.children:
                deconstructed += child.deconstruct()
        return deconstructed

    def to_dict(cls) -> dict:
        return {
            "element_id": cls.element_id,
            "schema_location": cls.schema_location,
            "arc_role": cls.arc_role,
            "weight": cls.weight,
            "children": [child.to_dict() for child in cls.children]
        }
    
@dataclass
class DefinitionElement(LinkbaseElement):
    context_element: str
    closed: bool
    children: List['DefinitionElement']

    @classmethod
    def new(
        cls, 
        element_id: str, 
        children: List['DefinitionElement'], 
        schema_location: str = None, 
        arc_role: str = None,
        context_element: str = None,
        closed: bool = None
    ) -> 'DefinitionElement':
        return cls(
            element_id=element_id,
            children=children,
            schema_location=schema_location,
            arc_role=arc_role,
            context_element=context_element,
            closed=closed
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'DefinitionElement':
        return cls.new(
            element_id=data.get("element_id"),
            schema_location=data.get("schema_location"),
            arc_role=data.get("arc_role"),
            context_element=data.get("context_element"),
            closed=data.get("closed"),
            children=[DefinitionElement.from_dict(child) for child in data.get("children", [])]
        )
    
    @property
    def extended_id(cls) -> str:
        return f"{cls.id}_{cls.arc_role}"

    def copy(cls, include_children: bool = True, include_sub_children: bool = True, include_all_children: bool = True) -> "DefinitionElement":
        children: List[DefinitionElement] = []
        if include_children:
            children = [child.copy(include_sub_children, include_all_children, include_all_children) for child in cls.children]
        return DefinitionElement(
            element_id=cls.element_id,
            schema_location=cls.schema_location,
            arc_role=cls.arc_role,
            context_element=cls.context_element,
            closed=cls.closed,
            children=children
        )

    def deconstruct(cls) -> List["DefinitionElement"]:
        deconstructed: List["DefinitionElement"] = []
        if cls.children:
            deconstructed = [cls.copy(True, False, False)]
            for child in cls.children:
                deconstructed += child.deconstruct()
        return deconstructed

    def to_dict(cls) -> dict:
        return {
            "element_id": cls.element_id,
            "schema_location": cls.schema_location,
            "arc_role": cls.arc_role,
            "context_element": cls.context_element,
            "closed": cls.closed,
            "children": [child.to_dict() for child in cls.children]
        }

@dataclass
class LabelElement:
    element_id: str
    schema_location: str
    labels: List['LabelData']
    
    @classmethod
    def new(
        cls,
        element_id: str,
        labels: List['LabelData'],
        schema_location: str = None
    ) -> 'LabelElement':
        return cls(
            element_id=element_id,
            schema_location=schema_location,
            labels=labels
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'LabelElement':
        return cls.new(
            element_id=data.get("element_id"),
            schema_location=data.get("schema_location"),
            labels=[LabelData.from_dict(label_data) for label_data in data.get("labels", [])]
        )
    
    def update_element(cls, update_element_map: Dict[str, str]) -> None:
        if not cls.schema_location and cls.element_id in update_element_map:
            cls.element_id = update_element_map[cls.element_id]
    
    def combine(cls, new_label_element: "LabelElement") -> None:
        used_label_roles: List[str] = [label_data.label_role for label_data in cls.labels]
        for new_label in new_label_element.labels:
            if not new_label.label_role in used_label_roles:
                cls.labels.append(new_label)

    @property
    def uname(cls) -> str:
        return f"{{{cls.schema_location}}}{cls.element_id}"

    def to_dict(cls) -> dict:
        return {
            "element_id": cls.element_id,
            "schema_location": cls.schema_location,
            "labels": [label_data.to_dict() for label_data in cls.labels]
        }

@dataclass
class LabelData:
    label_role: str
    label: str

    @classmethod
    def new(
        cls,
        label: str,
        label_role: str
    ) -> 'LabelData':
        return cls(
            label=label,
            label_role=label_role
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'LabelData':
        return cls.new(
            label_role=data.get("label_role"),
            label=data.get("label")
        )
    
    def to_dict(cls) -> dict:
        return {
            "label_role": cls.label_role,
            "label": cls.label
        }