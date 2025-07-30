import numpy as np
import torch
from datasets import Dataset
from faiss import METRIC_INNER_PRODUCT
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from ..shared.metrics import ClassificationMetrics, calculate_classification_metrics
from ..torch_layers.classification_heads import NearestMemoriesClassificationHead
from ..utils.dataset import parse_dataset
from ..utils.progress import OnProgressCallback, safely_call_on_progress
from ..utils.pydantic import Vector
from .embedding_models import EmbeddingModel


def evaluate_for_classification(
    embedding_model: EmbeddingModel,
    memory_dataset: Dataset,
    *,
    eval_dataset: Dataset | None = None,
    value_column: str = "value",
    label_column: str = "label",
    neighbor_count: int = 5,
    batch_size: int = 32,
    weigh_memories: bool = True,
    show_progress_bar: bool = True,
    on_progress: OnProgressCallback | None = None,
) -> ClassificationMetrics:
    """
    Evaluate the performance of an embedding model as a KNN classifier.

    Warning:
        This method is intended for small datasets, make sure to subsample your dataset. For a
        more scalable approach, create a proper memoryset and RAC model instead.

    Notes:
        This method does not rely on infrastrucutre for memorysets. It instead computes embeddings
        internally and uses FAISS with a flat index (i.e. not ANN) to compute nearest neighbors.

    Args:
        embedding_model: embedding model to evaluate
        memory_dataset: dataset containing the memories for the KNN classifier
        eval_dataset: Optional dataset to evaluate the KNN classifier on, if not provided a random
            20% subset of the memory_dataset will be split off for evaluation
        value_column: column containing the values to embed
        label_column: column containing the labels
        neighbor_count: number of neighbors to use for the KNN classifier
        batch_size: batch size for the dataloader
        weigh_memories: whether to weigh the memories by their lookup scores
        show_progress_bar: whether to show a progress bar for the evaluation
        on_progress: callback function that is called to report the progress of the evaluation
    """
    memory_dataset = parse_dataset(memory_dataset, value_column=value_column, label_column=label_column)

    # if no eval dataset is provided, split a 20% random subset off the memory_dataset for evaluation
    if eval_dataset is None:
        split_dataset = memory_dataset.train_test_split(0.2, shuffle=True, seed=42, stratify_by_column="label")
        eval_dataset = split_dataset["test"]
        memory_dataset = split_dataset["train"]
    else:
        eval_dataset = parse_dataset(eval_dataset, value_column=value_column, label_column=label_column)

    total_steps = len(memory_dataset) // batch_size + len(eval_dataset) // batch_size
    current_step = 0

    # create a pseudo memoryset by adding a faiss index to the memory dataset
    context = embedding_model.compute_context(memory_dataset["value"]) if embedding_model.uses_context else None

    def embed_batch(batch: dict):
        nonlocal current_step
        safely_call_on_progress(on_progress, current_step, total_steps)
        current_step += 1
        return {"embedding": embedding_model.embed(batch["value"], prompt="document", context=context)}

    # uses flat index (i.e. not ANN) by default, we could pass a custom index like HNSW (but it would need to be trained first)
    embedded_memory_dataset = memory_dataset.map(embed_batch, batched=True, batch_size=batch_size).add_faiss_index(
        column="embedding", metric_type=METRIC_INNER_PRODUCT
    )

    # instantiate the classification head
    num_classes = len(set(memory_dataset["label"]))
    head = NearestMemoriesClassificationHead(num_classes, weigh_memories=weigh_memories)

    # create a collator that computes the nearest neighbors for a batch of values
    def memory_lookup_collator(batch: list[dict]):
        values = [item["value"] for item in batch]
        labels = [item["label"] for item in batch]
        embeddings = embedding_model.embed(values, prompt="query", context=context)
        memory_weights = []
        memory_labels = []
        memory_embeddings = []
        for embedding in embeddings:
            scores, neighbors = embedded_memory_dataset.get_nearest_examples("embedding", embedding, k=neighbor_count)
            memory_weights.append(scores)
            memory_labels.append(neighbors["label"])
            memory_embeddings.append(neighbors["embedding"])

        return {
            "input_embeddings": torch.tensor(np.stack(embeddings)),
            "memories_labels": torch.tensor(memory_labels),
            "memories_weights": torch.tensor(np.stack(memory_weights)),
            "memories_embeddings": torch.tensor(np.stack(memory_embeddings)),
            "labels": torch.tensor(labels),
        }

    # compute the accuracy of the model
    logits: list[Vector] = []
    for batch in tqdm(
        DataLoader(eval_dataset, batch_size=batch_size, collate_fn=memory_lookup_collator),  # type: ignore
        disable=not show_progress_bar,
    ):
        safely_call_on_progress(on_progress, current_step, total_steps)
        current_step += 1
        logits_batch = head(
            input_embeddings=batch["input_embeddings"],
            memories_weights=batch["memories_weights"],
            memories_labels=batch["memories_labels"],
            memories_embeddings=batch["memories_embeddings"],
        )
        logits.extend([np.array(l) for l in logits_batch])

    metrics = calculate_classification_metrics(
        expected_labels=eval_dataset["label"],
        logits=logits,
    )
    safely_call_on_progress(on_progress, current_step, total_steps)
    # compute the accuracy of the model
    return metrics
