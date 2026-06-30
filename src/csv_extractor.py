import pandas as pd


REQUIRED_COLUMNS = [
    "name",
    "email",
    "phone",
    "current_company",
    "title"
]


class CSVExtractor:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def extract(self):
        """
        Read recruiter CSV and return candidate data.
        """

        try:
            df = pd.read_csv(self.csv_path)

        except FileNotFoundError:
            raise Exception(f"CSV file not found: {self.csv_path}")

        except Exception as e:
            raise Exception(f"Unable to read CSV: {e}")

        # Empty CSV
        if df.empty:
            raise Exception("CSV file is empty.")

        # Check required columns
        missing = []

        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                missing.append(column)

        if missing:
            raise Exception(
                f"Missing required columns: {', '.join(missing)}"
            )

        # Assignment contains one candidate
        row = df.iloc[0]

        candidate = {
            "name": str(row["name"]).strip(),
            "email": str(row["email"]).strip(),
            "phone": str(row["phone"]).strip(),
            "current_company": str(row["current_company"]).strip(),
            "title": str(row["title"]).strip()
        }

        return candidate