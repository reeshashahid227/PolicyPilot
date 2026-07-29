def format_citations(retrieved_chunks):
    """
    Create a clean list of unique sources
    from retrieved chunks.
    """

    citations = []
    seen = set()

    for chunk in retrieved_chunks:

        metadata = chunk.get("metadata", {})

        source = metadata.get("source", "Unknown source")
        section = metadata.get("section", "")

        citation_key = (source, section)

        if citation_key in seen:
            continue

        seen.add(citation_key)

        citation = {
            "source": source,
            "section": section
        }

        citations.append(citation)

    return citations