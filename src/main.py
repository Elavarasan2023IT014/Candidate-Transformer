from csv_extractor import CSVExtractor
from resume_extractor import ResumeExtractor
from normalizer import Normalizer
from merger import Merger
from projector import Projector
from validator import Validator


def generate_output(candidate_profile, config_path, output_path, output_name):
    """
    Generate projected output using a given config file.
    """

    print(f"\nGenerating {output_name}...")

    projector = Projector(config_path)

    projected_output = projector.project(candidate_profile)

    validator = Validator(config_path)

    if validator.validate_candidate(projected_output):

        projector.save(
            projected_output,
            output_path
        )

        print(f"{output_name} generated successfully.")

    else:

        print(f"{output_name} validation failed.")


def main():

    print("=" * 60)
    print("Candidate Transformer Pipeline")
    print("=" * 60)

    # ---------------------------------------------------
    # Step 1 : Extract Data
    # ---------------------------------------------------

    print("\n[1] Extracting CSV Data...")

    csv_extractor = CSVExtractor("./input/recruiter.csv")
    csv_candidate = csv_extractor.extract()

    print("CSV Extraction Completed")

    print("\n[2] Extracting Resume Data...")

    resume_extractor = ResumeExtractor("./input/resume.pdf")
    resume_candidate = resume_extractor.extract()

    print("Resume Extraction Completed")

    # ---------------------------------------------------
    # Step 2 : Normalize
    # ---------------------------------------------------

    print("\n[3] Normalizing Data...")

    normalizer = Normalizer()

    csv_candidate = normalizer.normalize(csv_candidate)
    resume_candidate = normalizer.normalize(resume_candidate)

    print("Normalization Completed")

    # ---------------------------------------------------
    # Step 3 : Merge
    # ---------------------------------------------------

    print("\n[4] Merging Candidate Information...")

    merger = Merger()

    candidate_profile = merger.merge(
        csv_candidate,
        resume_candidate
    )

    print("Merge Completed")

    # ---------------------------------------------------
    # Step 4 : Generate Default Output
    # ---------------------------------------------------

    generate_output(
        candidate_profile,
        "./input/default_config.json",
        "./output/canonical_output.json",
        "Default Output"
    )

    # ---------------------------------------------------
    # Step 5 : Generate Custom Output
    # ---------------------------------------------------

    generate_output(
        candidate_profile,
        "./input/custom_config.json",
        "./output/custom_output.json",
        "Custom Output"
    )

    print("\n" + "=" * 60)
    print("Pipeline Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()