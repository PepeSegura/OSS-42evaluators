import time
from django.db import transaction, OperationalError
from update_database.our_network_manager import *

def manageProject(project_data, user_instance):
    """
    Updates an existing project if the marked_at field has changed for the given user,
    or creates a new project if it does not exist or the user is different.

    Parameters:
    - project_data: A dictionary containing project data.
    - user_instance: An instance of the User model representing the user associated with the project.

    Returns:
    None
    """
    try:
        existing_project = Project.objects.get(name=project_data["name"], user=user_instance)
        if existing_project.marked_at != project_data['marked_at']:
            Project.objects.filter(id=existing_project.id).update(
                    status      = project_data['status'],
                    validated   = project_data['validated'],
                    final_mark  = project_data['final_mark'],
                    marked_at   = project_data['marked_at'],
                    )
    except ObjectDoesNotExist:
        Project.objects.create(
            name        = project_data["name"],
            slug        = project_data["slug"],
            project_id  = project_data["project_id"],
            status      = project_data["status"],
            validated   = project_data["validated"],
            final_mark  = project_data["final_mark"],
            marked_at   = project_data["marked_at"],
            cursus_id   = project_data["cursus_id"],
            user        = user_instance,
        )

cursus_names = {
        77      : "Discovery Piscine - AI",
        76      : "Remote Discovery - Web",
        75      : "Piscine Pro - AI",
        74      : "Piscine Pro - Cybersecurity",
        73      : "H2G2",
        69      : "Discovery Piscine - Python",
        68      : "Discovery Piscine - Cybersecurity",
        67      : "42 events",
        66      : "C-Piscine-Reloaded",
        65      : "C Piscine Antwerp",
        64      : "C Piscine Brussels",
        63      : "Discovery | Nice",
        62      : "Abu Dhabi",
        61      : "CodingInActionLabs",
        60      : "42Cursus-WarmUp-SP",
        59      : "Turbo 4.2",
        58      : "[DEPRECATED] Bootcamp Cybersecurity",
        57      : "42 Labs São Paulo",
        56      : "Seoul Labs",
        54      : "42Test",
        53      : "42.zip",
        52      : "Basecamp Warm Up| Rio",
        51      : "Basecamp | Rio",
        50      : "Road to",
        49      : "Hive Basecamp",
        48      : "problem-solving",
        47      : "Bocom test",
        46      : "GBRE",
        44      : "Paris Basecamp",
        43      : "Brussels Basecamp",
        42      : "Germany Basecamp",
        41      : "Basecamp Warm Up Germany",
        40      : "test-gb-v1",
        39      : "101",
        38      : "Basecamp WarmUp",
        37      : "msk-test",
        36      : "Basecamp",
        35      : "Java piscine",
        34      : "Data science piscine",
        33      : "42tokyo-playground",
        32      : "42 seoul events",
        31      : "kor-test",
        28      : "Reloaded",
        27      : "Madrid RPA",
        26      : "H2STest",
        25      : "micropiscine-web-101",
        23      : "python-101",
        22      : "static-riddle-101",
        21      : "42cursus",
        20      : "Boost",
        19      : "Atlantis",
        18      : "Starfleet",
        17      : "H2S",
        16      : "X-Mansion-Namido",
        15      : "X-Mansion",
        14      : "Technical Interview",
        13      : "42 Labs",
        12      : "Créa",
        11      : "BootCamp",
        10      : "Formation Pole Emploi",
        9       : "C Piscine",
        8       : "WeThinkCode_",
        7       : "Piscine C à distance",
        6       : "Piscine C décloisonnée",
        5       : "42partnerships",
        4       : "Piscine C",
        3       : "Discovery Piscine - Web",
        1       : "42"
}

def manageCursus(cursus_data, user_instance):
    """
    Updates an existing cursus if the relevant fields have changed for the given user,
    or creates a new cursus if it does not exist or the user is different.

    Parameters:
    - cursus_data: A dictionary containing cursus data.
    - user_instance: An instance of the User model representing the user associated with the cursus.

    Returns:
    None
    """
    cursus_name = cursus_names.get(cursus_data["cursus_id"], "Unknown Cursus Name")
    try:
        existing_cursus = Cursus.objects.get(cursus_id=cursus_data["cursus_id"], user=user_instance)

        if existing_cursus.level != cursus_data["level"] or existing_cursus.blackholed_at != cursus_data.get("blackholed_at"):
            Cursus.objects.filter(id=existing_cursus.id).update(
                    level           = cursus_data['level'],
                    blackholed_at    = cursus_data['blackholed_at'],
                    )
    except ObjectDoesNotExist:
        Cursus.objects.create(
                name            = cursus_name,
                cursus_id       = cursus_data['cursus_id'],
                level           = cursus_data['level'],
                blackholed_at   = cursus_data['blackholed_at'],
                begin_at        = cursus_data['begin_at'],
                user            = user_instance,
                )


def getUserInfo(user_id):
    """
    This function will be called from updateDatabase() if any user has changed
    It will make a request to the specific user to get info about his cursus and projects
    """
    params = {}
    response = makeRequest(API_URL + "/users/" + str(user_id), params)

    campuses = response.get('campus_users', [])
    is_from_madrid = any(campus['campus_id'] == 22 and campus['is_primary'] for campus in campuses)

    if not is_from_madrid:
        return

    default_date = datetime.max.isoformat()
    projects_data = sorted(
            response['projects_users'],
            key=lambda x: x["marked_at"] or default_date,
            reverse=True
            )
    filter_projects = [
        {
            "name"          : entry.get('project').get('name'),
            "slug"          : entry.get('project').get('slug'),
            "project_id"    : entry.get('id'),
            "status"        : entry.get('status'),
            "validated"     : entry.get('validated?'),
            "final_mark"    : entry.get('final_mark'),
            "marked_at"     : entry.get('marked_at'),
            "cursus_id"     : entry.get('cursus_ids')[0],
        }
        for entry in projects_data
        if entry.get('marked_at') and entry.get('cursus_ids')
    ]

    cursus_data = response['cursus_users']
    filter_cursus = [
        {
            "level"         : entry.get('level'),
            "begin_at"      : entry.get('begin_at'),
            "blackholed_at" : entry.get('blackholed_at'),
            "cursus_id"     : entry.get('cursus_id'),
        }
        for entry in cursus_data
        if entry.get('cursus')
    ]

    # Fetch or create the Piscine instance
    pool_month = response['pool_month']
    pool_year = response['pool_year']
    piscine, created = Piscine.objects.get_or_create(
        month=pool_month,
        year=pool_year,
        defaults={'sort_order': Piscine.objects.count() + 1}
    )

    user_instance, _ = User.objects.update_or_create(
        user_id=user_id,
        defaults={
            "login"             : response['login'],
            "evaluation_points" : response['correction_point'],
            "location"          : response['location'],
            "wallet"            : response['wallet'],
            "updated_at"        : response['updated_at'],
            "image"             : response['image']['versions']['medium'],
            "active"            : response['active?'],
            "profile_url"       : f"https://profile.intra.42.fr/users/{response['login']}",
            "piscine"           : piscine

        }
    )

    for project in filter_projects:
        manageProject(project, user_instance)
        
    for cursus in filter_cursus:
        manageCursus(cursus, user_instance)

    print(f"all new info from: {response['login']} stored")


def getCampusUsers():
  """
  This function will be called from updateDatabase()
  """
  MADRID = 22
  CURSUS = 21

  g_test_mode = True
  g_test_mode_max_pages = 5
  g_max_results_per_page = 100

  users_data = []

  page = 0

  while (not g_test_mode or g_test_mode_max_pages > 0):

    params = {
      "campus_id"   : MADRID,
      "cursus_id"   : CURSUS,
      "page[size]"  : g_max_results_per_page,
      "page[number]": page
    }

    response = makeRequest(
      API_URL + "/users"
      , params
    )

    for user in response:
      if user["kind"] == "student":
        user_data = {
          "user_id"             : user["id"],
          "login"               : user["login"],
          "evaluation_points"   : user["correction_point"],
          "updated_at"          : user['updated_at'],
          "wallet"              : user["wallet"],
          "profile_pic_url"     : user["image"]["link"],
          "active"              : user['active?'],
          "profile_url"         : f"https://profile.intra.42.fr/users/{user['login']}",
        }
        users_data.append(user_data)
    print(f"page: {page} with len: {len(response)}")
    if len(response) < g_max_results_per_page:
      break

    page += 1
    if g_test_mode:
      g_test_mode_max_pages -= 1

  print (f"Data from [{len(response)}] students", file=sys.stderr)
  return (users_data)


def getClusterMap():
  """
  This function will be called from updateLocations()
  """
  MADRID = 22

  g_test_mode = False
  g_test_mode_max_pages = 10000
  g_max_results_per_page = 100

  all_locations_data = []

  page = 1

  while (not g_test_mode or g_test_mode_max_pages > 0):

    params = {
      "page[size]"      : g_max_results_per_page,
      "page[number]"    : page,
      "filter[active]"  : "true",
    }

    response = makeRequest(
      API_URL + "/campus/" + str(MADRID) + "/locations"
      , params
    )

    for location in response:
        location_data = {
            "host"        : location["host"],
            "begin_at"    : location["begin_at"],
            "user_id"     : location["user"]["id"],
            "profile_url" : f"https://profile.intra.42.fr/users/{location['user']['login']}",
            "image"       : location["user"]["image"]["versions"]["small"],
        }
        all_locations_data.append(location_data)
    print(f"page: {page} with len: {len(response)}")
    if len(response) < g_max_results_per_page:
      break

    page += 1
    if g_test_mode:
      g_test_mode_max_pages -= 1

  print (f"there are [{len(all_locations_data)}] online students", file=sys.stderr)
  return (all_locations_data)


def updateDatabase():
  """
  This function will be called from the schedule_update.py
  1. call to getCampusUsers() to get jsonArray with the data from all the students from 42Madrid
  2. for every user in the jsonArray, it will check if any user has updated info
  3. call to getUserInfo() for every user with different data from the database
  """
  print('Starting update cursus job...')
  campus_users = getCampusUsers()
  if campus_users is not None:
    for user in campus_users:
      try:
        existing_user = User.objects.filter(user_id=user['user_id']).first()
        if existing_user and (existing_user.evaluation_points != user['evaluation_points'] or existing_user.updated_at != user['updated_at']): #if user has changed: UPDATE USER
            getUserInfo(user['user_id'])
            print(f"User {user['login']} updated.")
        elif existing_user: #if user has not change: DO NOTHING
          continue
        else: #if user does not exist: CREATE USER
            getUserInfo(user['user_id'])
            print(f"New User {user['login']} added.")
      except Exception as e:
        print(f"Failed to update user {user['login']}: {str(e)}")
  print('Update cursus job done!')


def updateLocations():
    """
    This function will be called from the schedule_update.py
    1. call to getClusterMap() to get jsonArray with the campus locations
    2. delete all the items from the ClusterLocation database
    3. populate de ClusterLocation database with the data from the jsonArray
    """
    print('Starting update locations job...')
    
    locations = getClusterMap()
    max_retries = 2
    retry_delay = 0.2  # seconds

    def attempt_operation(operation):
        for attempt in range(max_retries):
            try:
                return operation()
            except OperationalError as e:
                if 'database is locked' in str(e):
                    time.sleep(retry_delay)
                else:
                    raise

    # Delete all ClusterLocation objects with retry mechanism
    attempt_operation(lambda: ClusterLocation.objects.all().delete())
    print("ClusterLocation records deleted.")

    if locations is not None:
        for location in locations:
            attempt_operation(lambda: update_or_create_location(location))

    print('Update locations job done!')


def update_or_create_location(location):
    user_instance = User.objects.filter(user_id=location['user_id']).first()
    if user_instance is None:
        return  # Skip if user not found

    with transaction.atomic():
        ClusterLocation.objects.update_or_create(
            host=location['host'],
            defaults={
                "begin_at": location['begin_at'],
                "profile_url": location['profile_url'],
                "image": location['image'],
                "user": user_instance,
            }
        )
