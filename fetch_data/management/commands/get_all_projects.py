import sys
import os

# Ensure the directory of `our_network_manager.py` is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../update_database')))

from our_network_manager import makeRequest  # Adjust import based on the actual location

from django.core.management.base import BaseCommand
from fetch_data.models import CursusProject  # Replace with your actual model import

API_URL = "https://api.intra.42.fr/v2"

class Command(BaseCommand):
    help = 'Fetches all projects and updates the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting update cursus_projects job...'))
        
        all_projects_data = self.all_projects(22)
        project_with_xp = self.filter_exp(all_projects_data)
        self.save_to_db(project_with_xp)
        
        self.stdout.write(self.style.SUCCESS('Update cursus_projects job done!'))

    def all_projects(self, campus_id):
        g_test_mode = False
        g_test_mode_max_pages = 10000
        g_max_results_per_page = 100

        all_projects_data = []
        page = 1

        while (not g_test_mode or g_test_mode_max_pages > 0):
            params = {
                "page[size]": g_max_results_per_page,
                "page[number]": page           
            }

            self.stdout.write(f"Page Number [{page}]")
            response = makeRequest(
                API_URL + "/cursus/" + str(21) + "/projects", params
            )

            self.stdout.write(f"Response with data from: {len(response)} project(s)")
            self.stdout.write("---------------------------------------------------")
            for project in response:
                for campus in project.get('campus', []):
                    if campus.get('id') == campus_id:
                        project_sessions = project.get('project_sessions')
                        important_project_info = {
                            "id": project['id'],
                            "name": project['name'],
                            "slug": project['slug'],
                            "difficulty": project['difficulty'],
                            "estimate_time": project_sessions[0]['estimate_time'],
                            "is_subscriptable": project_sessions[0]['is_subscriptable'],
                            "link": f"https://projects.intra.42.fr/projects/{project['slug']}",
                        }
                        all_projects_data.append(important_project_info)
                        break

            if len(response) < g_max_results_per_page:
                break

            page += 1
            if g_test_mode:
                g_test_mode_max_pages -= 1

        self.stdout.write(f"Data from [{len(all_projects_data)}] projects")
        return all_projects_data

    def filter_exp(self, projects):
        filtered_projects = [project for project in projects if project['difficulty'] and project['difficulty'] != 0]
        self.stdout.write(f"There are [{len(filtered_projects)}] projects with exp")
        sorted_projects = sorted(filtered_projects, key=lambda project: project['difficulty'])
        return sorted_projects

    def save_to_db(self, projects):
        for project in projects:
            CursusProject.objects.update_or_create(
                project_id=project['id'],
                defaults={
                    'name': project['name'],
                    'slug': project['slug'],
                    'difficulty': project['difficulty'],
                    'estimate_time': project['estimate_time'],
                    'is_subscriptable': project['is_subscriptable'],
                    'project_url': project['link'],
                }
            )
        self.stdout.write(f"Saved [{len(projects)}] projects to the database")
