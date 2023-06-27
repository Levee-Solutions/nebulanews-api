import logging
from pathlib import Path

import pandas as pd
from django.core.management import BaseCommand
from tqdm import tqdm

from core_api.models import NewsArticle, NewsSource

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Create news list from MIND TSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            help="File path containing the TSV file.",
            required=True,
        )

    def handle(self, *args, **options):
        file = Path(options["file"])
        self.stdout.write(self.style.SUCCESS(f"Reading file at {options['file']}"))
        articles = pd.read_csv(
            file,
            sep="\t",
            names=[
                "id",
                "category",
                "subcategory",
                "title",
                "abstract",
                "url",
                "wikidata_title_entities",
                "wikidata_abstract_entities",
            ],
            usecols=[
                "id",
                "category",
                "subcategory",
                "title",
                "abstract",
                "url",
            ],
        )
        for _, article in tqdm(articles.iterrows(), total=articles.shape[0]):
            article_data = article.to_dict()
            article_id = article_data.pop("id")
            try:
                _, _ = NewsArticle.objects.update_or_create(
                    id=article_id,
                    defaults=dict(**article.to_dict(), source=NewsSource.mind),
                )
            except Exception as e:
                tqdm.write(
                    f"Could not create model for news article {article_id} of the form: {article_data}. Exception caught: {e}"
                )

                pass
        self.stdout.write(self.style.SUCCESS("Done!"))
