from datetime import datetime

class Note:

    def __init__(self, title, text, tags=None):
        uniq_tags = [*{*tags}]
        self.title = title
        self.text = text
        self.tags = uniq_tags or []
        self.created_at = datetime.now()
        self.edited_at = datetime.now()
        self.id = self.created_at.timestamp()
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags = [t for t in self.tags if t != tag]

    def __str__(self):
        tags = ", ".join(self.tags)
        return (
            f"ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Note: {self.text}\n"
            f"Tags: {tags or 'No tags'}\n"
            f"Created: {self.created_at}\n"
            "───────────────────────────\n"
        )
