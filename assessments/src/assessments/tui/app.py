from faker.decode import unidecode
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, TabbedContent, TabPane, Static, DataTable
from textual.containers import Horizontal, Vertical, ScrollableContainer
import polars as pl
import re
import json

REPLACE_ID_REGEX=r"[\\ \[\]\?:]+"

class AssessmentsReviewerApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "focus_students", "Focus Students"),
        ("a", "focus_answers", "Focus Answers"),
        ("t", "focus_terraform", "Focus Terraform"),
        ("n", "focus_notes", "Focus Notes"),
    ]
    CSS = """
    Screen {
        layout: horizontal;
    }

    #left-panel {
        width: 25%;
        height: 100%;
        border-right: solid $accent;
        background: $panel;
    }

    #main-panel {
        width: 75%;
        height: 100%;
    }

    .answer-block {
        border: solid $primary;
        margin: 1;
        padding: 1;
        height: auto;
    }
    
    .question-title {
        text-style: bold;
        background: $primary;
        color: $text;
        width: 100%;
        padding: 0 1;
    }

    .field-label {
        text-style: italic;
        color: $text-muted;
    }

    #terraform-container {
        layout: horizontal;
    }

    #terraform-code-container {
        width: 50%;
        height: 100%;
        border: solid $secondary;
    }

    #terraform-code {
        width: auto;
    }

    #terraform-criteria-container {
        width: 50%;
        height: 100%;
    }
    """

    def __init__(self, df: pl.DataFrame, answers_data: dict):
        super().__init__()
        self.df = df.with_columns(pl.col("username").str.replace_all(REPLACE_ID_REGEX, "_").map_elements(lambda x: unidecode(x.lower())).alias("username"))
        self.answers_data = answers_data

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            with Vertical(id="left-panel"):
                yield Label("Students", id="students-label")
                yield ListView(*[ListItem(Label(user, markup=False), id=user) for user in self.df["username"].sort().to_list()], id="user-list")
            
            with TabbedContent(id="main-panel"):
                with TabPane("Answers", id="answers-tab"):
                    answers_container = ScrollableContainer(id="answers-container")
                    answers_container.can_focus = True
                    yield answers_container
                with TabPane("Terraform", id="terraform-tab"):
                    with Horizontal(id="terraform-container"):
                        with ScrollableContainer(id="terraform-code-container"):
                            yield Static(id="terraform-code", expand=True, markup=False)
                        terraform_criteria_container = ScrollableContainer(id="terraform-criteria-container")
                        terraform_criteria_container.can_focus = True
                        yield terraform_criteria_container
                with TabPane("Notes", id="notes-tab"):
                    notes_container = ScrollableContainer(id="notes-container")
                    notes_container.can_focus = True
                    yield notes_container
        yield Footer()

    def on_mount(self) -> None:
        user_list = self.query_one("#user-list", ListView)
        if user_list.children:
            user_list.index = 0
            # Manually trigger display for the first user
            usernames = self.df["username"].sort().to_list()
            if usernames:
                self.display_user_data(usernames[0])

    def on_list_view_selected(self, event: ListView.Selected):
        if event.item and event.item.id:
            self.display_user_data(str(event.item.id))

    def action_focus_students(self) -> None:
        self.query_one("#user-list").focus()

    def action_focus_answers(self) -> None:
        self.query_one("#main-panel", TabbedContent).active = "answers-tab"
        self.query_one("#answers-container").focus()

    def action_focus_terraform(self) -> None:
        self.query_one("#main-panel", TabbedContent).active = "terraform-tab"
        self.query_one("#terraform-criteria-container").focus()

    def action_focus_notes(self) -> None:
        self.query_one("#main-panel", TabbedContent).active = "notes-tab"
        self.query_one("#notes-container").focus()

    def display_user_data(self, username: str):
        user_row = self.df.filter(pl.col("username") == username).to_dicts()[0]
        
        # Update Answers Tab
        container = self.query_one("#answers-container", ScrollableContainer)
        container.remove_children()
        
        for i in range(14):
            q_id = str(i + 1)
            q_info = self.answers_data.get(q_id, {})
            question_text = q_info.get("question", f"Question {i+1}")
            
            student_answer = user_row.get(f"answer_{i}", "")
            correction_json = user_row.get(f"answer_correction_{i}")
            
            note = "N/A"
            justification = "N/A"
            comment = "N/A"
            
            if correction_json:
                try:
                    correction = json.loads(correction_json)
                    note = str(correction.get("note", 0.0))
                    justification = correction.get("justification", "")
                    comment = correction.get("commentaire", "")
                except (json.JSONDecodeError, TypeError):
                    pass

            block = Vertical(
                Label(f"Q{i+1}: {question_text}", classes="question-title", markup=False),
                Label("Student's Answer:", classes="field-label"),
                Static(str(student_answer), markup=False),
                Label(f"Note: {note}", classes="field-label"),
                Label("Justification:", classes="field-label"),
                Static(str(justification), markup=False),
                Label("Comment:", classes="field-label"),
                Static(str(comment), markup=False),
                classes="answer-block"
            )
            container.mount(block)

        # Update Terraform Tab
        tf_code = user_row.get("terraform", "")
        self.query_one("#terraform-code", Static).update(str(tf_code))
        
        criteria_container = self.query_one("#terraform-criteria-container", ScrollableContainer)
        criteria_container.remove_children()
        
        terraform_criterias = self.answers_data.get("terraform_criterias", [])
        for criteria in terraform_criterias:
            name = criteria["name"]
            criteria_desc = criteria.get("criteria", "")
            correction_json = user_row.get(name)
            
            note = 0.0
            justification = ""
            comment = ""
            
            if correction_json:
                try:
                    correction = json.loads(correction_json)
                    note = correction.get("note", 0.0)
                    justification = correction.get("justification", "")
                    comment = correction.get("commentaire", "")
                except (json.JSONDecodeError, TypeError):
                    pass
            
            block = Vertical(
                Label(f"Criteria: {name}", classes="question-title", markup=False),
                Label("Description:", classes="field-label"),
                Static(str(criteria_desc), markup=False),
                Label(f"Note: {note}", classes="field-label"),
                Label("Justification:", classes="field-label"),
                Static(str(justification), markup=False),
                Label("Comment:", classes="field-label"),
                Static(str(comment), markup=False),
                classes="answer-block"
            )
            criteria_container.mount(block)

        # Update Notes Tab
        notes_container = self.query_one("#notes-container", ScrollableContainer)
        notes_container.remove_children()

        # Questions notes
        notes_container.mount(Label("Detailed Question Grades", classes="question-title"))
        answers_weighted_sum = 0.0
        total_answers_normal_coeffs = 0.0
        bonus_points = 0.0
        for i in range(14):
            q_id = str(i + 1)
            q_info = self.answers_data.get(q_id, {})
            coeff = q_info.get("coefficient", 1)
            is_bonus = q_info.get("bonus", False)
            
            correction_json = user_row.get(f"answer_correction_{i}")
            note = 0.0
            if correction_json:
                try:
                    correction = json.loads(correction_json)
                    note = float(correction.get("note", 0.0))
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass
            
            if is_bonus:
                bonus_points += (note / 20.0) * coeff
                notes_container.mount(Label(f"Q{i+1} (Bonus): {note} (max bonus: {coeff})", markup=False))
            else:
                total_answers_normal_coeffs += coeff
                answers_weighted_sum += note * coeff
                notes_container.mount(Label(f"Q{i+1}: {note} (coeff: {coeff})", markup=False))

        # Terraform notes
        notes_container.mount(Label("Detailed Terraform Grades", classes="question-title"))
        tf_weighted_sum = 0.0
        total_tf_coeffs = 0.0
        terraform_criterias = self.answers_data.get("terraform_criterias", [])
        for criteria in terraform_criterias:
            name = criteria["name"]
            coeff = criteria.get("coefficient", 1)
            total_tf_coeffs += coeff
            
            correction_json = user_row.get(name)
            note = 0.0
            if correction_json:
                try:
                    correction = json.loads(correction_json)
                    note = float(correction.get("note", 0.0))
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass
            
            tf_weighted_sum += note * coeff
            notes_container.mount(Label(f"{name}: {note} (coeff: {coeff})", markup=False))

        # Totals
        notes_container.mount(Label("Global Grades", classes="question-title"))
        
        q_grade_20 = (answers_weighted_sum / total_answers_normal_coeffs) * 20 if total_answers_normal_coeffs > 0 else 0.0
        q_grade_20 = min(20.0, q_grade_20 + bonus_points)
        tf_grade_20 = (tf_weighted_sum / total_tf_coeffs) * 20 if total_tf_coeffs > 0 else 0.0
        composite_grade = (q_grade_20 + tf_grade_20) / 2
        
        notes_container.mount(Label(f"Global Questions Grade: {q_grade_20:.2f} / 20", classes="field-label"))
        notes_container.mount(Label(f"Global Terraform Grade: {tf_grade_20:.2f} / 20", classes="field-label"))
        notes_container.mount(Label(f"Composite Grade (Average): {composite_grade:.2f} / 20", classes="question-title"))