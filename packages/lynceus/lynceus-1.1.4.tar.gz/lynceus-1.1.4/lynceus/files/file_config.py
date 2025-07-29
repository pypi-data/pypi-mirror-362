from enum import Enum


class FileMetadataType(Enum):
    DATASET: str = 'Dataset'
    DATASET_EXCERPT: str = 'Data excerpt'
    DATASET_FULL: str = 'Full dataset'

    TEST_SET_INTERIM: str = 'Interim Test Set'
    TEST_SET_FINAL: str = 'Final Test Set'

    DATA_DICTIONARY: str = 'Data dictionary'

    ASSIGNMENT_SOLUTION: str = 'Solution File'
    ASSIGNMENT_SAMPLE: str = 'Template Solution File'
    ASSIGNMENT_BENCHMARK: str = 'Benchmark Solution File'
    ASSIGNMENT_SUBMISSION: str = 'Submission File'

    CUSTOM_SCORER: str = 'Custom scorer'

    OTHER: str = 'Other'
    UNSPECIFIED: str = 'Unspecified'
