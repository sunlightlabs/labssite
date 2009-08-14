from blogdor.feeds import LatestComments, LatestPosts, LatestForTag, LatestForAuthor

class LabsLatestPosts(LatestPosts):
    feed_title = "Sunlight Labs blog"
    feed_description = "Latest blog updates from the nerds at Sunlight Labs"

class LabsLatestComments(LatestComments):
    feed_title = "Sunlight Labs blog comments"
    feed_description = "Latest comments from the nerds that read the Sunlight Labs blog"

class LabsLatestForTag(LatestForTag):
    feed_title = "Sunlight Labs loves %s"
    feed_description = "Posts from the Sunlight Labs blog tagged with '%s'"

class LabsLatestForAuthor(LatestForAuthor):
    feed_title = "Sunlight Labs' %s"
    feed_description = "Posts written by %s for the Sunlight Labs blog"

