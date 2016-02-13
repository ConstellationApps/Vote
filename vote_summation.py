class Vote:
    votes = dict()
    ballots = list(list())
    def __init__(self, voteList):
        self.ballots = voteList

    def computeWinners(self):
        for vote in self.ballots:
            for mark in vote:
                if mark not in self.votes:
                    self.votes[mark] = 0
                self.votes[mark] += 1
    
    def getWinners(self):
        return self.votes
