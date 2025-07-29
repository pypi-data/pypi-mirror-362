from transformers import AutoTokenizer, EsmModel
import torch


def load_model(model_name, conf):
    device = torch.device(conf['embedding'].get('device', "cuda"))
    return EsmModel.from_pretrained(model_name).to(device)


def load_tokenizer(model_name):
    return AutoTokenizer.from_pretrained(model_name)


def embedding_task(sequences, model, tokenizer, device, batch_size=32, embedding_type_id=None):
    """
    Processes sequences to generate embeddings.

    Args:
    - sequences: List of dictionaries containing sequence information. Each dictionary should have:
        - 'sequence': The protein sequence.
        - 'sequence_id': An identifier for the sequence.
    - model: Preloaded EsmModel.
    - tokenizer: Preloaded AutoTokenizer.
    - embedding_type_id: Identifier for the embedding type (optional).

    Returns:
    A list of embedding records with sequence_id and embedding_type_id.
    """
    model.to(device)

    embedding_records = []
    with torch.no_grad():
        for seq_info in sequences:
            sequence = seq_info["sequence"]
            sequence_id = seq_info.get("sequence_id")

            tokens = tokenizer(sequence, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
            tokens = {k: v.to(device) for k, v in tokens.items()}

            try:
                outputs = model(**tokens)
                embeddings = outputs.last_hidden_state.mean(dim=1)
                embedding_shape = embeddings.shape

                # Prepare the record
                record = {
                    'sequence_id': sequence_id,  # Include sequence_id
                    'embedding_type_id': embedding_type_id,  # Include embedding_type_id
                    'sequence': sequence,
                    'embedding': embeddings.cpu().numpy().tolist()[0],
                    'shape': embedding_shape
                }

                embedding_records.append(record)
            except Exception as e:
                print(f"Failed to process sequence {sequence_id}: {e}")
                continue

    return embedding_records
