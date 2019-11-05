import argparse
import pickle
import torch
import torch.optim as optim
from pathlib import Path
from torch.utils.data import DataLoader
from model.net import SAN
from model.data import Corpus, batchify
from model.utils import PreProcessor
from model.split import split_morphs, split_jamos
from model.metric import evaluate, acc, log_loss
from utils import Config, CheckpointManager, SummaryManager
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

# for reproducibility
torch.manual_seed(777)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

parser = argparse.ArgumentParser()
parser.add_argument(
    "--data_dir", default="data", help="Directory containing config.json of data"
)
parser.add_argument(
    "--model_dir",
    default="experiments/base_model",
    help="Directory containing config.json of model",
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

    # model
    model = SAN(model_config.num_classes, coarse_vocab, fine_vocab,
                model_config.fine_embedding_dim, model_config.hidden_dim, model_config.multi_step,
                model_config.prediction_drop_ratio)

    # training
    tr_ds = Corpus(data_config.train, preprocessor.preprocess)
    tr_dl = DataLoader(
        tr_ds,
        batch_size=model_config.batch_size,
        shuffle=True,
        num_workers=4,
        drop_last=True,
        collate_fn=batchify,
    )
    val_ds = Corpus(data_config.validation, preprocessor.preprocess)
    val_dl = DataLoader(
        val_ds, batch_size=model_config.batch_size, num_workers=4, collate_fn=batchify
    )

    opt = optim.Adam(model.parameters(), lr=model_config.learning_rate)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    writer = SummaryWriter("{}/runs".format(model_dir))
    checkpoint_manager = CheckpointManager(model_dir)
    summary_manager = SummaryManager(model_dir)
    best_val_loss = 1e10

    for epoch in tqdm(range(model_config.epochs), desc="epochs"):

        tr_loss = 0
        tr_acc = 0

        model.train()
        for step, mb in tqdm(enumerate(tr_dl), desc="steps", total=len(tr_dl)):
            qa_mb, qb_mb, y_mb = map(lambda elm: (el.to(device) for el in elm) if isinstance(elm, tuple) else
            elm.to(device), mb)
            opt.zero_grad()
            y_hat_mb = model((qa_mb, qb_mb))
            mb_loss = log_loss(y_hat_mb, y_mb)
            mb_loss.backward()
            opt.step()

            with torch.no_grad():
                mb_acc = acc(y_hat_mb, y_mb)

            tr_loss += mb_loss.item()
            tr_acc += mb_acc.item()

            if (epoch * len(tr_dl) + step) % model_config.summary_step == 0:
                val_loss = evaluate(model, val_dl, {"loss": log_loss}, device)["loss"]
                writer.add_scalars(
                    "loss",
                    {"train": tr_loss / (step + 1), "val": val_loss},
                    epoch * len(tr_dl) + step,
                )
                tqdm.write(
                    "global_step: {:3}, tr_loss: {:.3f}, val_loss: {:.3f}".format(
                        epoch * len(tr_dl) + step, tr_loss / (step + 1), val_loss
                    )
                )
                model.train()
        else:
            tr_loss /= step + 1
            tr_acc /= step + 1

            tr_summary = {"loss": tr_loss, "acc": tr_acc}
            val_summary = evaluate(model, val_dl, {"loss": log_loss, "acc": acc}, device)
            tqdm.write(
                "epoch : {}, tr_loss: {:.3f}, val_loss: "
                "{:.3f}, tr_acc: {:.2%}, val_acc: {:.2%}".format(
                    epoch + 1,
                    tr_summary["loss"],
                    val_summary["loss"],
                    tr_summary["acc"],
                    val_summary["acc"],
                )
            )

            val_loss = val_summary["loss"]
            is_best = val_loss < best_val_loss

            if is_best:
                state = {
                    "epoch": epoch + 1,
                    "model_state_dict": model.state_dict(),
                    "opt_state_dict": opt.state_dict(),
                }
                summary = {"train": tr_summary, "validation": val_summary}

                summary_manager.update(summary)
                summary_manager.save("summary.json")
                checkpoint_manager.save_checkpoint(state, "best.tar")

                best_val_loss = val_loss
