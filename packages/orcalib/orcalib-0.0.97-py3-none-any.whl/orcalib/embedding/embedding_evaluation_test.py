from .embedding_evaluation import evaluate_for_classification
from .embedding_models import EmbeddingModel


def test_evaluate_for_classification(dataset):
    metrics = evaluate_for_classification(
        embedding_model=EmbeddingModel.GTE_SMALL,
        memory_dataset=dataset,
        value_column="text",
    )
    assert metrics.accuracy > 0.5
