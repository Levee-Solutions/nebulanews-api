import logging
from pathlib import Path

import pandas as pd
from django.core.management import BaseCommand

from core_api.models import NewsArticle, NewsSource

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Create news list from local files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            help="File path containing the news.",
            required=True,
        )

    def handle(self, *args, **options):
        file = Path(options["file"])
        self.stdout.write(self.style.INFO(f"Reading file at {options['file']}"))
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
        for _, article in articles.iterrows():
            model_article = NewsArticle(**article.to_dict(), source=NewsSource.mind)
            model_article.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created article {article['id']}: {article['title']}"
                )
            )
