from tkinter import *
from quiz_brain import QuizBrain
from data import question_data

THEME_COLOR = "#375362"
sample_txt = "Amazon acquired Twitch in \nAugust 2014 for $970 million \ndollars"
sample_score = 0


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score Label
        self.score_label = Label(text=f"Score: {sample_score}", font=("courier new", 15), background=THEME_COLOR,
                                 foreground='white')
        self.score_label.grid(row=0, column=1)

        # Background
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(150, 125,
                                                     width=280,
                                                     text="",
                                                     font=("Arial", 15, "italic"),
                                                     fill=THEME_COLOR)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)  # add padding here!!

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_button_response)
        self.false_button.grid(row=2, column=1)

        # # right button
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_button_response)
        self.true_button.grid(row=2, column=0)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.configure(bg='white', highlightthickness=0)
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_button_response(self):
        self.give_feedback(self.quiz.check_answer("true"))

    def false_button_response(self):
        self.give_feedback(self.quiz.check_answer("false"))

    def give_feedback(self, is_right):

        if is_right:
            self.canvas.configure(bg='green', highlightthickness=0)
            # self.window.after(1000, self.get_next_question)
        else:
            self.canvas.configure(bg='red', highlightthickness=0)
            # self.window.after(1000, self.get_next_question)
        self.window.after(1000, self.get_next_question)
