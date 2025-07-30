"""Constants for the preprocess stage of the heart failure DVC pipeline."""


class PreprocessConstants:
    """Constants for the preprocess stage of the heart failure DVC pipeline."""

    SCALER = "scaler.pkl"
    FEATURE_DISTRIBUTIONS = "distribution_statistics.parquet"
    NUMERICAL_FEATURES = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]
    FEATURES_TO_ENCODE = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
    FEATURES_TO_IMPUTE = ["Cholesterol", "RestingBP"]
