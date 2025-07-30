from datetime import datetime
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from uuid_utils.compat import UUID, uuid4, uuid7

from ..models import LabelPredictionMemoryLookup, LabelPredictionWithMemories
from .action_add_memories import (
    AddMemoryInput,
    AddMemoryRecommendations,
    AddMemorySuggestion,
    add_memories_agent,
    generate_memories,
)
from .explain_prediction import ExplainPredictionContext


def create_test_memory_lookup(prediction_id: UUID):
    return LabelPredictionMemoryLookup(
        prediction_id=prediction_id,
        value="Memory text about a product",
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
        input_value="This product was not what I expected.",
        input_embedding=np.random.randn(10).astype(np.float32),
        logits=np.random.randn(2).astype(np.float32),
        timestamp=datetime.now(),
        memories=[
            create_test_memory_lookup(prediction_id),
            create_test_memory_lookup(prediction_id),
        ],
    )


def test_add_memory_recommendations_validation():
    """Test that AddMemoryRecommendations validates properly"""
    suggestions = [
        AddMemorySuggestion(value="I was disappointed with this product.", label="negative"),
        AddMemorySuggestion(value="This product fell short of my expectations.", label="negative"),
    ]

    recommendations = AddMemoryRecommendations(memories=suggestions)
    assert len(recommendations.memories) == 2
    assert recommendations.memories[0].value == "I was disappointed with this product."
    assert recommendations.memories[0].label == "negative"


@pytest.mark.asyncio
async def test_generate_memories(mock_llm):
    """Test the generate_memories function with mock_llm"""
    prediction = create_test_prediction()
    explanation = "The model predicted positive because it couldn't find similar negative examples."
    context = ExplainPredictionContext(
        model_description="sentiment analysis",
        lookup_score_median=0.6,
        lookup_score_std=0.2,
        label_names=["positive", "negative"],
    )

    # Patch the run method to return a mock result
    mock_result = MagicMock()
    mock_result.data = AddMemoryRecommendations(
        memories=[
            AddMemorySuggestion(value="I was disappointed with this product.", label="negative"),
            AddMemorySuggestion(value="This product didn't meet my expectations.", label="negative"),
            AddMemorySuggestion(value="I regret purchasing this item.", label="negative"),
        ]
    )

    with patch.object(add_memories_agent, "run", return_value=mock_result):
        result = await generate_memories(prediction, explanation, context)

        assert isinstance(result, AddMemoryRecommendations)
        assert len(result.memories) == 3
        assert all(mem.label == "negative" for mem in result.memories)
