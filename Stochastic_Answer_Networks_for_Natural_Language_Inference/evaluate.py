import argparse
import pickle
import torch
from pathlib import Path
from torch.utils.data import DataLoader
from model.net import SAN
from model.data import Corpus, batchify
from model.utils import PreProcessor
from model.split import split_morphs, split_jamos
from model.metric import evaluate, acc, log_loss
from utils import Config, CheckpointManager, SummaryManager

parser = argparse.ArgumentParser()
parser.add_argument(
    "--data_dir", default="data", help="Directory containing config.json of data"
)
parser.add_argument(
    "--model_dir",
    default="experiments/base_model",
    help="Directory containing config.json of model",
)
parser.add_argument(
    "--dataset",
    default="validation",
    help="name of the data in --data_dir to be evaluate",
)


if __name__ == "__main__":
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    model_dir = Path(args.model_dir)
    data_config = Config(data_dir / "config.json")
    model_config = Config(model_dir / "config.json")

    # tokenizer
    with open(data_config.fine_vocab, mode="rb") as io:
        fine_vocab = pickle.load(io)
    with open(data_config.coarse_vocab, mode="rb") as io:
        coarse_vocab = pickle.load(io)

    preprocessor = PreProcessor(
        coarse_vocab=coarse_vocab,
        fine_vocab=fine_vocab,
        coarse_split_fn=split_morphs,
        fine_split_fn=split_jamos,
    )

    # model (restore)
    checkpoint_manager = CheckpointManager(model_dir)
    checkpoint = checkpoint_manager.load_checkpoint("best.tar")
    model = SAN(model_config.num_classes, coarse_vocab, fine_vocab,
                model_config.fine_embedding_dim, model_config.hidden_dim, model_config.multi_step,
                model_config.prediction_drop_ratio)
    model.load_state_dict(checkpoint["model_state_dict"])

    # evaluation
    filepath = getattr(data_config, args.dataset)
    ds = Corpus(filepath, preprocessor.preprocess)
    dl = DataLoader(
        ds, batch_size=model_config.batch_size, num_workers=4, collate_fn=batchify
    )

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    summary_manager = SummaryManager(model_dir)
    summary = evaluate(model, dl, {"loss": log_loss, "acc": acc}, device)

    summary_manager.load("summary.json")
    summary_manager.update({"{}".format(args.dataset): summary})
    summary_manager.save("summary.json")

    print("loss: {:.3f}, acc: {:.2%}".format(summary["loss"], summary["acc"]))
