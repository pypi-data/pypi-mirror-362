from typing import List, Tuple, Any
from rara_tools.constants.subject_indexer import (
    EntityType, KeywordType, KeywordMARC, KeywordSource, URLSource,
    KEYWORD_TYPE_MAP, KEYWORD_MARC_MAP, KEYWORD_TYPES_TO_IGNORE,
    EMS_ENTITY_TYPES, SIERRA_ENTITY_TYPES, VIAF_ENTITY_TYPES
)

def _get_keyword_source(linked_doc: Any, entity_type: str, is_linked: bool
) -> str:
    """ Find keyword source.
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

def _find_indicators(entity_type: str, entity: str,
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


def format_keywords(flat_keywords: List[dict]) -> dict:
    """ Formats unlinked keywords for Kata CORE.
    """
    ignored_keywords = []
    filtered_keywords = []

    for keyword_dict in flat_keywords:
        keyword_type = keyword_dict.get("entity_type")
        if keyword_type in KEYWORD_TYPES_TO_IGNORE:
            ignored_keywords.append(keyword_dict)
        else:
            filtered_keywords.append(keyword_dict)

    formatted_keywords = {
        "keywords": [],
        "other": ignored_keywords
    }

    for keyword_dict in filtered_keywords:
        original_keyword = keyword_dict.get("keyword")
        keyword_type = keyword_dict.get("entity_type")
        entity_type = KEYWORD_TYPE_MAP.get(keyword_type, "")
        marc_field = KEYWORD_MARC_MAP.get(str(keyword_type), "")
        lang = keyword_dict.get("language", "")

        ind1, ind2 = _find_indicators(
            entity_type=entity_type,
            entity=original_keyword,
            is_linked=False
        )
        keyword_source = _get_keyword_source(
            linked_doc=None,
            is_linked=False,
            entity_type=entity_type
        )
        new_keyword_dict = {
            "dates": "",
            "indicator1": ind1,
            "indicator2": ind2,
            "is_linked": False,
            "keyword_source": keyword_source,
            "lang": lang,
            "location": "",
            "marc_field": marc_field,
            "numeration": "",
            "organisation_sub_unit": "",
            "original_keyword": original_keyword,
            "persons_title": "",
            "url": "",
            "url_source": ""
        }
        new_keyword_dict.update(keyword_dict)
        formatted_keywords["keywords"].append(new_keyword_dict)

    return formatted_keywords
