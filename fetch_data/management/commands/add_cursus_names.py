from django.core.management.base import BaseCommand
from fetch_data.models import Cursus  # Replace with your actual model import

# Define the cursustypes dictionary
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

class Command(BaseCommand):
    help = 'Adds cursus names to all existing Cursus entries based on cursus_id'

    def handle(self, *args, **options):
        # Fetch all Cursus entries
        cursuses = Cursus.objects.all()
        
        updated_count = 0
        for cursus in cursuses:
            cursus_name = cursus_names.get(cursus.cursus_id, "Unknown Cursus Name")
            if cursus.name != cursus_name:
                cursus.name = cursus_name
                cursus.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} Cursus entries.'))

