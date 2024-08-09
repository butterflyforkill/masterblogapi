


def sortingby(sort_by, direction_sort, blog_posts):
    if sort_by and direction_sort:
        return sorted(blog_posts, key=lambda x: x.get(sort_by, ""), reverse=(direction_sort == 'desc'))
    else:
        return sorted(blog_posts, key=lambda x: x.get('date', ""), reverse=(direction_sort == 'desc'))
    
    
print(sortingby('Let me love', "desc", [
    {
        "id": 19492219888727943634658101245175567792,
        "title": "iuiui",
        "content": "jkjkjkjkoo",
        "author": "Molina",
        "date": "2024-08-08"
    },
    {
        "id": 99433177330348234564350261618617104645,
        "title": "Hello how",
        "content": "Don't got away",
        "author": "Elis",
        "date": "2024-08-09"
    },
    {
        "id": 246066813733820383810268514818545446105,
        "title": "Let me love you",
        "content": "Day6 sonngs are amazing",
        "author": "Molina",
        "date": "2024-08-09"
    },
    {
        "id": 228866718248447822946344764221351711977,
        "title": "Sad Ending",
        "content": "Of Your life",
        "author": "Elis",
        "date": "2024-08-09"
    }
]))