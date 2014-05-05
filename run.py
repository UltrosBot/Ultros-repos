__author__ = 'Gareth Coles'

from git import repo

r = repo.Repo(".")

origin = r.remotes.origin
print origin.refs

result = origin.pull()

for x in result:
    print x
