from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

file_path = "data/resumes/sample.pdf"

with open(file_path, "rb") as f:
    file_bytes = f.read()

text = load_resume(file_bytes, "sample.pdf")

print("\n========== RESUME TEXT ==========\n")
print(text)

profile = parse_resume(text)

print("\n========== EXTRACTED PROFILE ==========\n")
print(profile.model_dump_json(indent=2))
