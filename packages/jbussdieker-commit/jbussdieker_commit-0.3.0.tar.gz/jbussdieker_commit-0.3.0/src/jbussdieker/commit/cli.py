from .util import run_commit


def register(subparsers):
    parser = subparsers.add_parser(
        "commit", help="Generate and create a conventional commit"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate commit message without creating commit",
    )
    parser.set_defaults(func=main)


def main(args):
    try:
        # run_commit(config.openai_api_key, dry_run=args.dry_run)
        run_commit(None, dry_run=args.dry_run)
    except Exception as e:
        logging.error(f"Commit failed: {e}")
        return 1
