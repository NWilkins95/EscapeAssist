from concurrent.futures import ThreadPoolExecutor, as_completed


def chunk_text(text: str, max_chars: int = 8000):
    """
    Split Markdown text into chunks while avoiding splits inside tables.

    Args:
        text: Full Markdown string extracted from the PDF.
        max_chars: Maximum character length per chunk.

    Yields:
        Markdown chunks that respect table boundaries.
    """
    lines = text.splitlines(keepends=True)
    current_chunk = []
    current_length = 0
    inside_table = False

    def is_table_line(line: str) -> bool:
        """
        Determine whether a line appears to be part of a Markdown table.

        Args:
            line: A single line of text.

        Returns:
            True if the line resembles table content, otherwise False.
        """
        stripped = line.strip()
        return stripped.startswith("|") or ("|" in stripped and "---" not in stripped)

    for line in lines:
        line_is_table = is_table_line(line)

        if line_is_table and not inside_table:
            inside_table = True
        elif not line_is_table and inside_table:
            inside_table = False

        if current_length + len(line) > max_chars and not inside_table:
            yield "".join(current_chunk)
            current_chunk = []
            current_length = 0

        current_chunk.append(line)
        current_length += len(line)

    if current_chunk:
        yield "".join(current_chunk)


def llm_cleaning(raw_md: str, client) -> str:
    """
    Clean and reorganize extracted Markdown using chunked LLM processing.

    Steps per chunk:
        1. Cleanup pass (remove TOC, fix tables, normalize formatting)
        2. Reorganization pass (group related content under headings)

    Args:
        raw_md: Raw Markdown extracted from Docling.
        client: OpenAI client used for cleanup and reorganization.

    Returns:
        A fully cleaned and reorganized Markdown document.
    """
    if client is None:
        raise RuntimeError(
            "OpenAI client not configured. Set OPENAI_API_KEY or source .env before running."
        )

    chunks = list(chunk_text(raw_md))
    print(f"Total chunks: {len(chunks)}")

    def process_chunk(idx, chunk):
        """
        Clean and reorganize a single Markdown chunk.

        Args:
            idx: Chunk index.
            chunk: Raw Markdown chunk.

        Returns:
            Tuple of (index, cleaned_and_reorganized_markdown).
        """
        cleaning_prompt = f"""
            You are cleaning text extracted from a PDF.

            Rules:
            1. Remove any Table of Contents sections.
            2. Fix broken Markdown tables.
            3. Preserve ALL real content exactly as written.
            4. Do NOT interpret the text.
            5. Do NOT hallucinate or invent content.
            6. Maintain Markdown formatting.
            7. Return ONLY cleaned Markdown.
            8. Do NOT wrap the output in triple backtick code fences.

            Here is the chunk to clean:
            {chunk}
            """

        cleaning_response = client.responses.create(
            model="gpt-4o-mini",
            input=cleaning_prompt,
            temperature=0,
            max_output_tokens=3000,
        )

        cleaned = cleaning_response.output_text

        reorganize_prompt = f"""
            You will reorganize a Markdown document into clean, logical sections.

            Rules:
            1. Do NOT rewrite, summarize, shorten, or expand any content.
            2. Preserve ALL text exactly as written.
            3. Group related content under consistent headings.
            4. Normalize headings if needed (e.g., use ## for major sections).
            5. Do NOT remove warnings, notes, steps, lists, or tables.
            6. Do NOT hallucinate or add new content.
            7. Maintain valid Markdown formatting.
            8. Do NOT wrap the output in triple backtick code fences.

            Here is the cleaned Markdown to reorganize:
            {cleaned}
            """

        reorganize_response = client.responses.create(
            model="gpt-4o-mini",
            input=reorganize_prompt,
            temperature=0,
            max_output_tokens=3000,
        )

        organized = reorganize_response.output_text

        print(f"Chunk {idx + 1}/{len(chunks)} cleaned + reorganized")
        return idx, organized

    processed_chunks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(process_chunk, idx, chunk)
            for idx, chunk in enumerate(chunks)
        ]
        for future in as_completed(futures):
            processed_chunks.append(future.result())

    processed_chunks.sort(key=lambda x: x[0])
    ordered = [c for _, c in processed_chunks]

    print("All chunks processed. Combining final Markdown.")
    return "\n".join(ordered)