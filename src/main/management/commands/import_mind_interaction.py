import logging
from pathlib import Path

import pandas as pd
from django.core.management import BaseCommand
from tqdm import tqdm

from core_api.models import NewsArticle, NewsImpression, NewsSource
from management.models import User

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Create impressions from MIND TSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            help="File path containing the TSV file.",
            required=True,
        )

    def handle(self, *args, **options):
        file = Path(options["file"])
        self.stdout.write(self.style.SUCCESS(f"Reading file at {options['file']}"))
        impressions = pd.read_csv(
            file,
            sep="\t",
            names=[
                "id",
                "user",
                "timestamp",
                "history",
                "impressions",
            ],
            usecols=[
                "user",
                "timestamp",
                "history",
                "impressions",
            ],
        )
        impressions["timestamp"] = pd.to_datetime(impressions["timestamp"])
        for user_id, interactions in tqdm(impressions.groupby("user")):
            session = user_id.replace("U", "S")
            # Get or create user
            user, _ = User.objects.get_or_create(id=user_id)
            # Get user history previous to impressions
            base_timestamp = interactions["timestamp"].min()
            history = (
                interactions["history"].dropna().str.split().explode().drop_duplicates()
            )
            # Get user impressions
            interactions["impressions"] = interactions["impressions"].str.split()
            new_impressions = interactions[["timestamp", "impressions"]].explode(
                "impressions"
            )
            new_impressions[["article", "clicked"]] = new_impressions[
                "impressions"
            ].str.split("-", expand=True)
            new_impressions = new_impressions[
                new_impressions["clicked"] == "1"
            ].drop_duplicates()
            # Create all interactions as models
            for _, article_id in history.items():
                try:
                    article = NewsArticle.objects.get(id=article_id)
                    impression = NewsImpression(
                        user=user,
                        article=article,
                        timestamp=base_timestamp,
                        session=session,
                    )
                    impression.save()
                except NewsArticle.DoesNotExist:
                    tqdm.write(f"Could not find model for news article {article_id}")
                    pass
                except Exception as e:
                    tqdm.write(
                        f"Could not create model for interaction {user,article_id,base_timestamp,session}. Exception caught: {e}"
                    )
                    pass
            for _, row in new_impressions.iterrows():
                try:
                    article = NewsArticle.objects.get(id=row["article"])
                    impression = NewsImpression(
                        user=user,
                        article=article,
                        timestamp=row["timestamp"],
                        session=session,
                    )
                    impression.save()
                except NewsArticle.DoesNotExist:
                    tqdm.write(
                        f"Could not find model for news article {row['article']}"
                    )
                    pass
                except Exception as e:
                    tqdm.write(
                        f"Could not create model for interaction {user,row['article'],row['timestamp'],session}. Exception caught: {e}"
                    )
                    pass
        self.stdout.write(self.style.SUCCESS("Done!"))
