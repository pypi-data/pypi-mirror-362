import time

from tabulate import tabulate
from tqdm import tqdm

from reviewtally.queries.local_exceptions import (
    GitHubTokenNotDefinedError,
    LoginNotFoundError,
    NoGitHubOrgError,
)

from .cli.parse_cmd_line import parse_cmd_line
from .queries.get_prs import get_pull_requests_between_dates
from .queries.get_repos_gql import get_repos_by_language
from .queries.get_reviewers_rest import (
    get_reviewers_with_comments_for_pull_requests,
)

DEBUG_FLAG = False


def timestamped_print(message: str) -> None:
    if DEBUG_FLAG:
        print(  # noqa: T201
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}", flush=True,
        )


BATCH_SIZE = 5


def main() -> None:
    # map containing the reviewer name and the number of pull requests reviewed
    start_time = time.time()
    timestamped_print("Starting process")
    reviewer_stats: dict[str, dict[str, int]] = {}
    org_name, start_date, end_date, languages = parse_cmd_line()
    try:
        timestamped_print(
            f"Calling get_repos_by_language {time.time() - start_time:.2f} "
            "seconds",
        )
        repo_names = tqdm(get_repos_by_language(org_name, languages))
    except GitHubTokenNotDefinedError as e:
        print("Error:", e)  # noqa: T201
        return
    except NoGitHubOrgError as e:
        print("Error:", e)  # noqa: T201
        return
    timestamped_print(
        f"Finished get_repos_by_language {time.time() - start_time:.2f} "
        f"seconds for {len(repo_names)} repositories",
    )
    timestamped_print(
        "Calling get_pull_requests_between_dates "
        f"{time.time() - start_time:.2f} seconds",
    )
    # it is possible to take these asynchronous requests and
    # batch them to improve performance.
    # get all the repo names

    for repo in repo_names:
        timestamped_print(f"Processing {repo}")
        pull_requests = get_pull_requests_between_dates(
            org_name,
            repo,
            start_date,
            end_date,
        )
        timestamped_print(
            "Finished get_pull_requests_between_dates "
            f"{time.time() - start_time:.2f} seconds for "
            f"{len(pull_requests)} pull requests",
        )
        pr_numbers = [pr["number"] for pr in pull_requests]
        repo_names.set_description(f"Processing {org_name}/{repo}")
        # create batches of 5 pr_numbers
        pr_numbers_batched = [
            pr_numbers[i: i + BATCH_SIZE]
                for i in range(0, len(pr_numbers), BATCH_SIZE)
        ]
        for pr_numbers in pr_numbers_batched:
            reviewer_data = get_reviewers_with_comments_for_pull_requests(
                org_name, repo, pr_numbers,
            )
            for review in reviewer_data:
                user = review["user"]
                if "login" not in user:
                    raise LoginNotFoundError

                login: str = user["login"]
                comment_count = review["comment_count"]

                if login not in reviewer_stats:
                    reviewer_stats[login] = {
                        "reviews": 0,
                        "comments": 0,
                    }

                reviewer_stats[login]["reviews"] += 1
                reviewer_stats[login]["comments"] += comment_count
        timestamped_print(
            "Finished processing "
            f"{repo} {time.time() - start_time:.2f} seconds",
        )
    # convert the dictionary to a list of lists and print out with tabulate
    timestamped_print(
        f"Printing results {time.time() - start_time:.2f} seconds")
    table = [
        [
            login,
            stats["reviews"],
            stats["comments"],
            f"{stats['comments'] / stats['reviews']:.1f}"
                if stats["reviews"] > 0 else "0.0",
        ]
        for login, stats in reviewer_stats.items()
    ]
    # convert the dictionary to a list of lists and
    #   sort by the number of PRs reviewed
    table = sorted(table, key=lambda x: (x[1],x[2]), reverse=True)
    print(tabulate(table, ["User", "Reviews", "Comments", "Avg Comments"]))  # noqa: T201


if __name__ == "__main__":
    main()
