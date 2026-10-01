# CyberSathy FiberNet Enterprise Documentation v3

This repository is a 3,000+ page-equivalent implementation documentation library for FiberNet.

## Contents
- Atomic specification pages: **5551**
- Narrative architecture/product books: **26**
- UI mockup references: **47**
- Architecture diagrams, schemas, API outline, matrices, runbooks and tests.

## How to use
1. Read `CLAUDE.md`.
2. Read `books/00-master-index.md` and the relevant narrative book.
3. Locate atomic feature pages through `MASTER-MANIFEST.csv`.
4. Use UI mockups as visual references only.
5. Implement backend truth and tests before declaring screens complete.

## Page semantics
Each Markdown file under `requirements/` is treated as one atomic documentation page in the docs library. The library contains more than 3,000 such pages and is designed for static-site publication (MkDocs/Docusaurus or similar).
