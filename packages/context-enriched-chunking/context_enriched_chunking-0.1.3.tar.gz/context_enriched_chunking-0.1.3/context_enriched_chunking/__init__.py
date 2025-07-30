from langchain_text_splitters import RecursiveCharacterTextSplitter

class ContextEnrichedChunking:
    def __init__(self, section_max_words=10, chunk_size=1000, chunk_overlap=100):
        self.section_max_words = section_max_words
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_text(self, text, title):
        # Replace every \n\n with \n
        text = text.replace('\n\n', '\n')
        # Join lines that do not end with punctuation
        lines = text.strip().splitlines()
        joined_lines = []
        buffer = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if buffer:
                buffer += " " + line
            else:
                buffer = line
            if (buffer and buffer[-1] in '.!?') or len(line.split()) <= self.section_max_words:
                joined_lines.append(buffer)
                buffer = ""
        if buffer:
            joined_lines.append(buffer)

        chunks = []
        section = None
        for line in joined_lines:
            if len(line.split()) <= self.section_max_words:
                section = line
                chunk = f"Content: {section}"
                if title:
                    chunk = f"Title: {title}\n" + chunk
                chunks.append(chunk)
            else:
                if not line.strip():
                    continue
                contents = self.recursive_text_splitter.split_text(line)
                n_contents = len(contents)
                for i, content in enumerate(contents):
                    part = f"(Part {i+1}/{n_contents}) " if n_contents > 1 else ""
                    chunk = f"Content: {part}{content}"
                    if section:
                        chunk = f"Section: {section}\n" + chunk
                    if title:
                        chunk = f"Title: {title}\n" + chunk
                    chunks.append(chunk)
        return chunks