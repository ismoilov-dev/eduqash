import openpyxl
from apps.quizzes.models import QuestionBank, QuizQuestion, QuizQuestionOption


class ExcelQuizImporter:
    @staticmethod
    def import_from_excel(file_obj, question_bank: QuestionBank):
        wb = openpyxl.load_workbook(file_obj)
        sheet = wb.active

        created_count = 0
        # Expect headers: Question, Type, Points, NegativeMarking, Option1, Correct1, Option2, Correct2, Option3, Correct3, Option4, Correct4
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or not row[0]:
                continue

            q_text = str(row[0]).strip()
            q_type = str(row[1]).strip().lower() if row[1] else 'single'
            points = float(row[2]) if len(row) > 2 and row[2] is not None else 1.0
            neg_marking = float(row[3]) if len(row) > 3 and row[3] is not None else 0.0

            if q_type not in ['single', 'multi', 'text']:
                q_type = 'single'

            question = QuizQuestion.objects.create(
                bank=question_bank,
                text=q_text,
                type=q_type,
                points=points,
                negative_marking=neg_marking
            )

            # Process option pairs starting from col index 4 (0-based: 4, 5, 6, 7...)
            col_idx = 4
            while col_idx < len(row):
                opt_text = row[col_idx]
                if not opt_text:
                    col_idx += 2
                    continue
                
                is_correct = False
                if col_idx + 1 < len(row):
                    is_correct_val = row[col_idx + 1]
                    if is_correct_val in [True, 1, '1', 'true', 'True', 'YES', 'yes']:
                        is_correct = True

                QuizQuestionOption.objects.create(
                    question=question,
                    text=str(opt_text).strip(),
                    is_correct=is_correct
                )
                col_idx += 2

            created_count += 1

        return created_count
