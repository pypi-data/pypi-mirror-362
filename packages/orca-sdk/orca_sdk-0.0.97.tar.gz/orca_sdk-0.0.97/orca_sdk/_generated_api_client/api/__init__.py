"""Contains methods for accessing the API"""

from .auth.check_authentication_auth_get import sync as check_authentication
from .auth.create_api_key_auth_api_key_post import sync as create_api_key
from .auth.create_org_plan_auth_org_plan_post import sync as create_org_plan
from .auth.delete_api_key_auth_api_key_name_or_id_delete import sync as delete_api_key
from .auth.delete_org_auth_org_delete import sync as delete_org
from .auth.get_org_plan_auth_org_plan_get import sync as get_org_plan
from .auth.list_api_keys_auth_api_key_get import sync as list_api_keys
from .auth.update_org_plan_auth_org_plan_put import sync as update_org_plan
from .classification_model.create_classification_model_classification_model_post import (
    sync as create_classification_model,
)
from .classification_model.delete_classification_model_classification_model_name_or_id_delete import (
    sync as delete_classification_model,
)
from .classification_model.delete_classification_model_evaluation_classification_model_model_name_or_id_evaluation_task_id_delete import (
    sync as delete_classification_model_evaluation,
)
from .classification_model.evaluate_classification_model_classification_model_model_name_or_id_evaluation_post import (
    sync as evaluate_classification_model,
)
from .classification_model.get_classification_model_classification_model_name_or_id_get import (
    sync as get_classification_model,
)
from .classification_model.get_classification_model_evaluation_classification_model_model_name_or_id_evaluation_task_id_get import (
    sync as get_classification_model_evaluation,
)
from .classification_model.list_classification_model_evaluations_classification_model_model_name_or_id_evaluation_get import (
    sync as list_classification_model_evaluations,
)
from .classification_model.list_classification_models_classification_model_get import (
    sync as list_classification_models,
)
from .classification_model.predict_label_gpu_classification_model_name_or_id_prediction_post import (
    sync as predict_label_gpu,
)
from .classification_model.update_classification_model_classification_model_name_or_id_patch import (
    sync as update_classification_model,
)
from .datasource.create_datasource_from_content_datasource_post import (
    sync as create_datasource_from_content,
)
from .datasource.create_datasource_from_files_datasource_upload_post import (
    sync as create_datasource_from_files,
)
from .datasource.create_embedding_evaluation_datasource_name_or_id_embedding_evaluation_post import (
    sync as create_embedding_evaluation,
)
from .datasource.delete_datasource_datasource_name_or_id_delete import (
    sync as delete_datasource,
)
from .datasource.download_datasource_datasource_name_or_id_download_get import (
    sync as download_datasource,
)
from .datasource.get_datasource_datasource_name_or_id_get import sync as get_datasource
from .datasource.get_embedding_evaluation_datasource_name_or_id_embedding_evaluation_task_id_get import (
    sync as get_embedding_evaluation,
)
from .datasource.list_datasources_datasource_get import sync as list_datasources
from .datasource.list_embedding_evaluations_datasource_name_or_id_embedding_evaluation_get import (
    sync as list_embedding_evaluations,
)
from .default.healthcheck_get import sync as healthcheck
from .default.healthcheck_gpu_get import sync as healthcheck_gpu
from .finetuned_embedding_model.create_finetuned_embedding_model_finetuned_embedding_model_post import (
    sync as create_finetuned_embedding_model,
)
from .finetuned_embedding_model.delete_finetuned_embedding_model_finetuned_embedding_model_name_or_id_delete import (
    sync as delete_finetuned_embedding_model,
)
from .finetuned_embedding_model.embed_with_finetuned_model_gpu_finetuned_embedding_model_name_or_id_embedding_post import (
    sync as embed_with_finetuned_model_gpu,
)
from .finetuned_embedding_model.get_finetuned_embedding_model_finetuned_embedding_model_name_or_id_get import (
    sync as get_finetuned_embedding_model,
)
from .finetuned_embedding_model.list_finetuned_embedding_models_finetuned_embedding_model_get import (
    sync as list_finetuned_embedding_models,
)
from .memoryset.analyze_memoryset_memoryset_name_or_id_analysis_post import (
    sync as analyze_memoryset,
)
from .memoryset.batch_delete_memoryset_batch_delete_memoryset_post import (
    sync as batch_delete_memoryset_batch_delete,
)
from .memoryset.clone_memoryset_memoryset_name_or_id_clone_post import (
    sync as clone_memoryset,
)
from .memoryset.create_memoryset_memoryset_post import sync as create_memoryset
from .memoryset.delete_memories_memoryset_name_or_id_memories_delete_post import (
    sync as delete_memories,
)
from .memoryset.delete_memory_memoryset_name_or_id_memory_memory_id_delete import (
    sync as delete_memory,
)
from .memoryset.delete_memoryset_memoryset_name_or_id_delete import (
    sync as delete_memoryset,
)
from .memoryset.get_analysis_memoryset_name_or_id_analysis_analysis_task_id_get import (
    sync as get_analysis,
)
from .memoryset.get_memories_memoryset_name_or_id_memories_get_post import (
    sync as get_memories,
)
from .memoryset.get_memory_memoryset_name_or_id_memory_memory_id_get import (
    sync as get_memory,
)
from .memoryset.get_memoryset_memoryset_name_or_id_get import sync as get_memoryset
from .memoryset.insert_memories_gpu_memoryset_name_or_id_memory_post import (
    sync as insert_memories_gpu,
)
from .memoryset.list_analyses_memoryset_name_or_id_analysis_get import (
    sync as list_analyses,
)
from .memoryset.list_memorysets_memoryset_get import sync as list_memorysets
from .memoryset.memoryset_lookup_gpu_memoryset_name_or_id_lookup_post import (
    sync as memoryset_lookup_gpu,
)
from .memoryset.potential_duplicate_groups_memoryset_name_or_id_potential_duplicate_groups_get import (
    sync as potential_duplicate_groups,
)
from .memoryset.query_memoryset_memoryset_name_or_id_memories_post import (
    sync as query_memoryset,
)
from .memoryset.suggest_cascading_edits_memoryset_name_or_id_memory_memory_id_cascading_edits_post import (
    sync as suggest_cascading_edits,
)
from .memoryset.update_memories_gpu_memoryset_name_or_id_memories_patch import (
    sync as update_memories_gpu,
)
from .memoryset.update_memory_gpu_memoryset_name_or_id_memory_patch import (
    sync as update_memory_gpu,
)
from .memoryset.update_memoryset_memoryset_name_or_id_patch import (
    sync as update_memoryset,
)
from .predictive_model.list_predictive_models_predictive_model_get import (
    sync as list_predictive_models,
)
from .pretrained_embedding_model.embed_with_pretrained_model_gpu_pretrained_embedding_model_model_name_embedding_post import (
    sync as embed_with_pretrained_model_gpu,
)
from .pretrained_embedding_model.get_pretrained_embedding_model_pretrained_embedding_model_model_name_get import (
    sync as get_pretrained_embedding_model,
)
from .pretrained_embedding_model.list_pretrained_embedding_models_pretrained_embedding_model_get import (
    sync as list_pretrained_embedding_models,
)
from .regression_model.create_regression_model_regression_model_post import (
    sync as create_regression_model,
)
from .regression_model.delete_regression_model_evaluation_regression_model_model_name_or_id_evaluation_task_id_delete import (
    sync as delete_regression_model_evaluation,
)
from .regression_model.delete_regression_model_regression_model_name_or_id_delete import (
    sync as delete_regression_model,
)
from .regression_model.evaluate_regression_model_regression_model_model_name_or_id_evaluation_post import (
    sync as evaluate_regression_model,
)
from .regression_model.get_regression_model_evaluation_regression_model_model_name_or_id_evaluation_task_id_get import (
    sync as get_regression_model_evaluation,
)
from .regression_model.get_regression_model_regression_model_name_or_id_get import (
    sync as get_regression_model,
)
from .regression_model.list_regression_model_evaluations_regression_model_model_name_or_id_evaluation_get import (
    sync as list_regression_model_evaluations,
)
from .regression_model.list_regression_models_regression_model_get import (
    sync as list_regression_models,
)
from .regression_model.predict_score_gpu_regression_model_name_or_id_prediction_post import (
    sync as predict_score_gpu,
)
from .regression_model.update_regression_model_regression_model_name_or_id_patch import (
    sync as update_regression_model,
)
from .task.abort_task_task_task_id_abort_delete import sync as abort_task
from .task.get_task_status_task_task_id_status_get import sync as get_task_status
from .task.get_task_task_task_id_get import sync as get_task
from .task.list_tasks_task_get import sync as list_tasks
from .telemetry.count_predictions_telemetry_prediction_count_post import (
    sync as count_predictions,
)
from .telemetry.drop_feedback_category_with_data_telemetry_feedback_category_name_or_id_delete import (
    sync as drop_feedback_category_with_data,
)
from .telemetry.explain_prediction_telemetry_prediction_prediction_id_explanation_get import (
    sync as explain_prediction,
)
from .telemetry.generate_memory_suggestions_telemetry_prediction_prediction_id_memory_suggestions_post import (
    sync as generate_memory_suggestions,
)
from .telemetry.get_action_recommendation_telemetry_prediction_prediction_id_action_get import (
    sync as get_action_recommendation,
)
from .telemetry.get_feedback_category_telemetry_feedback_category_name_or_id_get import (
    sync as get_feedback_category,
)
from .telemetry.get_prediction_telemetry_prediction_prediction_id_get import (
    sync as get_prediction,
)
from .telemetry.list_feedback_categories_telemetry_feedback_category_get import (
    sync as list_feedback_categories,
)
from .telemetry.list_memories_with_feedback_telemetry_memories_post import (
    sync as list_memories_with_feedback,
)
from .telemetry.list_predictions_telemetry_prediction_post import (
    sync as list_predictions,
)
from .telemetry.record_prediction_feedback_telemetry_prediction_feedback_put import (
    sync as record_prediction_feedback,
)
from .telemetry.update_prediction_telemetry_prediction_prediction_id_patch import (
    sync as update_prediction,
)

__all__ = [
    "abort_task",
    "analyze_memoryset",
    "batch_delete_memoryset_batch_delete",
    "check_authentication",
    "clone_memoryset",
    "count_predictions",
    "create_api_key",
    "create_classification_model",
    "create_datasource_from_content",
    "create_datasource_from_files",
    "create_embedding_evaluation",
    "create_finetuned_embedding_model",
    "create_memoryset",
    "create_org_plan",
    "create_regression_model",
    "delete_api_key",
    "delete_classification_model",
    "delete_classification_model_evaluation",
    "delete_datasource",
    "delete_finetuned_embedding_model",
    "delete_memories",
    "delete_memory",
    "delete_memoryset",
    "delete_org",
    "delete_regression_model",
    "delete_regression_model_evaluation",
    "download_datasource",
    "drop_feedback_category_with_data",
    "embed_with_finetuned_model_gpu",
    "embed_with_pretrained_model_gpu",
    "evaluate_classification_model",
    "evaluate_regression_model",
    "explain_prediction",
    "generate_memory_suggestions",
    "get_action_recommendation",
    "get_analysis",
    "get_classification_model",
    "get_classification_model_evaluation",
    "get_datasource",
    "get_embedding_evaluation",
    "get_feedback_category",
    "get_finetuned_embedding_model",
    "get_memories",
    "get_memory",
    "get_memoryset",
    "get_org_plan",
    "get_prediction",
    "get_pretrained_embedding_model",
    "get_regression_model",
    "get_regression_model_evaluation",
    "get_task",
    "get_task_status",
    "healthcheck",
    "healthcheck_gpu",
    "insert_memories_gpu",
    "list_analyses",
    "list_api_keys",
    "list_classification_model_evaluations",
    "list_classification_models",
    "list_datasources",
    "list_embedding_evaluations",
    "list_feedback_categories",
    "list_finetuned_embedding_models",
    "list_memories_with_feedback",
    "list_memorysets",
    "list_predictions",
    "list_predictive_models",
    "list_pretrained_embedding_models",
    "list_regression_model_evaluations",
    "list_regression_models",
    "list_tasks",
    "memoryset_lookup_gpu",
    "potential_duplicate_groups",
    "predict_label_gpu",
    "predict_score_gpu",
    "query_memoryset",
    "record_prediction_feedback",
    "suggest_cascading_edits",
    "update_classification_model",
    "update_memories_gpu",
    "update_memory_gpu",
    "update_memoryset",
    "update_org_plan",
    "update_prediction",
    "update_regression_model",
]
