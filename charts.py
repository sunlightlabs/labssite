
def people_skills_piechart():
    return tag_piechart(People)

def projects_piechart():
    counts = Project.objects.values('official').annotate(num=Count('id'))
    items = [{'name': 'Sunlight Projects', 'num': 3, 'color': '00ff00'},
             {'name': 'Community Projects', 'num': 5, 'color': '0000ff'}]
    return piechart(items)

def role_piechart():
    colors = {'Developers': '003300', 'Designers': '009900', 'Both': '00cc00',
              'Other': '00ff00'}
    items = Profile.objects.values('role').annotate(Count('id'))
    for item in items:
        item['color'] = colors[item['name']]
    return piechart(counts)

