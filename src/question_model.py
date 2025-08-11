# src/question_model.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Question:
    order: int
    question: str
    instruction: str
    difficulty: str
    options: List[str]
    correct_index: int  # 0-based index of correct option
    explanation: str
    subject: str
    unit: str
    topic: str
    plusmarks: int = 1
    image_tag: Optional[str] = None  # if LLM requests image use this tag to generate it

    def to_output_block(self) -> str:
        """Serialize to the exact 'Question Output Format' block."""
        lines = []
        lines.append(f"@question {self.question}")
        lines.append(f"@instruction {self.instruction}")
        lines.append(f"@difficulty {self.difficulty}")
        lines.append(f"@Order {self.order}")
        lines.append("")  # blank line
        for i, opt in enumerate(self.options):
            prefix = "@@option" if i == self.correct_index else "@option"
            lines.append(f"{prefix} {opt}")
        lines.append("")  # blank
        lines.append("@explanation")
        lines.append(self.explanation)
        lines.append(f"@subject {self.subject}")
        lines.append(f"@unit {self.unit}")
        lines.append(f"@topic {self.topic}")
        lines.append(f"@plusmarks {self.plusmarks}")
        if self.image_tag:
            # This is an extension: not in the original PDF but useful for automation.
            # The final .docx can show the image where appropriate.
            lines.append(f"@image {self.image_tag}")
        return "\n".join(lines)

def parse_output_format(text: str, curriculum_map: dict[int, tuple[str, str, str]] = None):
    """
    Parse the LLM's output into a dict with title, description, and a list of Question objects.
    Optionally takes curriculum_map: {order: (subject, unit, topic)} to enforce correct tagging.
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    title = ""
    description = ""
    questions = []

    i = 0
    # read header lines
    while i < len(lines):
        if lines[i].startswith("@title"):
            title = lines[i][len("@title"):].strip()
            i += 1
        elif lines[i].startswith("@description"):
            description = lines[i][len("@description"):].strip()
            i += 1
        else:
            break

    # question blocks
    while i < len(lines):
        if lines[i].strip() == "":
            i += 1
            continue
        if not lines[i].startswith("@question"):
            i += 1
            continue

        q_text = lines[i][len("@question"):].strip()
        i += 1
        instruction = ""
        difficulty = "moderate"
        order = 0
        options = []
        correct_index = None
        explanation = ""
        subject = ""
        unit = ""
        topic = ""
        plusmarks = 1
        image_tag = None

        while i < len(lines) and not lines[i].startswith("@question"):
            ln = lines[i]
            if ln.startswith("@instruction"):
                instruction = ln[len("@instruction"):].strip()
            elif ln.startswith("@difficulty"):
                difficulty = ln[len("@difficulty"):].strip()
            elif ln.startswith("@Order"):
                order = int(ln[len("@Order"):].strip())
            elif ln.startswith("@option") or ln.startswith("@@option"):
                if ln.startswith("@@option"):
                    opt = ln[len("@@option"):].strip()
                    options.append(opt)
                    correct_index = len(options) - 1
                else:
                    opt = ln[len("@option"):].strip()
                    options.append(opt)
            elif ln.startswith("@explanation"):
                i += 1
                expl_lines = []
                while i < len(lines) and not lines[i].startswith("@subject") and not lines[i].startswith("@image"):
                    expl_lines.append(lines[i])
                    i += 1
                explanation = "\n".join(expl_lines).strip()
                continue
            elif ln.startswith("@subject"):
                subject = ln[len("@subject"):].strip()
            elif ln.startswith("@unit"):
                unit = ln[len("@unit"):].strip()
            elif ln.startswith("@topic"):
                topic = ln[len("@topic"):].strip()
            elif ln.startswith("@plusmarks"):
                plusmarks = int(ln[len("@plusmarks"):].strip())
            elif ln.startswith("@image"):
                image_tag = ln[len("@image"):].strip()
            i += 1

        if correct_index is None:
            correct_index = 0

        # Enforce correct curriculum tags if mapping provided
        if curriculum_map and order in curriculum_map:
            subject, unit, topic = curriculum_map[order]

        q = Question(
            order=order,
            question=q_text,
            instruction=instruction,
            difficulty=difficulty,
            options=options,
            correct_index=correct_index,
            explanation=explanation,
            subject=subject,
            unit=unit,
            topic=topic,
            plusmarks=plusmarks,
            image_tag=image_tag
        )
        questions.append(q)

    return {"title": title, "description": description, "questions": questions}

