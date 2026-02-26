"""
Class Attendance Tracker
Supports marking students as Present (P), Absent (A), or Late (L)
"""

from datetime import date


class AttendanceTracker:
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.students: dict[str, dict] = {}  # {student_id: {name, records}}

    # ──────────────────────────────────────────────
    # Student Management
    # ──────────────────────────────────────────────

    def add_student(self, student_id: str, name: str) -> None:
        """Add a student to the class."""
        if student_id in self.students:
            print(f"⚠️  Student ID '{student_id}' already exists.")
            return
        self.students[student_id] = {"name": name, "records": {}}
        print(f"✅ Added: {name} (ID: {student_id})")

    def remove_student(self, student_id: str) -> None:
        """Remove a student from the class."""
        if student_id not in self.students:
            print(f"⚠️  Student ID '{student_id}' not found.")
            return
        name = self.students.pop(student_id)["name"]
        print(f"🗑️  Removed: {name} (ID: {student_id})")

    # ──────────────────────────────────────────────
    # Attendance Marking
    # ──────────────────────────────────────────────

    def mark_attendance(self, student_id: str, status: str, attendance_date: date = None) -> None:
        """
        Mark attendance for a student.
        status: 'P' (Present), 'A' (Absent), 'L' (Late)
        attendance_date: defaults to today if not provided
        """
        status = status.upper()
        if status not in ("P", "A", "L"):
            print("⚠️  Invalid status. Use 'P' (Present), 'A' (Absent), or 'L' (Late).")
            return
        if student_id not in self.students:
            print(f"⚠️  Student ID '{student_id}' not found.")
            return

        attendance_date = attendance_date or date.today()
        date_str = str(attendance_date)
        self.students[student_id]["records"][date_str] = status

        labels = {"P": "Present ✅", "A": "Absent ❌", "L": "Late ⏰"}
        name = self.students[student_id]["name"]
        print(f"📋 {name} marked {labels[status]} on {date_str}")

    def mark_bulk(self, attendance_dict: dict[str, str], attendance_date: date = None) -> None:
        """
        Mark attendance for multiple students at once.
        attendance_dict: {student_id: status}
        """
        attendance_date = attendance_date or date.today()
        for student_id, status in attendance_dict.items():
            self.mark_attendance(student_id, status, attendance_date)

    # ──────────────────────────────────────────────
    # View Records
    # ──────────────────────────────────────────────

    def view_student_record(self, student_id: str) -> None:
        """Display attendance records for a single student."""
        if student_id not in self.students:
            print(f"⚠️  Student ID '{student_id}' not found.")
            return

        student = self.students[student_id]
        records = student["records"]
        print(f"\n📖 Attendance Record — {student['name']} (ID: {student_id})")
        print("-" * 40)

        if not records:
            print("  No records found.")
        else:
            labels = {"P": "Present ✅", "A": "Absent ❌", "L": "Late ⏰"}
            for d in sorted(records):
                print(f"  {d}  →  {labels[records[d]]}")

        pct = self.get_attendance_percentage(student_id)
        if pct is not None:
            print(f"\n  Attendance: {pct:.1f}%")
        print()

    def view_all_records(self) -> None:
        """Display the full attendance sheet for all students."""
        if not self.students:
            print("No students enrolled.")
            return

        # Collect all unique dates
        all_dates = sorted(
            {d for s in self.students.values() for d in s["records"]}
        )

        print(f"\n📋 Class: {self.class_name}")
        print("=" * (30 + 8 * len(all_dates)))

        # Header
        header = f"{'Name':<20} {'ID':<8}" + "".join(f" {d[5:]:>8}" for d in all_dates)
        print(header)
        print("-" * len(header))

        for sid, data in self.students.items():
            row = f"{data['name']:<20} {sid:<8}"
            for d in all_dates:
                status = data["records"].get(d, "-")
                row += f" {status:>8}"
            print(row)

        print()

    def view_date_record(self, attendance_date: date) -> None:
        """Display attendance for all students on a specific date."""
        date_str = str(attendance_date)
        print(f"\n📅 Attendance on {date_str} — {self.class_name}")
        print("-" * 40)

        labels = {"P": "Present ✅", "A": "Absent ❌", "L": "Late ⏰"}
        for sid, data in self.students.items():
            status = data["records"].get(date_str, "Not marked")
            label = labels.get(status, status)
            print(f"  {data['name']:<20} ({sid})  →  {label}")
        print()

    # ──────────────────────────────────────────────
    # Statistics
    # ──────────────────────────────────────────────

    def get_attendance_percentage(self, student_id: str) -> float | None:
        """
        Calculate attendance percentage for a student.
        Present = 100%, Late = 50%, Absent = 0%
        """
        if student_id not in self.students:
            return None
        records = self.students[student_id]["records"]
        if not records:
            return None

        weights = {"P": 1.0, "L": 0.5, "A": 0.0}
        score = sum(weights[s] for s in records.values())
        return (score / len(records)) * 100

    def summary_report(self) -> None:
        """Print a summary of attendance percentages for all students."""
        if not self.students:
            print("No students enrolled.")
            return

        print(f"\n📊 Attendance Summary — {self.class_name}")
        print("=" * 50)
        print(f"  {'Name':<20} {'ID':<10} {'Attendance':>10}")
        print("-" * 50)

        for sid, data in self.students.items():
            pct = self.get_attendance_percentage(sid)
            pct_str = f"{pct:.1f}%" if pct is not None else "N/A"
            flag = " ⚠️" if pct is not None and pct < 75 else ""
            print(f"  {data['name']:<20} {sid:<10} {pct_str:>10}{flag}")

        print("\n  ⚠️  = Below 75% attendance threshold")
        print()


# ──────────────────────────────────────────────────────
# Demo / Example Usage
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    # Create a class
    tracker = AttendanceTracker("Computer Science 101")

    # Add students
    print("=" * 50)
    print("   Adding Students")
    print("=" * 50)
    tracker.add_student("S001", "Alice Johnson")
    tracker.add_student("S002", "Bob Smith")
    tracker.add_student("S003", "Carol White")
    tracker.add_student("S004", "David Brown")

    # Mark attendance for multiple dates
    print("\n" + "=" * 50)
    print("   Marking Attendance")
    print("=" * 50)

    day1 = date(2024, 3, 1)
    tracker.mark_bulk({"S001": "P", "S002": "P", "S003": "A", "S004": "L"}, day1)

    day2 = date(2024, 3, 4)
    tracker.mark_bulk({"S001": "P", "S002": "L", "S003": "P", "S004": "A"}, day2)

    day3 = date(2024, 3, 6)
    tracker.mark_bulk({"S001": "P", "S002": "A", "S003": "A", "S004": "P"}, day3)

    day4 = date(2024, 3, 8)
    tracker.mark_bulk({"S001": "P", "S002": "P", "S003": "L", "S004": "A"}, day4)

    # View full attendance sheet
    tracker.view_all_records()

    # View a specific student's record
    tracker.view_student_record("S003")

    # View attendance for a specific date
    tracker.view_date_record(day3)

    # Summary report
    tracker.summary_report()
