from abc import ABC
from dataclasses import dataclass

class ObjectID(ABC):
    def __init__(self, object_id: str):
        self._id = object_id

    def __eq__(self, other: "ObjectID"):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)
    
    def __str__(self):
        return self._id
    
    def __repr__(self):
        return "{class_}(id={id})".format(class_=self.__class__.__name__, id=self._id)

class EntityID(ObjectID):
    def __init__(self, entity_id: str):
        if not entity_id.startswith('Q'):
            raise ValueError('EntityID must start with Q')
        super().__init__(entity_id)

class RelationID(ObjectID):
    def __init__(self, relation_id: str):
        if not relation_id.startswith('P'):
            raise ValueError('RelationID must start with P')
        super().__init__(relation_id)

class Object(ABC):
    def __init__(self, object_id: ObjectID):
        self.id = object_id

    def __eq__(self, other: "Object"):
        if not isinstance(other, Object):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return "{class_}(id={id})".format(class_=self.__class__.__name__, id=self.id)

class Entity(Object):
    def __init__(self, entity_id: str | EntityID, aliases: list[str], text: str | None = None):
        if isinstance(entity_id, str):
            entity_id = EntityID(entity_id)
        super().__init__(entity_id)
        self.aliases = aliases
        self.text = text

class Relation(Object):
    def __init__(self, relation_id: str | RelationID, aliases: list[str], text: str | None = None):
        if isinstance(relation_id, str):
            relation_id = RelationID(relation_id)
        super().__init__(relation_id)
        self.aliases = aliases
        self.text = text

@dataclass
class Compositional32QuestionData:
    support_entity_1: Entity
    support_entity_2: Entity
    parent_support_entity_1: Entity
    parent_support_entity_2: Entity
    relation_support_1: Relation
    relation_support_2: Relation
    question_entity: Entity
    relation_main_support_1: Relation
    relation_main_support_2: Relation
    answer_entity: Entity
    question_relation: Relation

    def __hash__(self):
        return hash((self.support_entity_1, self.support_entity_2, self.parent_support_entity_1, self.parent_support_entity_2, self.relation_support_1, self.relation_support_2, self.question_entity, self.relation_main_support_1, self.relation_main_support_2, self.answer_entity, self.question_relation))
    
    def __eq__(self, other: "Compositional32QuestionData"):
        return (self.support_entity_1, self.support_entity_2, self.parent_support_entity_1, self.parent_support_entity_2, self.relation_support_1, self.relation_support_2, self.question_entity, self.relation_main_support_1, self.relation_main_support_2, self.answer_entity, self.question_relation) == (other.support_entity_1, other.support_entity_2, other.parent_support_entity_1, other.parent_support_entity_2, other.relation_support_1, other.relation_support_2, other.question_entity, other.relation_main_support_1, other.relation_main_support_2, other.answer_entity, other.question_relation)
    
    def __repr__(self):
        return "{class_}(support_entity_1={support_entity_1}, support_entity_2={support_entity_2}, parent_support_entity_1={parent_support_entity_1}, parent_support_entity_2={parent_support_entity_2}, relation_support_1={relation_support_1}, relation_support_2={relation_support_2}, question_entity={question_entity}, relation_main_support_1={relation_main_support_1}, relation_main_support_2={relation_main_support_2}, answer_entity={answer_entity}, question_relation={question_relation})".format(class_=self.__class__.__name__, support_entity_1=self.support_entity_1, support_entity_2=self.support_entity_2, parent_support_entity_1=self.parent_support_entity_1, parent_support_entity_2=self.parent_support_entity_2, relation_support_1=self.relation_support_1, relation_support_2=self.relation_support_2, question_entity=self.question_entity, relation_main_support_1=self.relation_main_support_1, relation_main_support_2=self.relation_main_support_2, answer_entity=self.answer_entity, question_relation=self.question_relation)
    
    def to_id_dict(self):
        return {
            "support_entity_1": str(self.support_entity_1.id),
            "support_entity_2": str(self.support_entity_2.id),
            "parent_support_entity_1": str(self.parent_support_entity_1.id),
            "parent_support_entity_2": str(self.parent_support_entity_2.id),
            "relation_support_1": str(self.relation_support_1.id),
            "relation_support_2": str(self.relation_support_2.id),
            "question_entity": str(self.question_entity.id),
            "relation_main_support_1": str(self.relation_main_support_1.id),
            "relation_main_support_2": str(self.relation_main_support_2.id),
            "answer_entity": str(self.answer_entity.id),
            "question_relation": str(self.question_relation.id)
        }