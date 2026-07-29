from unstructured.chunking.title import chunk_by_title
from unstructured.documents.elements import Element


def chunk_elements(
    elements: list[Element],
    max_characters: int = 2000,
    combine_text_under_n_chars: int = 200,
    new_after_n_chars: int = 200,
    multipage_sections: bool = True,
) -> list[Element]:
    return chunk_by_title(
        elements,
        max_characters=max_characters,
        combine_text_under_n_chars=combine_text_under_n_chars,
        new_after_n_chars=new_after_n_chars,
        multipage_sections=multipage_sections,
    )
