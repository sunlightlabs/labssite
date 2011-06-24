from blogdor.feeds import LatestPosts, LatestForTag, LatestForAuthor

class LabsLatestPosts(LatestPosts):
    title = "Sunlight Labs blog"
    description = "Latest blog updates from the nerds at Sunlight Labs"

class LabsLatestForTag(LatestForTag):
    feed_title = "Sunlight Labs loves %s"
    feed_description = "Posts from the Sunlight Labs blog tagged with '%s'"

class LabsLatestForAuthor(LatestForAuthor):
    feed_title = "Sunlight Labs' %s"
    feed_description = "Posts written by %s for the Sunlight Labs blog"

