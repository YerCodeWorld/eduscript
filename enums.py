from enum import Enum

class ExerciseTypes(Enum):
    MCQ = "mcq"
    BLANKS = "blanks"
    MATCHING = "matching"
    ORDERING = "ordering"
    CATEGORIZE = "categorize"
    SELECT = "select"

class ExerciseDifficulty(Enum):
    BEGINNER = "beginner"
    UPPER_BEGINNER = "upper_beginner"
    INTERMEDIATE = "intermediate"
    UPPER_INTERMEDIATE = "upper_intermediate"
    ADVANCED = "advanced"
    SUPER_ADVANCED = "super_advanced"

class ExerciseCategory(Enum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    READING = "reading"
    LISTENING = "listening"
    WRITING = "writing"
    CONVERSATION = "conversation"
    SPEAKING = "speaking"
    GENERAL = "general"

class DisplayStyle(Enum):
    SIMPLE = "simple"
    ANIMATED = "animated"
    SCHOOL = "school"
    NATURE = "nature"
    DARK = "dark"

class MaxValuesLength(Enum):
    TITLE = 50
    VARIATION = 10
    STYLE = 10
    INSTRUNCTIONS = 50
    PACKAGEID = 20

class RequiredMetadataInfo(Enum):
    TYPE = "type"
    TITLE = "title"

class ValidMetadataBlock(Enum):
    TYPE = "type"
    VARIATION = "variation"
    STYLE = "style"
    TITLE = "title"
    DIFFICULTY = "difficulty"
    INSTRUNCTIONS = "instructions"
    CATEGORY = "category"
    ISPUBLISHED = "isPublished"
    PACKAGEID = "packageId"


