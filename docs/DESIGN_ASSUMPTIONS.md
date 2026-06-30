# CandidateOne 
# Design Assumptions

## General

- Resume PDFs are machine-readable (OCR is not supported).
- One canonical profile is generated per candidate.
- Unknown or unsupported fields are ignored safely.

## Source Priority

The default merge priority is:

1. Resume
2. LinkedIn
3. ATS
4. GitHub
5. Recruiter CSV

Higher-priority sources are preferred during conflict resolution.

## Data Normalization

- Dates are normalized to `YYYY-MM`.
- Phone numbers are normalized to E.164 format.
- Skills are canonicalized using predefined mappings.
- Country names are standardized whenever possible.

## Merge Strategy

- Prefer non-empty values.
- Preserve provenance for every field.
- Remove duplicate emails, phone numbers, skills, and experience entries.
- Never invent missing information.

## Projection

- The canonical schema is immutable.
- Runtime configuration determines the projected output schema.

## Validation

- Every projected profile is validated before export.
- Invalid or malformed fields are ignored without terminating the pipeline.

## Known Limitations

- OCR for scanned resumes is not implemented.
- DOCX resumes are not currently supported.
- No live ATS or LinkedIn API integration.
- Confidence scoring is heuristic-based.