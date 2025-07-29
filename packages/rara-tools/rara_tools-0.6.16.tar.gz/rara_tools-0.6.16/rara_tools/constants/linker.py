COMPONENT_KEY = "linker"


class Tasks:
    BASE = "base_linker_task"
    VECTORIZE = "vectorize_text"
    VECTORIZE_WITH_CORE = "vectorize_text_with_core_logic"
    PIPELINE = "link_keywords_with_core_logic"

    LINK_AND_NORMALIZE = "core_linker_with_normalization"
    VECTORIZE_AND_INDEX = "core_vectorize_and_index"
    RECEIVE_LINK_AND_NORMALIZE = "receive_link_and_normalize"


class Queue:
    LINKER = "linker"
    VECTORIZER = "vectorizer"


class StatusKeys:
    VECTORIZE_CONTEXT = "vectorize_context"
    LINK_KEYWORDS = "link_keywords"
