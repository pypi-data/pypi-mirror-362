from enum import Enum

class DigitizeReportAgentComponents(Enum):
    AGENT_MISSING_SECTIONS = "missing-sections"
    AGENT_MISSING_CHECKBOXES = "missing-checkboxes"
    AGENT_MISSING_SECTION_TEXT = "missing-section-text"


class DigitizeReportComponents(Enum):
    DTW = "dtw"
    LINE_COMPARISON = "line-comparison"
    MISSING_SECTIONS = DigitizeReportAgentComponents.AGENT_MISSING_SECTIONS.value
    MISSING_CHECKBOXES = DigitizeReportAgentComponents.AGENT_MISSING_CHECKBOXES.value
    MISSING_SECTION_TEXT = DigitizeReportAgentComponents.AGENT_MISSING_SECTION_TEXT.value
