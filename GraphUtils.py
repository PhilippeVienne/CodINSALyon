from model import Base

class GraphUtils(object):
    """

    Utils for managing the map graph

    """
    @staticmethod
    def get_neighbours(b):
        """
        @param{Base} b
        @return [FullView]
        """
        return [a.next() for a in b.axes()]

    @staticmethod
    def interconnection_score_from_country(b, country, depth):
        """
        @param{Base} b
        @param{int} depth
        @return int
        """
        pos_from = country.position()
        if depth is 0:
            return 1
        score = 0
        dist_b = pos_from.squareDistanceTo(b.position())
        dist_b += dist_b * 5 / 100.0  # 5% margin to allow for slightly further nodes
        for a in GraphUtils.get_neighbours(b):
            dist = pos_from.squareDistanceTo(a.position())
            if dist <= dist_b:  # We only count towards the score, the nodes that are in the direction of the country, relative to this current node
                score += GraphUtils.interconnection_score_from_country(a, country, depth-1)
        return score