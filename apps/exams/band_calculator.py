class BandCalculatorService:
    @staticmethod
    def calculate_ielts_band(raw_score, total_questions=40):
        if total_questions <= 0:
            return "0.0"
        percentage = (raw_score / total_questions) * 100
        if percentage >= 97.5:
            return "9.0"
        elif percentage >= 92.5:
            return "8.5"
        elif percentage >= 87.5:
            return "8.0"
        elif percentage >= 80.0:
            return "7.5"
        elif percentage >= 72.5:
            return "7.0"
        elif percentage >= 65.0:
            return "6.5"
        elif percentage >= 57.5:
            return "6.0"
        elif percentage >= 50.0:
            return "5.5"
        elif percentage >= 40.0:
            return "5.0"
        elif percentage >= 30.0:
            return "4.5"
        elif percentage >= 20.0:
            return "4.0"
        return "3.5"

    @staticmethod
    def calculate_sat_score(raw_score, total_questions=40):
        if total_questions <= 0:
            return "200"
        percentage = min(1.0, max(0.0, raw_score / total_questions))
        sat_score = 200 + int(percentage * 600)
        return str(sat_score)

    @staticmethod
    def calculate_cefr_level(raw_score, total_questions=40):
        if total_questions <= 0:
            return "A1"
        percentage = (raw_score / total_questions) * 100
        if percentage >= 90:
            return "C2"
        elif percentage >= 80:
            return "C1"
        elif percentage >= 65:
            return "B2"
        elif percentage >= 50:
            return "B1"
        elif percentage >= 35:
            return "A2"
        return "A1"

    @classmethod
    def calculate_band(cls, exam_type, raw_score, total_questions=40):
        if 'ielts' in exam_type:
            return cls.calculate_ielts_band(raw_score, total_questions)
        elif 'sat' in exam_type:
            return cls.calculate_sat_score(raw_score, total_questions)
        elif 'cefr' in exam_type:
            return cls.calculate_cefr_level(raw_score, total_questions)
        return str(raw_score)
