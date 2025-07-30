# xolmurodov/__init__.py

class DiyorbekResume:
    def __init__(self):
        self.name = "Xolmurodov Diyorbek"
        self.title = "Backend Developer"
        self.contact = {
            "Email": "diyorbek0143@gmail.com",
            "Phone": "+998990502611",
            "Location": "Navoiy, Uzbekistan",
            "Telegram": "@diyor_developer",
            "GitHub": "@diyorbekw"
        }
        self.profile = (
            "I am a Backend Developer with strong expertise in Python frameworks such as Django, FastAPI, "
            "and Django REST Framework. Currently working at SIFATDEV, I have built over 25 Telegram bots and "
            "more than 10 APIs for web platforms. I studied Backend Development at Sifat IT Academy, where I focused "
            "on modern Python technologies. I am proficient in tools like Git and AioGram, and continuously work to "
            "improve my backend development skills."
        )
        self.education = {
            "Course": "Backend Development",
            "Academy": "Sifat IT Academy",
            "Duration": "12/2023 – 09/2024",
            "Location": "Navoiy, Uzbekistan"
        }
        self.experience = {
            "Role": "Backend Developer",
            "Company": "SIFATDEV",
            "Duration": "2024 – present",
            "Description": "Developed over 25 Telegram bots and more than 10 APIs for websites."
        }
        self.skills = [
            "Python", "Django", "FastAPI", "Aiogram", "Django REST Framework", "Git"
        ]
        self.projects = [
            {
                "Name": "Coffeeroom API",
                "Tech": "Django REST Framework",
                "Description": "A RESTful API for the online coffee shop Coffeeroom.",
                "Date": "12/2024 – 01/2025"
            },
            {
                "Name": "Get Chat ID Bot",
                "Tech": "Telegram bot",
                "Description": "Telegram bot for retrieving IDs of users, channels, groups, and bots.",
                "Date": "01/2025"
            },
            {
                "Name": "Barbershop API",
                "Tech": "FastAPI",
                "Description": "A RESTful API for an online barber booking platform.",
                "Date": "05/2025"
            }
        ]
        self.languages = {
            "Uzbek": 5,
            "Russian": 4,
            "English": 2
        }
        self.interests = [
            "Reading books", "Playing sports", "Writing clean code",
            "Learning new languages", "Listening to music"
        ]

    def about(self):
        contact_info = '\n'.join([f"{key}: {value}" for key, value in self.contact.items()])
        skills = ', '.join(self.skills)
        languages = '\n'.join([f"{lang}: {'●' * level + '○' * (5 - level)}" for lang, level in self.languages.items()])
        projects = '\n'.join([f"- {p['Name']} ({p['Tech']}, {p['Date']}): {p['Description']}" for p in self.projects])
        interests = ' | '.join(self.interests)

        return f"""
=============================
{self.name.upper()}
{self.title}
=============================

📞 CONTACT
{contact_info}

📌 PROFILE
{self.profile}

🎓 EDUCATION
{self.education['Course']} – {self.education['Academy']}
{self.education['Duration']}, {self.education['Location']}

💼 EXPERIENCE
{self.experience['Role']} at {self.experience['Company']}
{self.experience['Duration']}
{self.experience['Description']}

🛠️ SKILLS
{skills}

📁 PROJECTS
{projects}

🗣️ LANGUAGES
{languages}

🎯 INTERESTS
{interests}
"""

resume = DiyorbekResume()