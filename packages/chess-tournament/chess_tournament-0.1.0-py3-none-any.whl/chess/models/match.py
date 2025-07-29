class Match:
    """Represents a match between two players."""

    def __init__(self, joueur1, joueur2, score):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score = score  # [score1, score2]

    def to_dict(self):
        return {"joueur1": self.joueur1, "joueur2": self.joueur2, "score": self.score}

    @classmethod
    def from_dict(cls, data):
        return cls(data["joueur1"], data["joueur2"], data["score"])
