import csv
from fpdf import FPDF
from collections import defaultdict

# === Read and Analyze Data ===
data = []
department_scores = defaultdict(list)

with open("data.csv", newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row['Name']
        dept = row['Department']
        score = int(row['Score'])
        data.append((name, dept, score))
        department_scores[dept].append(score)

averages = {dept: sum(scores)/len(scores) for dept, scores in department_scores.items()}

# === Generate PDF ===
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Internship Automated Report', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = PDFReport()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.set_font("Arial", 'B', 12)
pdf.cell(60, 10, "Name", 1)
pdf.cell(60, 10, "Department", 1)
pdf.cell(30, 10, "Score", 1)
pdf.ln()

pdf.set_font("Arial", '', 12)
for name, dept, score in data:
    pdf.cell(60, 10, name, 1)
    pdf.cell(60, 10, dept, 1)
    pdf.cell(30, 10, str(score), 1)
    pdf.ln()

pdf.ln(10)
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, 'Department Average Scores:', ln=True)

pdf.set_font("Arial", '', 12)
for dept, avg in averages.items():
    pdf.cell(0, 10, f'{dept}: {avg:.2f}', ln=True)

pdf.output("internship_report.pdf")
print("✅ Report generated: internship_report.pdf")