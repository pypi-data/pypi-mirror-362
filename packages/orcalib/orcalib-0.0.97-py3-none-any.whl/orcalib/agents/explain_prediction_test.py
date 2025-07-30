from datetime import datetime

import numpy as np
import pytest
from uuid_utils.compat import UUID, uuid4, uuid7

from ..models import LabelPredictionMemoryLookup, LabelPredictionWithMemories
from .explain_prediction import ExplainPredictionContext, explain_prediction_agent


def create_test_memory_lookup(prediction_id: UUID):
    return LabelPredictionMemoryLookup(
        prediction_id=prediction_id,
        value="Memory 1 text",
        label_name="positive",
        embedding=np.random.randn(10).astype(np.float32),
        memory_id=uuid7(),
        memory_version=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        edited_at=datetime.now(),
        metrics={},
        metadata={},
        label=0,
        source_id=None,
        lookup_score=0.9,
        attention_weight=0.5,
    )


def create_test_prediction():
    prediction_id = uuid4()
    return LabelPredictionWithMemories(
        prediction_id=prediction_id,
        anomaly_score=0.5,
        label=0,
        label_name="positive",
        expected_label=1,
        expected_label_name="negative",
        confidence=0.8,
        input_value="This is a test input",
        input_embedding=np.random.randn(10).astype(np.float32),
        logits=np.random.randn(2).astype(np.float32),
        timestamp=datetime.now(),
        memories=[
            create_test_memory_lookup(prediction_id),
            create_test_memory_lookup(prediction_id),
        ],
    )


@pytest.mark.asyncio
async def test_explain_prediction_agent(mock_llm):
    prediction = create_test_prediction()

    context = ExplainPredictionContext(
        model_description="sentiment analysis",
        lookup_score_median=0.6,
        lookup_score_std=0.2,
        label_names=["positive", "negative"],
    )

    result = await explain_prediction_agent.run(prediction, deps=context)
    assert isinstance(result.data, str)
    assert len(result.data) > 0
