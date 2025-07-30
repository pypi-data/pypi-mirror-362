from enum import Enum


class NotFoundErrorResponseResourceType0(str, Enum):
    ANALYSIS = "analysis"
    API_KEY = "api_key"
    CLASSIFICATION_MODEL = "classification_model"
    DATASOURCE = "datasource"
    EMBEDDING_EVALUATION = "embedding_evaluation"
    EVALUATION = "evaluation"
    FEEDBACK_CATEGORY = "feedback_category"
    FINETUNED_EMBEDDING_MODEL = "finetuned_embedding_model"
    MEMORY = "memory"
    MEMORYSET = "memoryset"
    ORG = "org"
    ORG_PLAN = "org_plan"
    PREDICTION = "prediction"
    PRETRAINED_EMBEDDING_MODEL = "pretrained_embedding_model"
    REGRESSION_MODEL = "regression_model"
    TASK = "task"

    def __str__(self) -> str:
        return str(self.value)
