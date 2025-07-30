import argparse
import sys

from akride.client import AkriDEClient


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Akride ingestion utility.")
    sub_parser = parser.add_subparsers(
        help="sub command", dest="command", required=True
    )
    ingest_parser = sub_parser.add_parser("ingest", help="ingest data")

    ingest_parser.add_argument(
        "-n", "--dataset_name", type=str, help="Dataset Name"
    )

    ingest_parser.add_argument(
        "-d", "--dataset_id", type=str, help="Dataset Id"
    )

    ingest_parser.add_argument(
        "-f",
        "--featurizer_type",
        choices=["patch", "full"],
        default="patch",
        type=str,
        help="Featurizer type",
    )

    ingest_parser.add_argument(
        "-c",
        "--with_clip",
        choices=["yes", "no"],
        default="yes",
        type=str,
        help="CLIP needed",
    )

    ingest_parser.add_argument(
        "-i",
        "--input_dir",
        required=True,
        type=str,
        help="Input directory path",
    )

    ingest_parser.add_argument(
        "-e", "--endpoint", required=True, type=str, help="Saas endpoint"
    )
    ingest_parser.add_argument(
        "-a", "--api_key", required=True, type=str, help="Api key"
    )

    # Parse arguments
    args = parser.parse_args()
    dataset_name = args.dataset_name
    dataset_id = args.dataset_id
    featurizer_type = args.featurizer_type
    with_clip = args.with_clip
    input_dir = args.input_dir
    endpoint = args.endpoint
    api_key = args.api_key

    if not dataset_name and not dataset_id:
        raise Exception(
            "one of the arguments -n/--dataset_name -d/--dataset_id is required"
        )

    # Initialize client
    de_client = AkriDEClient(saas_endpoint=endpoint, api_key=api_key)

    if dataset_id:
        datasets = de_client.get_datasets(
            attributes={"filter_by_ids": [dataset_id]}
        )
        if not datasets:
            raise Exception(f"Dataset with id `{dataset_id}` is not found")
        dataset = datasets[0]
    else:
        # Fetch dataset by name
        dataset = de_client.get_dataset_by_name(dataset_name)
        if not dataset:
            raise Exception(f"Dataset with name `{dataset_name}` is not found")

    # Start ingestion
    task = de_client.ingest_dataset(
        dataset=dataset,
        data_directory=input_dir,
        use_patch_featurizer=featurizer_type == "patch",
        with_clip_featurizer=with_clip == "yes",
        async_req=False,
    )
    # Exit with non-zero exit code if task has failed
    if task.has_failed():
        sys.exit(1)


if __name__ == "__main__":
    main()
