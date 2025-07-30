import os
from typing import List, Tuple
from rara_linker.config import (
    LOGGER, EntityType, KeywordType, URLSource, KeywordSource,
    KEYWORD_TYPE_MAP, KEYWORD_TYPES_TO_IGNORE,
    KEYWORD_MARC_MAP, URL_SOURCE_MAP,
    EMS_ENTITY_TYPES, SIERRA_ENTITY_TYPES, VIAF_ENTITY_TYPES
)
from rara_linker.exceptions import InvalidInputError
from rara_linker.linkers.ems_linker import EMSLinker
from rara_linker.linkers.linking_result import LinkingResult, LinkedDoc
from rara_linker.linkers.loc_linker import LocationLinker
from rara_linker.linkers.org_linker import OrganizationLinker
from rara_linker.linkers.per_linker import PersonLinker
from rara_linker.linkers.title_linker import TitleLinker
from rara_linker.tools.vectorizer import Vectorizer

from rara_tools.parsers.marc_records.person_record import PersonRecord
from rara_tools.parsers.marc_records.organization_record import OrganizationRecord
from rara_tools.parsers.marc_records.title_record import TitleRecord
from rara_tools.parsers.marc_records.ems_record import EMSRecord

logger = LOGGER

ALLOWED_ENTITY_TYPES = [
    EntityType.PER,
    EntityType.ORG,
    EntityType.KEYWORD,
    EntityType.LOC,
    EntityType.TITLE,
    EntityType.UNK,
]

DEFAULT_FUZZINESS = 2


class Linker:
    def __init__(
            self,
            add_viaf_info: bool = False,
            vectorizer_or_dir_path: str | Vectorizer = os.path.join(".", "vectorizer_data"),
            per_config: dict = {},
            org_config: dict = {},
            loc_config: dict = {},
            ems_config: dict = {},
            title_config: dict = {}
    ):
        self.vectorizer: Vectorizer = self._handle_vectorizer_load(vectorizer_or_dir_path)

        per_config.update({"vectorizer": self.vectorizer})
        org_config.update({"vectorizer": self.vectorizer})

        self.per_linker: PersonLinker = PersonLinker(**per_config)
        self.org_linker: OrganizationLinker = OrganizationLinker(**org_config)
        self.ems_linker: EMSLinker = EMSLinker(**ems_config)
        self.loc_linker: LocationLinker = LocationLinker(**loc_config)
        self.title_linker: TitleLinker = TitleLinker(**title_config)
        self.add_viaf_info: bool = add_viaf_info
        self.linkers_map: dict = {
            EntityType.PER: self.per_linker,
            EntityType.ORG: self.org_linker,
            EntityType.LOC: self.loc_linker,
            EntityType.KEYWORD: self.ems_linker,
            EntityType.TITLE: self.title_linker
        }
        self.url_source_map: dict = URL_SOURCE_MAP

    def _handle_vectorizer_load(self, path_or_instance) -> Vectorizer:
        if isinstance(path_or_instance, str):
            return Vectorizer(path_or_instance)
        elif isinstance(path_or_instance, Vectorizer):
            return path_or_instance

        raise ValueError("Inserted value is not the expected str or Vectorizer type!")

    def execute_all_linkers(self, entity: str, **kwargs) -> LinkingResult:
        temp = []
        for entity_type, linker in self.linkers_map.items():
            logger.debug(f"Searching {entity_type} matches for entity '{entity}'...")
            linked = linker.link(entity=entity, add_viaf_info=self.add_viaf_info, **kwargs)
            if linked.linked_info:
                if not linked.linked_info[0].elastic:
                    LOGGER.info(
                        f"Found only VIAF matches for entity '{entity}' with entity_type='{entity_type}'. " \
                        f"Continuing until Sierra/EMS matches are detected or until all entity types are checked."
                    )
                    temp.append(linked)
                else:
                    break
        if not linked.linked_info:
            if temp:
                entity_types = [linked_doc.entity_type for linked_doc in temp]
                LOGGER.debug(
                    f"Found VIAF matches for the following entity types: {entity_types}."
                )
                LOGGER.warning(
                    f"Returning only the first match in the array (for entity_type={entity_types[0]}). " \
                    f"This might not be correct!"
                )
                linked = temp[0]
            else:
                logger.debug(f"No matches found for entity '{entity}'.")
                linked.entity_type = EntityType.UNK
        return linked

    def link(self, entity: str, **kwargs) -> LinkingResult:
        if not isinstance(entity, str) or not entity.strip():
            raise InvalidInputError(f"Invalid value for entity: '{entity}'.")

        entity_type = kwargs.get("entity_type", None)
        if entity_type:
            if entity_type not in ALLOWED_ENTITY_TYPES:
                raise InvalidInputError(
                    f"Invalid entity type '{entity_type}'. " \
                    f"Supported entity types are: {ALLOWED_ENTITY_TYPES}"
                )
            else:
                linker = self.linkers_map.get(entity_type)
                logger.debug(f"Searching {entity_type} matches for entity '{entity}'...")
                linked = linker.link(entity=entity, add_viaf_info=self.add_viaf_info, **kwargs)
        else:
            LOGGER.debug("Executing first round with fuzziness=0")
            fuzziness = kwargs.pop("fuzziness", DEFAULT_FUZZINESS)
            linked = self.execute_all_linkers(
                entity=entity,
                fuzziness=0,
                **kwargs
            )
            if not linked.linked_info:
                LOGGER.debug(f"Executing second round with fuzziness={fuzziness}")
                linked = self.execute_all_linkers(
                    entity=entity,
                    fuzziness=fuzziness,
                    **kwargs
                )
        return linked

    def _get_identifier_url(self, linked_doc: LinkedDoc | None,
            entity_type: str
    ) -> dict:
        """ Finds URL identifier from LinkedDoc based on
        given entity type.

        Parameters
        -----------
        linked_doc: LinkedDoc | None
            A LinkedDoc class instance.
        entity_type: str
            Entity type for detecting correct URL source.

        Returns
        ----------
        dict:
            Dictionary with keys `url` - URL identifier and
            `url_source` - source of the URL (e.g. "EMS").

        """
        url_source = self.url_source_map.get(entity_type, "")
        url = ""

        if linked_doc:
            if url_source == URLSource.EMS:
                url = linked_doc.elastic.get("ems_url", "")
            elif url_source == URLSource.VIAF:
                url = linked_doc.viaf.get("parsed", {}).get("viaf_url", "")
        if not url:
            url_source = ""
        identifier_url = {"url": url, "url_source": url_source}
        LOGGER.debug(
            f"Detected URL info: {identifier_url}. Used entity_type = {entity_type}. " \
            f"URL source map = {self.url_source_map}."
        )
        return identifier_url

    def _get_keyword_source(self, linked_doc: LinkedDoc | None,
            entity_type: str, is_linked: bool
    ) -> str:
        """ Find keyword source
        """
        if not is_linked:
            source = KeywordSource.AI
        elif entity_type in EMS_ENTITY_TYPES:
            source = KeywordSource.EMS
        elif entity_type in SIERRA_ENTITY_TYPES:
            if linked_doc and linked_doc.elastic:
                source = KeywordSource.SIERRA
            elif linked_doc and linked_doc.viaf:
                source = KeywordSource.VIAF
            else:
                source = KeywordSource.AI
        else:
            source = KeywordSource.AI
        return source

    def _find_indicators(self, entity_type: str, entity: str,
            is_linked: bool
    ) -> Tuple[str, str]:
        """ Find MARC indicators 1 and 2.
        """
        ind1 = " "
        ind2 = " "
        if entity_type in SIERRA_ENTITY_TYPES:
            if entity_type == EntityType.PER:
                if "," in entity:
                    ind1 = "1"
                else:
                    ind1 = "0"
            else:
                # 1 märksõna esimeseks elemendiks võimupiirkonna nimi, nt:
                #    (a) Eesti (b) Riigikogu - raske automaatselt määrata
                # 2 märksõna esimeseks elemendiks nimi pärijärjestuses
                ind1 = "2"
            if not is_linked:
                ind2 = "4"
        elif entity_type in EMS_ENTITY_TYPES:
            ind2 = "4"
        return (ind1, ind2)

    def link_keywords(self, keywords: List[dict], use_viaf: bool = True,
            main_taxonomy_lang: str = "et", context: str = "", query_vector: List[float] = [],
            **kwargs
    ) -> dict:
        """ Applies linking onto rara-subject-indexer flat output.

        Parameters
        -----------
        keywords: List[dict]
            rara-subject-indexer `apply_indexer` output with param `flat=True`.
        use_viaf: bool
            If enabled, VIAF queries are used for linking / enriching the output.
        main_taxnomy_lang: str
            Language of the linked keywords. NB! Currently assumes that only
            one language is used, but might not be true in the future +
            keyword linked only via VIAF might not be in the specifiad language
            as well.

        Returns
        ----------
        dict
            Dictionary with keys "keywords" - has the same structure as the input,
            but each keyword dict contains additional fields "marc_field", "is_linked",
            "original_keyword" + value in field "keyword" is updated with the linked keyword.

        """
        if use_viaf:
            self.add_viaf_info = True

        new_keywords = []
        filtered_keywords = []
        ignored_keywords = []
        categories = []

        for keyword_dict in keywords:
            keyword_type = keyword_dict.get("entity_type")
            keyword = keyword_dict.get("keyword")

            if keyword_type in KEYWORD_TYPES_TO_IGNORE:
                if keyword_type == KeywordType.CATEGORY:
                    categories.append(keyword)
                ignored_keywords.append(keyword_dict)
            else:
                filtered_keywords.append(keyword_dict)


        for keyword_dict in filtered_keywords:
            keyword = keyword_dict.get("keyword")
            keyword_type = keyword_dict.get("entity_type")
            entity_type = KEYWORD_TYPE_MAP.get(keyword_type, "")

            lang = keyword_dict.get("language", "")

            # Fallback URL info, this will be
            # overwritten for linked keywords
            url_info = self._get_identifier_url(
                linked_doc=None,
                entity_type=entity_type
            )
            # Fields
            persons_title = ""
            dates = ""
            location = ""
            organisation_sub_unit = ""
            numeration = ""

            try:
                # Keep highest only:
                # if enabled, only results with max similarity are returned
                # otherwise all that surpass the min threshold
                if keyword_type == KeywordType.TOPIC:
                    allowed_categories = categories
                    keep_highest_only = False
                else:
                    allowed_categories = []
                    keep_higest_only = True

                linked_keyword = self.link(
                    entity=keyword,
                    entity_type=entity_type,
                    lang=lang,
                    categories=allowed_categories,
                    keep_highest_only=keep_highest_only,
                    context=context,
                    query_vector=query_vector,
                    **kwargs
                )
                if linked_keyword.linked_info:
                    first_doc = linked_keyword.linked_info[0]
                    keyword_value = first_doc.linked_entity
                    url_info = self._get_identifier_url(
                        linked_doc=first_doc,
                        entity_type=entity_type
                    )
                    is_linked = True
                    LOGGER.debug(
                        f"Linking keyword '{keyword}' successful. New value = '{keyword_value}'."
                    )
                    if entity_type == EntityType.PER:
                        if first_doc.json:

                            original_record = PersonRecord(first_doc.json)
                            persons_title = original_record.name_specification
                            dates = original_record.life_years
                            numeration = original_record.original_name.get("b", "")

                    elif entity_type == EntityType.ORG:
                        if first_doc.json:
                            original_record = OrganizationRecord(first_doc.json)
                            dates = original_record.dates
                            location = original_record.location
                            organisation_sub_unit = original_record.original_name.get("b", "")
                            keyword_value = original_record.original_name.get("a", "")
                            numeration = original_record.numeration

                else:
                    keyword_value = keyword
                    is_linked = False
                    first_doc = None

                    LOGGER.debug(
                        f"No matches detected for keyword '{keyword}'. " \
                        f"Keeping the original value: '{keyword_value}'."
                    )
            except Exception as e:
                LOGGER.error(f"Linking keyword '{keyword}' failed with error: {e}")
                keyword_value = keyword
                is_linked = False
                first_doc = None

            keyword_source = self._get_keyword_source(
                linked_doc=first_doc,
                is_linked=is_linked,
                entity_type=entity_type
            )
            ind1, ind2 = self._find_indicators(
                entity_type=entity_type,
                entity=keyword_value,
                is_linked=is_linked
            )

            keyword_dict.update(
                {
                    "keyword": keyword_value,
                    "original_keyword": keyword,
                    "is_linked": is_linked,
                    "marc_field": KEYWORD_MARC_MAP.get(str(keyword_type), ""),
                    "keyword_source": keyword_source,
                    "indicator1": ind1,
                    "indicator2": ind2,
                    "persons_title": persons_title,
                    "location": location,
                    "dates": dates,
                    "organisation_sub_unit": organisation_sub_unit,
                    "numeration": numeration
                }
            )
            keyword_dict.update(url_info)
            if is_linked:
                keyword_dict.update({"lang": main_taxonomy_lang})
            new_keywords.append(keyword)
        out = {"keywords": filtered_keywords, "other": ignored_keywords}
        return out
