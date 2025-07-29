import argparse
from aider_rag.rag_pipeline import build_vectorstore
from aider_rag.aider_runner import run_aider

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()

    run_aider(args.file, args.prompt)

if __name__ == "__main__":
    main()
