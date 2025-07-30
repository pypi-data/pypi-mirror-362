import torch

from .regression_heads import MemoryMixtureOfExpertsRegressionHead


def test_mmoe_regression_head():
    # Given an MMOE regression head
    embedding_dim = 128
    memory_count = 5
    batch_size = 2
    mmoe_head = MemoryMixtureOfExpertsRegressionHead(embedding_dim=embedding_dim)
    # And a batch of memories and an input embedding
    memories_scores = torch.tensor([[1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 4.0, 6.0, 8.0, 10.0]])
    assert memories_scores.shape == (batch_size, memory_count)
    input_embeds = torch.rand(batch_size, embedding_dim)
    memories_embeds = torch.rand(batch_size, memory_count, embedding_dim)
    # When the forward method is called
    scores = mmoe_head.forward(
        input_embeddings=input_embeds,
        memories_scores=memories_scores,
        memories_embeddings=memories_embeds,
    )
    # Then the scores should be a tensor of shape batch_size
    assert scores.shape == (batch_size,)
    # And the scores should be weighted averages of the memory scores
    assert torch.all(scores >= torch.min(memories_scores, dim=1).values)
    assert torch.all(scores <= torch.max(memories_scores, dim=1).values)
    # And the last memory weights should be a tensor of shape batch_size x memory_count
    assert mmoe_head.last_memories_attention_weights is not None
    assert mmoe_head.last_memories_attention_weights.shape == (batch_size, memory_count)
    # And the memory weights should be non-negative (due to LeakyReLU)
    assert torch.all(mmoe_head.last_memories_attention_weights >= 0)


def test_mmoe_regression_head_single_memory():
    # Given an MMOE regression head
    embedding_dim = 128
    memory_count = 1
    batch_size = 2
    mmoe_head = MemoryMixtureOfExpertsRegressionHead(embedding_dim=embedding_dim)
    # And a batch with single memory per example
    memories_scores = torch.tensor([[2.5], [5.0]])
    assert memories_scores.shape == (batch_size, memory_count)
    input_embeds = torch.rand(batch_size, embedding_dim)
    memories_embeds = torch.rand(batch_size, memory_count, embedding_dim)
    # When the forward method is called
    scores = mmoe_head.forward(
        input_embeddings=input_embeds,
        memories_scores=memories_scores,
        memories_embeddings=memories_embeds,
    )
    # Then the scores should match the input scores (since there's only one memory per example)
    assert scores.shape == (batch_size,)
    assert torch.allclose(scores, memories_scores.squeeze(1))
    # And the last memory weights should be a tensor of shape batch_size x memory_count
    assert mmoe_head.last_memories_attention_weights is not None
    assert mmoe_head.last_memories_attention_weights.shape == (batch_size, memory_count)


def test_mmoe_regression_head_with_weights():
    # Given an MMOE regression head
    embedding_dim = 128
    memory_count = 3
    batch_size = 2
    mmoe_head = MemoryMixtureOfExpertsRegressionHead(embedding_dim=embedding_dim)
    # And a batch of memories with weights
    memories_scores = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert memories_scores.shape == (batch_size, memory_count)
    memories_weights = torch.tensor([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert memories_weights.shape == (batch_size, memory_count)
    input_embeds = torch.rand(batch_size, embedding_dim)
    memories_embeds = torch.rand(batch_size, memory_count, embedding_dim)
    # When the forward method is called with weights
    scores = mmoe_head.forward(
        input_embeddings=input_embeds,
        memories_scores=memories_scores,
        memories_embeddings=memories_embeds,
        memories_weights=memories_weights,
    )
    # Then the scores should be a tensor of shape batch_size
    assert scores.shape == (batch_size,)
    # And the scores should be weighted appropriately
    assert torch.all(scores >= torch.min(memories_scores, dim=1).values)
    assert torch.all(scores <= torch.max(memories_scores, dim=1).values)
    # And the last memory weights should be a tensor of shape batch_size x memory_count
    assert mmoe_head.last_memories_attention_weights is not None
    assert mmoe_head.last_memories_attention_weights.shape == (batch_size, memory_count)
