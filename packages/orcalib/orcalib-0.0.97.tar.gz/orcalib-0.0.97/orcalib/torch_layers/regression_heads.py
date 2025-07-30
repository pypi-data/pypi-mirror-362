from abc import ABC, abstractmethod

import torch
from torch import Tensor, nn


class RegressionHead(ABC, nn.Module):
    def __init__(self):
        super().__init__()
        self.last_memories_attention_weights: Tensor | None = None  # batch_size x memory_count

    @abstractmethod
    def forward(
        self,
        input_embeddings: Tensor | None = None,
        memories_scores: Tensor | None = None,
        memories_embeddings: Tensor | None = None,
        memories_weights: Tensor | None = None,
    ) -> Tensor:
        """
        Compute the output score by mixing the memories based on the input embedding

        Args:
            memories_scores: scores of the memories, float tensor of shape batch_size x memory_count
            input_embeddings: embedding of the model input, float tensor of shape batch_size x embedding_dim
            memories_embeddings: embeddings of the memories, float tensor of shape batch_size x memory_count x embedding_dim
            memories_weights: optional weights for each memory should be between 0 and 1, float tensor of shape batch_size x memory_count

        Returns:
            predicted scores, float tensor of shape batch_size
        """
        raise NotImplementedError


class MemoryMixtureOfExpertsRegressionHead(RegressionHead):
    """
    Regression head that returns scores based on scores of the memories weighted by learned
    weights that are a function of the input embedding and the memories embeddings
    """

    def __init__(self, embedding_dim: int):
        """
        Initialize the regression head

        Args:
            embedding_dim: dimension of the embeddings
        """
        super().__init__()
        self.embedding_dim = embedding_dim
        init_tensor = torch.nn.init.orthogonal_(torch.empty(embedding_dim, embedding_dim))
        self.memory_weights = nn.Parameter(init_tensor.clone().T.contiguous())
        self.input_weights = nn.Parameter(init_tensor.clone())
        self.nonlinear = nn.LeakyReLU()

    def forward(
        self,
        input_embeddings=None,
        memories_scores=None,
        memories_embeddings=None,
        memories_weights=None,
    ):
        assert input_embeddings is not None and memories_embeddings is not None and memories_scores is not None
        mmoe_memories_weights = self.nonlinear(
            torch.bmm(
                (input_embeddings @ self.input_weights).unsqueeze(1),
                self.memory_weights @ memories_embeddings.permute(0, 2, 1),
            )
        )  # batch_size x 1 x memory_count
        # Normalize the attention weights using softmax
        mmoe_memories_weights = torch.nn.functional.softmax(mmoe_memories_weights, dim=2)
        scores = torch.bmm(mmoe_memories_weights, memories_scores.unsqueeze(2)).squeeze(2).squeeze(1)  # batch_size
        self.last_memories_attention_weights = mmoe_memories_weights.squeeze(1)
        return scores
