from datasets import load_dataset


class DatasetLoader:
    """Loader for Indonesian NLP datasets from HuggingFace."""

    def load_stopwords_dataset(self, language="indonesian"):
        ds = load_dataset("nahiar/indo-stopwords")
        # Ambil list stopwords dari split 'train', field 'stopword'
        return [item["stopword"] for item in ds["train"]]  # type: ignore

    def load_slang_dataset(self, language="indonesian"):
        ds = load_dataset("nahiar/indonesia-slang")
        # Ambil list dict slang-formal dari split 'train'
        return [
            {"slang": item["slang"], "formal": item["formal"]} for item in ds["train"]  # type: ignore
        ]

    def load_emoji_dataset(self, language="indonesian"):
        ds = load_dataset("nahiar/indo-emoji-dictionary")
        # Ambil list dict emoji dari split 'train'
        return [dict(item) for item in ds["train"]]
