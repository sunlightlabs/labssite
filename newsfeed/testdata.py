post = ItemType.objects.create(name='Blog Post', slug='post', icon_url='page.png', template='newsfeed/post.html')
idea = ItemType.objects.create(name='Idea', slug='idea', icon_url='lightbulb.png', template='newsfeed/idea.html')
event = ItemType.objects.create(name='Event', slug='event', icon_url='calendar.png', template='newsfeed/event.html')

FeedItem.objects.create(title='Hackathon in Cheboygan, MI', link='events/cheboygan-hackathon', user='Bill', item_type=event)
FeedItem.objects.create(title='Looking to Help "The Man", Turning in My Chief Evangelist Badge', body='''“What we’ve learned from the Open House Project,” said Sunlight’s Greg Elin, “is that whenever we sit outside and build things, we learn that there are people inside who want to do the same thing.” That's me, quoted in Matthew Burton's 2008 essay, Why I Help "The Man", and Why You Should, Too.''', link='/blog/gregpost', user='Greg', item_type=post)
FeedItem.objects.create(title='Should Data.gov visualize? Probably not.', body='''A few people who saw our Data.gov design post asked for ways to visualize the data on Data.gov. As an organization that's such a proponent of data not only being free, but also using design to provide context to the data, why don't we advocate for data.gov to have visualizations for citizens to make sense of the data?''', link='/blog/post-link', user='Clay', item_type=post)
FeedItem.objects.create(title='Data Commons', link='ideas/datacommons', user='James', item_type=idea)
FeedItem.objects.create(title='Are("R") You a visualizer?', body='''Yesterday, I posted a bit about how data.gov shouldn't focus on data visualizations, but rather providing clean reliable data to citizens. But what this means is that we as a non-government community really need to start thinking about how to do visualizations when that data becomes available. Right now we're asking a lot of questions about data visualizations inside the Sunlight Offices that need to be shared with the wider Labs community: ''', link='/blog/post-link', user='Clay', item_type=post)

feed = Feed.objects.create(title='main', slug='main')
feed.items = FeedItem.objects.all()

