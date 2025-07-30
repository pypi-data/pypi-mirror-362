import json
import os


os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from huggingface_hub import ModelCard, create_repo, upload_file, upload_large_folder, whoami

from audiozen.trainer_utils import collect_env


@dataclass
class Args:
    # The path to the model folder
    model_folder_path: str = "/path/to/your/model"
    # Whether the repo should be private
    private: bool = True
    # Whether to only upload `exp` folder
    only_exp_folder: bool = False
    # Whether to only upload the best checkpoint. If True, all other checkpoints will be ignored.
    only_best_checkpoint: bool = True
    # Whether to create a model card, or upload the README.md file if it exists
    create_model_card: bool = True


def generate_repo_id(model_folder_path: Path) -> str:
    """recipes/dns_icassp_2023/**/bsrnn => dns_icassp_2023_**_bsrnn."""
    # Get username
    user = whoami()["name"]

    path_parts = model_folder_path.parts
    # Get all parts after "recipes"
    valid_path_parts = path_parts[path_parts.index("recipes") + 1 :]

    repo_name = "__".join(valid_path_parts)
    repo_id = f"{user}/{repo_name}"

    print(f"Will upload model path {model_folder_path.as_posix()} to repo id {repo_id}")
    return repo_id


def get_git_revision_hash(model_folder_path: Path) -> str:
    return subprocess.check_output(["git", "-C", model_folder_path, "rev-parse", "HEAD"]).strip().decode("utf-8")


def push_to_huggingface_hub(args: Args):
    """Push a model to the Hugging Face Hub.

    Args:
        args (Args): The arguments to push the model to the Hugging Face Hub.

    Notes:
        The model will be pushed to the Hugging Face Hub with the following structure:
        ```
        recipes/
            path/
                to/
                    model/
                        README.md
                        exp/
                        other_files/
        ```
    """
    model_folder_path = Path(args.model_folder_path).absolute()
    assert model_folder_path.exists(), f"Model folder {model_folder_path} does not exist."

    # Create a new repo on the hugingface hub if it doesn't exist
    repo_id = generate_repo_id(model_folder_path)
    repo_url = create_repo(repo_id=repo_id, token=None, private=args.private, repo_type="model", exist_ok=True)
    print(f"Created repo at `{repo_url}`")

    # Create a model card (README.md)
    # First check if the user wants to create a model card
    # If yes, create a model card with the following content:
    # If no, check if a README.md file exists in the model folder, and upload it to the repo
    if args.create_model_card:
        print(f"> Creating a auto-generated README.md for {repo_id}")

        model_card_content = f"""
---
language: en
license: mit
---
# {repo_id.split("/")[-1]}

This project was initially created for personal use and is now archived.
While the code and documentation may be incomplete, I'm happy to share it in case others find it useful.

This model was uploaded from AudioZen at **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**.

## Overview

- **Training folder:** `{model_folder_path.as_posix()}`
- **Git hash:** `{get_git_revision_hash(model_folder_path)}`

## Usage

Refer to https://huggingface.co/docs/hub/en/models-downloading for instructions on how to download this model.
For example, you can use the following code to download the model:

```bash
# Install git lfs if you haven't already
git lfs install

# Go into the directory where you want to download the model
cd {model_folder_path.parent.as_posix()}

# Clone the model checkpoint
git clone https://huggingface.co/{repo_id}
# or
git clone git@hf.co:/{repo_id}
```

## Model Architecture

- Model architecture:
- Hyperparameters: Check the `config.yaml` file in the training folder for hyperparameters.


## Environment Info

<details>

{collect_env()}

Note: This information was generated automatically when the model was uploaded instead of when the model was trained.
</details>

## Upload Arguments

<details>

```python
{json.dumps(vars(args), indent=4, sort_keys=True)}
```

</details>
        """

        model_card = ModelCard(model_card_content)
        model_card.save(model_folder_path / "modelcard.md")
        model_card.push_to_hub(repo_id=repo_id)
    else:
        print("> Not creating a ModelCard, uploading README.md if it exists...")
        if (model_folder_path / "README.md").exists():
            upload_file(path_or_fileobj=(model_folder_path / "README.md"), path_in_repo="README.md", repo_id=repo_id)
        else:
            print(f"> No README.md found in {model_folder_path}")

    # Upload model files and tensorboard logs
    print(f"> Uploading model files to `{repo_url}`...")

    upload_folder_kwargs = {
        "repo_id": repo_id,
        "repo_type": "model",
        "ignore_patterns": ["*__pycache__*", "*.nfs*"],
    }

    # If the user only wants to upload the `exp` folder, set the folder path to the `exp` folder
    if args.only_exp_folder:
        print("> Only uploading `exp` folder")
        upload_folder_kwargs["folder_path"] = (model_folder_path / "exp").as_posix()
        upload_folder_kwargs["path_in_repo"] = "exp"
    else:
        upload_folder_kwargs["folder_path"] = model_folder_path.as_posix()

    # If the user only wants to upload the best checkpoint, ignore all other checkpoints
    if args.only_best_checkpoint:
        print("> Only uploading the best checkpoint")
        upload_folder_kwargs["ignore_patterns"].append("**/epoch_*")
    else:
        # TODO Can We only upload the latest 10 checkpoints?
        print("> Uploading all checkpoints (best and `epoch_*` checkpoints)")

    upload_large_folder(**upload_folder_kwargs)

    print(f"Model uploaded to {repo_url}")
