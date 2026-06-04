---
name: Create Ebook Reference List
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a formatted reference list for an ebook with proper citation styles, source categorization, and link validation.
tags: [ebook, references, citations, bibliography, sources]
role: research-analyst
model: any
trigger: When the user asks for ebook references, bibliography, citations, or source list.
---

# Create Ebook Reference List

Generate a professional reference list for an ebook.

## Citation Styles

### APA (Social Sciences)
Author, A. A. (Year). *Title of work*. Publisher. URL

### MLA (Humanities)
Author. *Title of Work*. Publisher, Year. URL.

### Chicago (General)
Author, *Title* (Place: Publisher, Year), page. URL.

### IEEE (Technical)
[1] A. Author, "Title of paper," in *Title of Book*, City, State, Country: Publisher, year, pp. xxx-xxx.

## Source Categories

- **Books**: Monographs, edited collections
- **Articles**: Journal, magazine, blog posts
- **Documentation**: Official docs, API references
- **Data**: Datasets, reports, surveys
- **Media**: Talks, podcasts, videos

## Output Format

```markdown
## References

### Books
1. Author, A. (2024). *Title*. Publisher. https://example.com/book

### Articles
2. Author, B. (2024). "Article Title." *Journal Name*, Vol(Issue), pp-pp.

### Documentation
3. Company. (2024). *Product Documentation*. https://docs.example.com

### Data Sources
4. Organization. (2024). *Report Title* (Dataset). https://example.com/dataset

---

## Source Quality Audit
| Source | Type | Credibility | URL Valid |
|--------|------|-------------|-----------|
| [Author] | Book | High | ✅ |
```
