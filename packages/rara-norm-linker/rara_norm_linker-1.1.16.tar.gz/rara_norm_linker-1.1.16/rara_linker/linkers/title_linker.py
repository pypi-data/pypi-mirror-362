from pprint import pprint
from rara_linker.config import LOGGER, EntityType
from rara_linker.kata_config import TITLEConfig
from rara_linker.linkers.base_linker import BaseLinker
from rara_linker.linkers.linking_result import LinkingResult
import logging

logger = LOGGER


class TitleLinker(BaseLinker):
    def __init__(self, **config) -> None:
        conf = TITLEConfig(**config)
        super().__init__(conf)
        
    @property
    def entity_type(self) -> str:
        return EntityType.TITLE
    
    def link(self, entity: str, **kwargs) -> LinkingResult:
        self.es_linker.search_field = self.config.search_field
        result = self.link_entity(entity=entity, **kwargs)
        if not result.linked_info:
            logger.debug(
                f"Could not find any Estonian matches for entity '{entity}'. " \
                f"Searching English matches..."
            )
            result = self.link_entity(entity=entity, **kwargs)
        return result