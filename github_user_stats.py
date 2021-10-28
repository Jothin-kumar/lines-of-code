from github import Github, Repository

github = Github('<token>')
user = github.get_user()


class ContributedRepository:
    def __init__(self, contributed_to: Repository):
        self.total_lines_of_addition_in_contribution = 0
        self.total_lines_of_deletion_in_contribution = 0
        self.name = contributed_to.full_name
        for contribution in contributed_to.get_stats_contributors():
            if contribution.author.id == user.id:
                for week in contribution.weeks:
                    self.total_lines_of_addition_in_contribution += week.a
                    self.total_lines_of_deletion_in_contribution += week.d
        if not any([self.total_lines_of_addition_in_contribution, self.total_lines_of_deletion_in_contribution]):
            raise ValueError('User have not contributed to this repository.')


class OwnedRepository:
    def __init__(self, owned_repository: Repository):
        self.total_lines_of_addition = 0
        self.total_lines_of_deletion = 0
        self.name = owned_repository.name
        for contribution in owned_repository.get_stats_contributors():
            if contribution.author.id == user.id:
                for week in contribution.weeks:
                    self.total_lines_of_addition += week.a
                    self.total_lines_of_deletion += week.d


contributed_repos = []
own_repos = []
for repo in user.get_repos():
    if repo.fork:
        try:
            contributed_repos.append(ContributedRepository(contributed_to=repo.parent))
        except ValueError:
            pass
    else:
        own_repos.append(OwnedRepository(owned_repository=repo))
