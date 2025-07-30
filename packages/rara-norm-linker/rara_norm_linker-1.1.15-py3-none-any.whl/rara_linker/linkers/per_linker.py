import logging
from typing import NoReturn
from rara_linker.linkers.base_linker import BaseLinker
from rara_linker.tools.normalizers import PersonNormalizer
from rara_linker.linkers.linking_result import LinkingResult
from rara_linker.config import LOGGER, EntityType
from rara_linker.kata_config import PERConfig

class PersonLinker(BaseLinker):
    def __init__(self, **config) -> None:
        conf = PERConfig(**config)
        super().__init__(conf, **{"vectorizer": config.get("vectorizer", None)})
        
    @property
    def entity_type(self) -> str:
        return EntityType.PER
    
    def link(self, entity: str, **kwargs) -> LinkingResult:
        result = self.link_entity(entity=entity, **kwargs)
        if not result.linked_info and PersonNormalizer.has_cyrillic(entity):
            latin_entity = PersonNormalizer.transliterate(entity)
            result = self.link_entity(entity=latin_entity, **kwargs)
            result.original_entity = entity  
        return result
        
