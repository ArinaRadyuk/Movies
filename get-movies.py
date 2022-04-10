import re
import csv
import argparse


def normalize_request(request):
    """
    reads the whole file into list if there are no other filters and sorts vector by rating
    """
    if len(request) == 0:
        read_the_whole_file(request)
    request.sort(key=lambda x: x[3], reverse=True)


def get_total_ratings():
    """
    returns a dictionary: key = id, value = sum of all grades
    """
    list_grades = {}
    for _, movieID, rating, _ in open_file('ratings.csv'):
        if movieID in list_grades:
            list_grades[movieID] = list_grades[movieID][0] + float(rating), list_grades[movieID][1] + 1
        else:
            list_grades[movieID] = [float(rating), 1]
    return list_grades


def get_average_rating(list_grades):
    """
    returns a dictionary: key = id, value = average rating
    """
    for movie_ID in list_grades:
        total = list_grades[movie_ID][0]
        count = list_grades[movie_ID][1]
        list_grades[movie_ID] = total/count
    return list_grades


def read_the_whole_file(request):
    """
    creates a list, which contains information on films: request[i] = [genre, name, year, rating]
    """
    for movieID, orig_title, genres in open_file('movies.csv'):
        search_result = re.search("^(.*) \((\d{4})\)$", orig_title)
        if search_result:
            year = int(search_result.group(2))
            title = search_result.group(1)
        else:
            year = None
            title = orig_title
        rating = d.get(movieID)
        genres = genres.split('|')
        for genre in genres:
            request.append([genre, year, title, rating])


def open_file(src_filename):
    """
    checks source file
    """
    try:
        reader = csv.reader(open(src_filename, 'r'), delimiter=',')
        next(reader)
    except Exception as e:
        print('Error:{}:{}'.format(e.strerror, e.filename))
    return reader


def get_sorted_n(request, n):
    """
    returns a list of N higher rated films for each genre
    """
    result = list()
    range_of_genres = list()
    counter = 0
    for genre, year, title, rating in request:
        if counter == n and genre in range_of_genres:
            continue
        if genre not in range_of_genres:
            counter = 0
            range_of_genres.append(genre)
            result.append([genre, year, title, rating])
            counter += 1
        else:
            result.append([genre, year, title, rating])
            counter += 1
    return result


def get_sorted_by_genres(request, arg_genres):
    """
    returns a list of higher rated films of chosen genres
    """
    result = list()
    arg_genres = arg_genres.split('|')
    for genre, year, title, rating in request:
        if genre in arg_genres:
            result.append([genre, year, title, rating])
    return result


def get_sorted_by_year_from(request, year_from):
    """
    returns a list of higher rated films shot later than chosen year
    """
    result = list()
    for genre, year, title, rating in request:
        if year is None:
            continue
        if year_from <= year:
            result.append([genre, year, title, rating])
    return result


def get_sorted_by_year_to(request, year_to):
    """
    returns a list of higher rated films shot earlier than chosen year
    """
    result = list()
    for genre, year, title, rating in request:
        if year is None:
            continue
        if year_to >= year:
            result.append([genre, year, title, rating])
    return result


def get_sorted_by_regexp(request, regexp):
    """
    returns a list of higher rated films the title of which matches the chosen regular expression
    """
    result = list()
    for genre, year, title, rating in request:
        if re.match(regexp, title, re.IGNORECASE):
            result.append([genre, year, title, rating])
    return result


def get_args():
    parser = argparse.ArgumentParser(description='Films')
    parser.add_argument('--N', dest='N', type=int, default=None,
                        help="the number of films ")
    parser.add_argument('--genres', dest='genres', type=str, default=None,
                        help="a string with a list of genres")
    parser.add_argument('--year_from', dest='year_from', type=int, default=None,
                        help="the film was shot later than the specified year")
    parser.add_argument('--year_to', dest='year_to', type=int, default=None,
                        help="the film was shot earlier than the specified year")
    parser.add_argument('--regexp', dest='regexp', type=str, default=None,
                        help="a word or a group of words that should be included in the title")

    return parser.parse_args()


if __name__ == '__main__':
    request = list()
    d = get_average_rating(get_total_ratings())  # dictionary {index of film:rating}
    args = get_args()

    if args.N:
        normalize_request(request)
        request.sort(key=lambda x: x[0])
        request = get_sorted_n(request, args.N)
    if args.genres:
        normalize_request(request)
        request = get_sorted_by_genres(request, args.genres)
        request.sort(key=lambda x: x[0])
    if args.year_from:
        normalize_request(request)
        request = get_sorted_by_year_from(request, args.year_from)
    if args.year_to:
        normalize_request(request)
        request = get_sorted_by_year_to(request, args.year_to)
    if args.regexp:
        normalize_request(request)
        request = get_sorted_by_regexp(request, args.regexp)
    else:
        normalize_request(request)
        request.sort(key=lambda x: x[0])
    if request is not None:
        for genre, year, title, rating in request:
            print(genre, year, title, rating, sep=", ")

