"""Define user and item features that can be used by the Hybrid Recommender."""


class UserFeatures:
    """Define user features."""

    def __init__(self):
        self.features = [
            "age",
            "gender",
        ]


class ItemFeatures:
    """Define item features."""

    def __init__(self):
        self.features = [
            "unknown",
            "Action",
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film_Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci_Fi",
            "Thriller",
            "War",
            "Western",
        ]
