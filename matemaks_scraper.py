from selenium import webdriver
from config import *


class MatemaksScraper:
    def __init__(self, login=LOGIN, password=PASSWORD):
        self.login = login
        self.password = password

        # Open browser
        self.browser = webdriver.Chrome()

        # Login to matemaks.pl
        self.__login_to_matemaks()

    def __login_to_matemaks(self):
        self.browser.get("https://www.matemaks.pl/login.php")

        input_username = self.browser.find_element_by_id("nazwa_uz")
        input_username.send_keys(self.login)

        input_password = self.browser.find_element_by_id("haslo")
        input_password.send_keys(self.password)

        login_button = self.browser.find_element_by_id("login_button")
        login_button.click()

    def get_questions(self, url, only_video_ids=False):
        # Verify url
        if "zadania" not in url:
            print("Pod tym linkiem nie ma żadnych zadań")
            return False

        questions = {}

        # Go to url with questions
        self.browser.get(url)

        all_lesson_questions = self.browser.find_elements_by_css_selector(
            ".zadanie:not(.lekcja)"
        )

        for curr_question in all_lesson_questions:
            if only_video_ids:
                questions[curr_question.get_attribute(
                    "id"
                )] = curr_question.get_attribute("yt")
                continue

            # Set answer
            if curr_question.get_attribute("odp"):
                answer = curr_question.find_element_by_css_selector(
                    ".p_o"
                ).get_attribute("innerHTML").replace('<span class="u">Odpowiedź:</span> ', "")
            else:
                answer = False

            # Add question details to questions dict
            questions[curr_question.get_attribute("id")] = {
                "yt": curr_question.get_attribute("yt"),
                "ans": answer,
                "pts": curr_question.get_attribute("pkt"),
                "date": curr_question.get_attribute("data"),
            }

        print("Pobrano pytania z", url)

        return questions

    def get_lessons_data(self, url, **kwargs):
        lessons = {}

        # Go to url with lessons
        self.browser.get(url)

        number_of_lessons = len(
            self.browser.find_elements_by_class_name("lekcja")
        )

        # Get lesson level
        lvl = 1 if "podstawowa" in self.browser.find_element_by_class_name(
            "tytuldzialu"
        ).text else 2

        # Store lesson details
        for i in range(number_of_lessons):
            lesson = self.browser.find_elements_by_class_name("lekcja")[i]
            print(
                f"Pobieranie danych dla lekcji: {lesson.get_attribute('tytul')}"
            )

            lesson_url = lesson.find_element_by_tag_name(
                'a').get_attribute("href")

            lesson_details = {
                "lvl": lvl,
                "yt": lesson.get_attribute("yt"),
                "lesson_url": lesson_url if not "youtube" in lesson_url else ""
            }

            lessons[i + 1] = lesson_details

        # Get and save questions dict for each lesson
        for lesson_number in lessons:
            lesson = lessons[lesson_number]

            if 'only_video_ids' in kwargs:
                lessons[lesson_number] = lesson["yt"]
                continue

            print(
                f"Pobieranie pytań do lekcji nr: {lesson_number}, poziom: {lesson['lvl']}"
            )
            questions = self.get_questions(lesson["lesson_url"])

            if 'only_video_ids':
                if questions:
                    for question in questions:
                        questions[question] = questions[question]['yt']

                lessons[lesson_number] = questions
            elif 'only_questions' in kwargs:
                lessons[lesson_number] = questions
            else:
                lessons[lesson_number]["questions"] = questions

        return lessons

    def get_basic_matura_course(self, **kwargs):
        return self.get_lessons_data(BASIC_MATURA_COURSE_URL, **kwargs)

    def get_extended_matura_course(self, **kwargs):
        return self.get_lessons_data(EXTENDED_MATURA_COURSE_URL, **kwargs)

    def get_all_matura_course(self, **kwargs):
        return {
            "basic_matura": self.get_basic_matura_course(**kwargs),
            "extended_matura": self.get_extended_matura_course(**kwargs)
        }

    def get_all_matura_questions(self, only_video_ids=False):
        questions = {}

        for url in QUESTIONS_COLLECTIONS_URLS:
            print("Rozpoczęto pobieranie pytań z kolekcji:", url)
            questions.update(self.get_questions(url, only_video_ids))

        questions_from_lessons = self.get_all_matura_course(
            only_questions=True
        )

        for level in questions_from_lessons:
            for lesson_number in questions_from_lessons[level]:
                lesson_questions = questions_from_lessons[level][lesson_number]

                if lesson_questions:
                    questions.update(lesson_questions)

        return questions

    def generate_data_for_matemaks_extension(self):
        from export_functions import export_to_json

        # Get needed data
        extension_data = {
            "lessons_info": self.get_all_matura_course(only_video_ids=True),
            "questions": self.get_all_matura_questions(only_video_ids=True)
        }

        # Close browser
        self.close_browser

        # Write to file
        export_to_json(
            extension_data, "output/data_for_matemaks_extension.json"
        )

        print("Możesz teraz wgrać wygenerowany plik do 'Matemaks extension'")

    def close_browser(self):
        self.browser.close()

    def __del__(self):
        self.close_browser()
