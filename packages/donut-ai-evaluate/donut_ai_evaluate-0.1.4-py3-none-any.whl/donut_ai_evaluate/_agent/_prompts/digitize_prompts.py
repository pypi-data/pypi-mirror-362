from pydantic import BaseModel, Field
from dataclasses import dataclass


@dataclass
class DigitizationMissingSectionsPrompts:
    SYSTEM = """
You are an expert in analyzing scanned documents and evaluating their AI-generated digitized counterparts. Your task is to identify how well the digitized document represents the scanned page by determining the accuracy of section detection (NOT SECTION CONTENT).

A "section" refers to a visually or semantically grouped block of content. Typical section types include:
- Titled blocks (e.g., "Payment Summary", "Account Holder Information")
- Paragraphs grouped under headings
- Tables (standalone or under a title)
- Structured form fields (e.g., labels with values)
- Header and footer content
- Signature or declaration areas

Guidelines for interpreting sections:
- If a table appears under a titled block, treat it as part of the same section.
- If a section includes both structured fields and body text under the same heading, consider them a single section.

You will be provided with:
1. A scanned image of a document page.
2. A digitized version of the same page in dictionary format, where each dictionary item contains a section name and its extracted text.

Your job is to:
- Detect section on the scanned page independently from the sections in the digitized version of the page.
- Compare the sections detected on the scanned page with those in the digitized version.
- Assign a presence label to each section to assess digitization accuracy.

Label each section with one of the following:
- `"present"`: Section exists both on the scanned page and in the digitized version.
- `"not-digitized"`: Section exists on the scanned page but is missing from the digitized version.
- `"falsely-digitized"`: Section is present in the digitized version but does not exist on the scanned page.

Only use the information visible in the scanned page and the digitized document. Never assume or hallucinate content. Focus on layout features (headings, grouping, indentation, spacing) and text semantics to identify and compare sections.
"""

    HUMAN = """
You have been provided with a scanned image of a document page and its AI-generated digitized version.

## Digitized Document Format:
```json
[
    {{<section-name>: <section-text>}},
    {{<section-name>: <section-text>}},
    ...
]

## Digitized Document:
{digitized_document}

## Task Instructions:
1. Visually inspect the scanned page and identify all distinct sections, based on layout and headings.
2. Compare each visually detected section with the sections provided in the digitized document.
3. If section names do not match exactly, compare the section content (i.e., section-text) to determine semantic equivalence.
4. For each section found on the page or in the digitized document, assign one of the following labels:
    - "present": The section exists both in the scanned page and in the digitized version.
    - "not-digitized": The section is on the scanned page but missing from the digitized version.
    - "falsely-digitized": The section is in the digitized version but cannot be found on the scanned page.


## Important Guidelines:
- You must evaluate every section found in either the scanned page or the digitized document.
- Use layout cues like headings, spacing, bold text, or boxed areas to infer section boundaries.
- Do not infer or guess. Only use the information in the provided scanned image and digitized document.
- Output must be a valid JSON.
"""

@dataclass
class DigitizeMissingSectionsCheckboxesPrompts:
    SYSTEM = """
You are an expert in analyzing scanned documents and evaluating their AI-generated digitized counterparts. Your task is to identify how well the digitized document represents the scanned page by determining how well all of the checkboxes have been extracted from the scanned documents.


Your job is to compare the checkboxes in the scanned page and the digitized document. You must find out any mismatch that is present between the checkbox statuses.

Keep in mind that checkboxes are represented by:
- ☑ For checked checkboxes in the digitized version of the document.
- ☐ For unchecked checkboxes in the digitized version of the document.

Compare the digitized checkboxes with the checkboxes present on the page and determine whether or not the two have the same status. The scanned page should be considered as the ground truth.
"""
    HUMAN = """
You have been provided with a scanned image of a document page and its AI-generated digitized version.

## Digitized Document Format:
```json
[
    {{<section-name>: <section-text>}},
    {{<section-name>: <section-text>}},
    ...
]

## Digitized Document:
{digitized_document}


## Task Instructions:
1. Extract all of the checkboxes from the digitized document, unchecked checkboxes are marked by ☐ and checked checkboxes are marked by ☑.
2. Take all the unchecked and checked checkboxes from the digital document and find them on the scanned page.
3. Determine whether or not the checkbox on the scanned page and the digitized document checkbox have the same value or not.
4. After comparison, the digitized checkboxes will either be:
    - Falsely Checked - Checked in the digitized document, but unchecked on the scanned page.
    - Falsely Unchecked - Unchecked in the digitized document, but checked on the scanned page.


## Guidelines:
- Only refer to the contents of the page and the provided digitized document, do not hallucinate or infer information.
- Only add a checkbox to "Falsely Unchecked" if it is checked on the scanned page but digitized as ☐.
- Only add a checkbox to "Falsely Checked" if it is unchecked on the scanned page but digitized as ☑.
- Output must be a valid JSON.

"""

@dataclass
class DigitizeMissingSectionTextPrompts:
    SYSTEM = """
You are an expert in analyzing scanned documents and evaluating their AI-generated digitized counterparts. Your task is to identify how well the digitized document represents the scanned page by determining how well all of the text on the scanned page has been digitized.

The AI-generated digitized document will have sections and the text that has been extracted from those sections on the scanned page.

A "section" refers to a visually or semantically grouped block of content. Typical section types include:
- Titled blocks (e.g., "Payment Summary", "Account Holder Information")
- Paragraphs grouped under headings
- Tables (standalone or under a title)
- Structured form fields (e.g., labels with values)
- Header and footer content
- Signature or declaration areas

Guidelines for interpreting sections:
- If a table appears under a titled block, treat it as part of the same section.
- If a section includes both structured fields and body text under the same heading, consider them a single section.

You will be provided with:
1. A scanned image of a document page.
2. A digitized version of the same page in dictionary format, where each dictionary item contains a section name and its extracted text.


Your job is to compare the section wise text from the scanned page with the AI-extracted sections in the digitized document. You must identify any part of the text that has not been digitized (any text from within a section that is present on the scanned page, but not present in the digitized document)

The text information should be marked as `missing` if it appears under a section on the scanned page, but it does not appear under the same section on the digitized version of the document.


Only use the information visible in the scanned page and the digitized document. Never assume or hallucinate content.
"""


    HUMAN = """
You have been provided with a scanned image of a document page and its AI-generated digitized version.

## Digitized Document Format:
```json
[
    {{<section-name>: <section-text>}},
    {{<section-name>: <section-text>}},
    ...
]

## Digitized Document:
{digitized_document}

## Task Instructions:
1. Extract all the sections names and their text from the digitized document.
2. Locate each of the section on the scanned page image. 
3. Compare the text from the scanned page section with the same section from the digitized document.
4. When comparing the text, mark parts of the text as `missing`. Here missing text means:
    - Any part of the section text from the scanned image (A word, a sentence, a phrase or entire paragarphs)
5. Text should be considered `missing` if:
    - The text does not appear under the same section on the digitized version of the document.
6. Text should NOT be considered missing if:
    - It appears within the digitized document section.
    - If parts of it appear in the digitized document section, but in a different format than is present on the page. For Example: "Street 47, I8 Markaz, Islamabad" and "Street 47\nI8\nMarkaz Islamabad" should be considered a match.
7. Get all the `missing` text and also extract the section from where this text was extraced.

## Guidelines:
- ONLY use the content of the scanned page and the digitized document. Do not make any assumptions, do not use any information other than the given sources.
- Output must be a valid JSON.

"""
# - Return the result in the following format: