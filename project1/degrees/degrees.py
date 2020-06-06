import csv
import sys
from util import QueueFrontier, Node, StackFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def reverse(ans):
    answer=set()
    for index in range(ans.__len__()):
        k=ans.pop()
        answer.add(k)

    return answer



def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    expolred_set = {}
    queue = QueueFrontier()
    parent = source

    source_node = Node(parent, None, None)

    neighbours = neighbors_for_person(parent)
    expolred_set[parent] = parent
    no_of_parent_neighbour = neighbours.__len__()

    for index in range(no_of_parent_neighbour):
        neighbour_of_parent = neighbours.pop()
        node = Node(neighbour_of_parent[1], source_node, neighbour_of_parent[0])
        expolred_set[neighbour_of_parent[1]] = neighbour_of_parent[1]
        queue.add(node)

    while True:

        if queue.empty() == True:
            return None
        frontier_node = queue.remove()
        target_node = frontier_node
        parent = frontier_node.state
        neighbours = neighbors_for_person(parent)
        no_of_parent_neighbour = neighbours.__len__()
        for index in range(no_of_parent_neighbour):
            neighbour_of_parent = neighbours.pop()
            if expolred_set.__contains__(neighbour_of_parent[1]) == False:
                expolred_set[neighbour_of_parent[1]] = neighbour_of_parent[1]
                if queue.contains_state(neighbour_of_parent[1]) == False:
                    node = Node(neighbour_of_parent[1], frontier_node, neighbour_of_parent[0])
                    queue.add(node)

        if parent == target:
            break

    check = set()
    while target_node.state != source:
        check.add((target_node.action, target_node.state))
        target_node = target_node.parent

    k = check.pop()
    check.add(k)
    answer = list(check)


    if k[1] == target:
        answer.reverse()

    return answer

    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
