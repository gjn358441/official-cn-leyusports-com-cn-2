from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    url: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    importance: int = 3

    def __post_init__(self):
        if self.importance < 1 or self.importance > 5:
            raise ValueError("Importance must be between 1 and 5")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "url": self.url,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "importance": self.importance,
        }


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def filter_by_importance(self, min_imp: int = 1, max_imp: int = 5) -> List[KeywordNote]:
        return [note for note in self.notes if min_imp <= note.importance <= max_imp]

    def sort_by_date(self, reverse: bool = False) -> None:
        self.notes.sort(key=lambda n: n.created_at, reverse=reverse)

    def summary(self) -> str:
        lines = []
        lines.append(f"Total notes: {len(self.notes)}")
        if self.notes:
            lines.append(f"Keywords: {', '.join(n.keyword for n in self.notes[:5])}")
            lines.append(f"Tags: {', '.join(set(tag for n in self.notes for tag in n.tags))}")
        return "\n".join(lines)


def format_note_simple(note: KeywordNote) -> str:
    """Simple single-line format for a keyword note."""
    tags_str = ", ".join(note.tags) if note.tags else "no tags"
    desc = note.description or "no description"
    return f"[{note.importance}] {note.keyword} - {desc} (tags: {tags_str}) | {note.url}"


def format_note_detailed(note: KeywordNote) -> str:
    """Multi-line detailed format for a keyword note."""
    lines = []
    lines.append(f"Keyword:    {note.keyword}")
    lines.append(f"URL:        {note.url}")
    lines.append(f"Description: {note.description or 'N/A'}")
    lines.append(f"Tags:       {', '.join(note.tags) if note.tags else 'N/A'}")
    lines.append(f"Importance: {note.importance}/5")
    lines.append(f"Created:    {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    return "\n".join(lines)


def format_collection_table(collection: KeywordNoteCollection) -> str:
    """Format collection as a simple table string."""
    if not collection.notes:
        return "No notes in collection."
    header = f"{'Keyword':<20} {'Importance':<12} {'Tags':<25} {'URL':<30}"
    sep = "-" * len(header)
    rows = []
    for note in collection.notes:
        tags_short = ", ".join(note.tags[:3]) if note.tags else ""
        rows.append(f"{note.keyword:<20} {note.importance:<12} {tags_short:<25} {note.url:<30}")
    return "\n".join([header, sep] + rows)


def demo_usage() -> None:
    """Demonstrate usage with sample data including the target URL and keyword."""
    sample_url = "https://official-cn-leyusports.com.cn"
    sample_keyword = "乐鱼体育"

    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword=sample_keyword,
        url=sample_url,
        description="Official sports portal for 乐鱼体育",
        tags=["sports", "official", "china"],
        importance=5,
    )
    note2 = KeywordNote(
        keyword="足球赛事",
        url=sample_url + "/football",
        description="Live football events and scores",
        tags=["football", "live"],
        importance=4,
    )
    note3 = KeywordNote(
        keyword="篮球分析",
        url=sample_url + "/basketball",
        description="Basketball match analysis",
        tags=["basketball", "analysis"],
        importance=3,
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)

    print("=== Collection Summary ===")
    print(collection.summary())
    print()

    print("=== Detailed note for 乐鱼体育 ===")
    print(format_note_detailed(note1))
    print()

    print("=== Simple format all notes ===")
    for note in collection.notes:
        print(format_note_simple(note))
    print()

    print("=== Table format ===")
    print(format_collection_table(collection))
    print()

    print("=== Filtered by tag 'football' ===")
    football_notes = collection.filter_by_tag("football")
    for note in football_notes:
        print(format_note_simple(note))


if __name__ == "__main__":
    demo_usage()