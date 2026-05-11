"""
In-memory mock data store for CodeLab Revival.
Replace with a real database (PostgreSQL/MongoDB) in production.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Users ─────────────────────────────────────────────────────
# instructor_key  : matches the `instructor` field in SEMESTERS courses
# enrolled_courses: list of course_ids a student is enrolled in
USERS = [
    {
        "id": 1,
        "name": "Patrick Haye",
        "email": "patrick@codelab.edu",
        "hashed_password": pwd_context.hash("password123"),
        "role": "instructor",
        "instructor_key": "Haye",
    },
    {
        "id": 2,
        "name": "David Arnow",
        "email": "arnow@codelab.edu",
        "hashed_password": pwd_context.hash("password123"),
        "role": "instructor",
        "instructor_key": "Arnow",
    },
    {
        "id": 3,
        "name": "Student One",
        "email": "student@codelab.edu",
        "hashed_password": pwd_context.hash("student123"),
        "role": "student",
        "enrolled_courses": ["59094"],
    },
    {
        "id": 4,
        "name": "Test User",
        "email": "testuser@codelab.edu",
        "hashed_password": pwd_context.hash("test123"),
        "role": "student",
        "enrolled_courses": ["59097"],
    },
    {
        "id": 5,
        "name": "Daphne Gray",
        "email": "daphne@codelab.edu",
        "hashed_password": pwd_context.hash("password123"),
        "role": "instructor",
        "instructor_key": "DG",
    },
    {
        "id": 6,
        "name": "Ashanti Benons",
        "email": "ashanti@codelab.edu",
        "hashed_password": pwd_context.hash("password123"),
        "role": "instructor",
        "instructor_key": "Benons",
    }
]

# ── Courses ───────────────────────────────────────────────────
SEMESTERS = [
    {
        "term": "Spring 2026",
        "courses": [
            {
                "course_id": "59094",
                "number": "CS1-Java",
                "title": "Generic JAVA For Development",
                "section": "A",
                "instructor": "Arnow",
                "language": "Java",
                "access_code": "TCAB-32741-HWYW-67",
            },
            {
                "course_id": "59097",
                "number": "CS1-Java",
                "title": "PH-Generic JAVA For Development",
                "section": "PH",
                "instructor": "Haye",
                "language": "Java",
                "access_code": "CODE-32744-KAHZ-67",
            },
            {
                "course_id": "59095",
                "number": "CS1-Java",
                "title": "Generic JAVA For Development",
                "section": "B",
                "instructor": "Arnow",
                "language": "Java",
                "access_code": "TCAB-32742-HWYW-68",
            },
            {
                    "course_id": "59096",
                    "number": "CS1-Java",
                    "title": "AB-Generic JAVA For Development",
                    "section": "AB",
                    "instructor": "Benons",
                    "language": "Java",
                    "access_code": "CODE-32745-KAHZ-68",
            },
            {
                "course_id": "59098",
                "number": "CS1-Java",
                "title": "DG-Generic JAVA For Development",
                "section": "DG",
                "instructor": "DG",
                "language": "Java",
                "access_code": "CODE-32746-KAHZ-68",
            }
        ],
    }
]

# ── Lab Structures (one per course) ─────────────────────────
# Course 59094 is the MAIN / aggregate course — all exercises live here.
# Each other course shows only that instructor's exercises.
LAB_STRUCTURES = {
    "59094": {
        "course_id": "59094",
        "title": "JAVA CODELAB",
        "tree": [
            {
                "id": "new-exercises",
                "label": "NEW EXERCISES",
                "children": [],
                "exercises": [],
            },
            {
                "id": "codelab-warmup",
                "label": "CODELAB WARMUP",
                "children": [],
                "exercises": [
                    {"id": "00006", "label": "Print Your Name", "status": "blank"},
                    {"id": "00007", "label": "Simple Calculator", "status": "blank"},
                ],
            },
            {
                "id": "imperative-programming",
                "label": "IMPERATIVE PROGRAMMING",
                "children": [],
                "exercises": [
                    {"id": "00008", "label": "FizzBuzz", "status": "blank"},
                    {"id": "00009", "label": "Array Sum and Average", "status": "blank"},
                    {"id": "00010", "label": "String Reversal", "status": "blank"},
                ],
            },
            {
                "id": "oop",
                "label": "OBJECT ORIENTED PROGRAMMING",
                "children": [
                    {
                        "id": "classes-and-objects",
                        "label": "Classes and Objects",
                        "children": [],
                        "exercises": [
                            {"id": "00011", "label": "BankAccount Class", "status": "blank"},
                        ],
                    },
                    {
                        "id": "references-objects",
                        "label": "REFERENCES and OBJECTS",
                        "children": [
                            {
                                "id": "reference-variable-declaration",
                                "label": "reference variable declaration",
                                "children": [],
                                "exercises": [
                                    {"id": "20518", "label": "String Reference Variable", "status": "blank"},
                                    {"id": "20516", "label": "reference variable declaration", "status": "blank"},
                                    {"id": "20517", "label": "Reference Variable from Input", "status": "blank"},
                                    {"id": "21055", "label": "Null Reference Check", "status": "blank"},
                                    {"id": "21051", "label": "Reference Aliasing", "status": "blank"},
                                    {"id": "21079", "label": "Reference Reassignment", "status": "blank"},
                                    {"id": "21063", "label": "Reference as Method Parameter", "status": "blank"},
                                    {"id": "21067", "label": "Polymorphic Reference", "status": "blank"},
                                    {"id": "21075", "label": "Array of Reference Variables", "status": "blank"},
                                    {"id": "21071", "label": "Reference Returned from Method", "status": "blank"},
                                    {"id": "21059", "label": "Linked Node Chain", "status": "blank"},
                                ],
                            },
                            {
                                "id": "object-creation-expression",
                                "label": "object creation expression",
                                "children": [],
                                "exercises": [
                                    {"id": "21056", "label": "Exercise 21056", "status": "blank"},
                                    {"id": "21052", "label": "Exercise 21052", "status": "blank"},
                                    {"id": "21080", "label": "Exercise 21080", "status": "blank"},
                                    {"id": "21064", "label": "Exercise 21064", "status": "blank"},
                                    {"id": "21068", "label": "Exercise 21068", "status": "blank"},
                                    {"id": "21072", "label": "Exercise 21072", "status": "blank"},
                                    {"id": "21076", "label": "Exercise 21076", "status": "blank"},
                                    {"id": "21060", "label": "Exercise 21060", "status": "blank"},
                                ],
                            },
                            {
                                "id": "object-creation-reference",
                                "label": "object creation and reference",
                                "children": [],
                                "exercises": [],
                            },
                        ],
                        "exercises": [],
                    }
                ],
                "exercises": [],
            },
            {
                "id": "advanced-topics",
                "label": "ADVANCED TOPICS",
                "children": [],
                "exercises": [
                    {"id": "00012", "label": "Fibonacci Sequence (Recursive)", "status": "blank"},
                    {"id": "00013", "label": "Stack Implementation", "status": "blank"},
                    {"id": "00014", "label": "Generic Pair Class", "status": "blank"},
                ],
            },
            {
                "id": "graphics-gui",
                "label": "GRAPHICS AND GUI",
                "children": [],
                "exercises": [],
            },
            {
                "id": "patrick-haye-exercises",
                "label": "Patrick Haye Exercises",
                "children": [
                    {
                        "id": "uncategorized",
                        "label": "Uncategorized",
                        "children": [],
                        "exercises": [
                            {"id": "00001", "label": "Run-Length Encoding", "status": "blank"},
                            {"id": "00002", "label": "Exercise 00002", "status": "blank"},
                            {"id": "00003", "label": "Exercise 00003", "status": "blank"},
                            {"id": "00004", "label": "Hello World", "status": "blank"},
                            {"id": "00005", "label": "Exercise 00005", "status": "blank"},
                        ],
                    }
                ],
                "exercises": [{"id": "00004", "label": "Hello World", "status": "blank"}],
            },
        ],
    },
    # ── Arnow — Section B (59095) ─────────────────────────────
    "59095": {
        "course_id": "59095",
        "title": "JAVA CODELAB — Section B",
        "tree": [
            {
                "id": "new-exercises",
                "label": "NEW EXERCISES",
                "children": [],
                "exercises": [],
            },
            {
                "id": "imperative-programming",
                "label": "IMPERATIVE PROGRAMMING",
                "children": [],
                "exercises": [
                    {"id": "00008", "label": "FizzBuzz", "status": "blank"},
                    {"id": "00009", "label": "Array Sum and Average", "status": "blank"},
                    {"id": "00010", "label": "String Reversal", "status": "blank"},
                ],
            },
            {
                "id": "oop",
                "label": "OBJECT ORIENTED PROGRAMMING",
                "children": [
                    {
                        "id": "references-objects",
                        "label": "REFERENCES and OBJECTS",
                        "children": [
                            {
                                "id": "reference-variable-declaration",
                                "label": "reference variable declaration",
                                "children": [],
                                "exercises": [
                                    {"id": "20516", "label": "reference variable declaration", "status": "blank"},
                                ],
                            },
                        ],
                        "exercises": [],
                    }
                ],
                "exercises": [],
            },
        ],
    },
    # ── Benons — Section AB (59096) ───────────────────────────
    "59096": {
        "course_id": "59096",
        "title": "JAVA CODELAB — Section AB",
        "tree": [
            {
                "id": "new-exercises",
                "label": "NEW EXERCISES",
                "children": [],
                "exercises": [],
            },
            {
                "id": "oop",
                "label": "OBJECT ORIENTED PROGRAMMING",
                "children": [
                    {
                        "id": "classes-and-objects",
                        "label": "Classes and Objects",
                        "children": [],
                        "exercises": [
                            {"id": "00011", "label": "BankAccount Class", "status": "blank"},
                        ],
                    },
                ],
                "exercises": [],
            },
            {
                "id": "advanced-topics",
                "label": "ADVANCED TOPICS",
                "children": [],
                "exercises": [
                    {"id": "00012", "label": "Fibonacci Sequence (Recursive)", "status": "blank"},
                ],
            },
        ],
    },
    # ── Haye — Section PH (59097) ─────────────────────────────
    "59097": {
        "course_id": "59097",
        "title": "PH-JAVA CODELAB",
        "tree": [
            {
                "id": "new-exercises",
                "label": "NEW EXERCISES",
                "children": [],
                "exercises": [],
            },
            {
                "id": "codelab-warmup",
                "label": "CODELAB WARMUP",
                "children": [],
                "exercises": [
                    {"id": "00006", "label": "Print Your Name", "status": "blank"},
                    {"id": "00007", "label": "Simple Calculator", "status": "blank"},
                ],
            },
            {
                "id": "haye-exercises",
                "label": "Patrick Haye Exercises",
                "children": [
                    {
                        "id": "uncategorized",
                        "label": "Uncategorized",
                        "children": [],
                        "exercises": [
                            {"id": "00001", "label": "Run-Length Encoding", "status": "blank"},
                            {"id": "00004", "label": "Hello World", "status": "blank"},
                        ],
                    }
                ],
                "exercises": [],
            },
        ],
    },
    # ── Daphne Gray — Section DG (59098) ──────────────────────
    "59098": {
        "course_id": "59098",
        "title": "DG-JAVA CODELAB",
        "tree": [
            {
                "id": "new-exercises",
                "label": "NEW EXERCISES",
                "children": [],
                "exercises": [],
            },
            {
                "id": "advanced-topics",
                "label": "ADVANCED TOPICS",
                "children": [],
                "exercises": [
                    {"id": "00013", "label": "Stack Implementation", "status": "blank"},
                    {"id": "00014", "label": "Generic Pair Class", "status": "blank"},
                ],
            },
        ],
    },
}

# ── Exercises ─────────────────────────────────────────────────
EXERCISES = {
    "00001": {
        "id": "00001",
        "title": "Run-Length Encoding",
        "instructions": (
            "Write a <strong>program</strong> that compresses a <strong>string</strong> "
            "using <strong>run-length encoding</strong>.<br><br>"
            "Your class should be named <strong>RunLength</strong>.<br>"
            "Read a single line from standard input and print the encoded result."
        ),
        "sample_runs": [
            {"input": "aaabbcaaaa", "output": "a3b2c1a4"},
            {"input": "xyz", "output": "x1y1z1"},
        ],
        "starter_code": "public class RunLength {\n    public static void main(String[] args) {\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RunLength {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String s = sc.nextLine();\n"
            "        StringBuilder sb = new StringBuilder();\n"
            "        int i = 0;\n"
            "        while (i < s.length()) {\n"
            "            char c = s.charAt(i);\n"
            "            int count = 1;\n"
            "            while (i + count < s.length() && s.charAt(i + count) == c) count++;\n"
            "            sb.append(c).append(count);\n"
            "            i += count;\n"
            "        }\n"
            "        System.out.println(sb.toString());\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "Patrick Haye Exercises",
    },
    "20516": {
        "id": "20516",
        "title": "reference variable declaration",
        "instructions": (
            "Declare a <strong>reference variable</strong> of type <code>File</code> "
            "named <code>myFile</code>.<br><br>"
            "Use the appropriate import statement if needed."
        ),
        "sample_runs": [],
        "starter_code": "import java.io.File;\n\npublic class Declare {\n    public static void main(String[] args) {\n        // declare myFile here\n    }\n}\n",
        "solution_code": (
            "import java.io.File;\n\n"
            "public class Declare {\n"
            "    public static void main(String[] args) {\n"
            "        File myFile;\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "00004": {
        "id": "00004",
        "title": "Hello World",
        "instructions": (
            "Write a Java program that prints <strong>Hello, World!</strong> "
            "to standard output.<br><br>"
            "Your class should be named <strong>HelloWorld</strong>."
        ),
        "sample_runs": [
            {"input": "", "output": "Hello, World!"},
        ],
        "starter_code": "public class HelloWorld {\n    public static void main(String[] args) {\n        // your code here\n    }\n}\n",
        "solution_code": (
            "public class HelloWorld {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Hello, World!\");\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "Patrick Haye Exercises",
    },
    # ── Codelab Warmup ────────────────────────────────────────
    "00006": {
        "id": "00006",
        "title": "Print Your Name",
        "instructions": (
            "<strong>[Beginner]</strong> Write a Java program that asks the user for their "
            "<strong>first name</strong> and <strong>last name</strong> on separate lines, "
            "then prints: <code>Hello, FirstName LastName!</code><br><br>"
            "Your class should be named <strong>PrintName</strong>.<br>"
            "Use a <code>Scanner</code> to read input from standard input."
        ),
        "sample_runs": [
            {"input": "Jane\nDoe", "output": "Hello, Jane Doe!"},
            {"input": "John\nSmith", "output": "Hello, John Smith!"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class PrintName {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class PrintName {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String first = sc.nextLine();\n"
            "        String last = sc.nextLine();\n"
            "        System.out.println(\"Hello, \" + first + \" \" + last + \"!\");\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "CODELAB WARMUP",
    },
    "00007": {
        "id": "00007",
        "title": "Simple Calculator",
        "instructions": (
            "<strong>[Beginner]</strong> Write a Java program that reads two integers and an "
            "operator (<code>+</code>, <code>-</code>, <code>*</code>, or <code>/</code>) "
            "from standard input, then prints the result.<br><br>"
            "Input format: first integer, operator, second integer — each on its own line.<br>"
            "For division, perform <strong>integer division</strong>.<br>"
            "Your class should be named <strong>Calculator</strong>."
        ),
        "sample_runs": [
            {"input": "10\n+\n3", "output": "13"},
            {"input": "10\n/\n3", "output": "3"},
            {"input": "7\n*\n6", "output": "42"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class Calculator {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class Calculator {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int a = sc.nextInt();\n"
            "        String op = sc.next();\n"
            "        int b = sc.nextInt();\n"
            "        int result = switch (op) {\n"
            "            case \"+\" -> a + b;\n"
            "            case \"-\" -> a - b;\n"
            "            case \"*\" -> a * b;\n"
            "            case \"/\" -> a / b;\n"
            "            default  -> 0;\n"
            "        };\n"
            "        System.out.println(result);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "CODELAB WARMUP",
    },
    # ── Missing Beginner Exercises ────────────────────────────
    "00002": {
        "id": "00002",
        "title": "Temperature Converter",
        "instructions": (
            "<strong>[Beginner]</strong> Write a Java program that converts "
            "temperature from Celsius to Fahrenheit.<br><br>"
            "Read a temperature in Celsius from standard input and print the "
            "equivalent temperature in Fahrenheit.<br><br>"
            "Formula: <code>F = (C × 9/5) + 32</code><br><br>"
            "Your class should be named <strong>TempConverter</strong>.<br>"
            "Print the result with 2 decimal places."
        ),
        "sample_runs": [
            {"input": "25", "output": "77.00"},
            {"input": "0", "output": "32.00"},
            {"input": "100", "output": "212.00"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class TempConverter {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class TempConverter {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        double celsius = sc.nextDouble();\n"
            "        double fahrenheit = (celsius * 9.0 / 5.0) + 32.0;\n"
            "        System.out.printf(\"%.2f\\n\", fahrenheit);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "Patrick Haye Exercises",
    },
    "00003": {
        "id": "00003",
        "title": "Even or Odd",
        "instructions": (
            "<strong>[Beginner]</strong> Write a Java program that determines if a number "
            "is even or odd.<br><br>"
            "Read an integer from standard input and print <code>Even</code> if the number "
            "is even, or <code>Odd</code> if the number is odd.<br><br>"
            "Your class should be named <strong>EvenOdd</strong>."
        ),
        "sample_runs": [
            {"input": "4", "output": "Even"},
            {"input": "7", "output": "Odd"},
            {"input": "0", "output": "Even"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class EvenOdd {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class EvenOdd {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int num = sc.nextInt();\n"
            "        if (num % 2 == 0) {\n"
            "            System.out.println(\"Even\");\n"
            "        } else {\n"
            "            System.out.println(\"Odd\");\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "Patrick Haye Exercises",
    },
    "00005": {
        "id": "00005",
        "title": "Simple Interest Calculator",
        "instructions": (
            "<strong>[Beginner]</strong> Write a Java program that calculates simple interest.<br><br>"
            "Read three values from standard input:<br>"
            "<code>principal</code> (double), <code>rate</code> (double as percentage), "
            "<code>time</code> (int in years).<br><br>"
            "Calculate simple interest using: <code>SI = (P × R × T) / 100</code><br><br>"
            "Your class should be named <strong>SimpleInterest</strong>.<br>"
            "Print the result with 2 decimal places."
        ),
        "sample_runs": [
            {"input": "1000\n5\n2", "output": "100.00"},
            {"input": "5000\n7.5\n3", "output": "1125.00"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class SimpleInterest {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class SimpleInterest {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        double principal = sc.nextDouble();\n"
            "        double rate = sc.nextDouble();\n"
            "        int time = sc.nextInt();\n"
            "        double interest = (principal * rate * time) / 100.0;\n"
            "        System.out.printf(\"%.2f\\n\", interest);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "Patrick Haye Exercises",
    },
    # ── Imperative Programming ────────────────────────────────
    "00008": {
        "id": "00008",
        "title": "FizzBuzz",
        "instructions": (
            "<strong>[Beginner–Intermediate]</strong> Write a Java program that reads a positive integer "
            "<code>N</code> from standard input and prints every integer from <code>1</code> to "
            "<code>N</code> (inclusive), one per line, with the following substitutions:<br><br>"
            "<ul>"
            "<li>If the number is divisible by <strong>3</strong>, print <code>Fizz</code></li>"
            "<li>If the number is divisible by <strong>5</strong>, print <code>Buzz</code></li>"
            "<li>If divisible by <strong>both</strong>, print <code>FizzBuzz</code></li>"
            "<li>Otherwise, print the number</li>"
            "</ul>"
            "Your class should be named <strong>FizzBuzz</strong>."
        ),
        "sample_runs": [
            {"input": "15", "output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class FizzBuzz {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class FizzBuzz {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        for (int i = 1; i <= n; i++) {\n"
            "            if (i % 15 == 0)     System.out.println(\"FizzBuzz\");\n"
            "            else if (i % 3 == 0) System.out.println(\"Fizz\");\n"
            "            else if (i % 5 == 0) System.out.println(\"Buzz\");\n"
            "            else                 System.out.println(i);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "IMPERATIVE PROGRAMMING",
    },
    "00009": {
        "id": "00009",
        "title": "Array Sum and Average",
        "instructions": (
            "<strong>[Intermediate]</strong> Write a Java program that reads an integer "
            "<code>N</code>, then reads <code>N</code> integers, and prints their "
            "<strong>sum</strong> and <strong>average</strong> (as a <code>double</code>) "
            "on separate lines.<br><br>"
            "Format the average to <strong>2 decimal places</strong>.<br>"
            "Your class should be named <strong>ArrayStats</strong>."
        ),
        "sample_runs": [
            {"input": "4\n10\n20\n30\n40", "output": "Sum: 100\nAverage: 25.00"},
            {"input": "3\n1\n2\n3", "output": "Sum: 6\nAverage: 2.00"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class ArrayStats {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class ArrayStats {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        int[] nums = new int[n];\n"
            "        int sum = 0;\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            nums[i] = sc.nextInt();\n"
            "            sum += nums[i];\n"
            "        }\n"
            "        System.out.println(\"Sum: \" + sum);\n"
            "        System.out.printf(\"Average: %.2f%n\", (double) sum / n);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "IMPERATIVE PROGRAMMING",
    },
    "00010": {
        "id": "00010",
        "title": "String Reversal",
        "instructions": (
            "<strong>[Intermediate]</strong> Write a Java program that reads a line of text "
            "from standard input and prints the <strong>reversed</strong> string.<br><br>"
            "Do <strong>not</strong> use <code>StringBuilder.reverse()</code> — implement "
            "the reversal manually using a loop.<br>"
            "Your class should be named <strong>ReverseString</strong>."
        ),
        "sample_runs": [
            {"input": "hello", "output": "olleh"},
            {"input": "Java", "output": "avaJ"},
            {"input": "racecar", "output": "racecar"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class ReverseString {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String line = sc.nextLine();\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class ReverseString {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String line = sc.nextLine();\n"
            "        String reversed = \"\";\n"
            "        for (int i = line.length() - 1; i >= 0; i--) {\n"
            "            reversed += line.charAt(i);\n"
            "        }\n"
            "        System.out.println(reversed);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "IMPERATIVE PROGRAMMING",
    },
    # ── OOP ───────────────────────────────────────────────────
    "00011": {
        "id": "00011",
        "title": "BankAccount Class",
        "instructions": (
            "<strong>[Intermediate–OOP]</strong> Create a class named <strong>BankAccount</strong> "
            "with the following:<br><br>"
            "<strong>Fields:</strong><br>"
            "<ul><li><code>private double balance</code></li></ul>"
            "<strong>Methods:</strong><br>"
            "<ul>"
            "<li><code>BankAccount(double initialBalance)</code> — constructor</li>"
            "<li><code>void deposit(double amount)</code> — adds amount to balance</li>"
            "<li><code>boolean withdraw(double amount)</code> — subtracts amount if sufficient funds, returns <code>true</code> on success, <code>false</code> otherwise</li>"
            "<li><code>double getBalance()</code> — returns the current balance</li>"
            "</ul>"
            "In <code>main</code>, read three commands from standard input: "
            "<code>deposit &lt;amount&gt;</code>, <code>withdraw &lt;amount&gt;</code>, "
            "or <code>balance</code>. Print the result of each command."
        ),
        "sample_runs": [
            {"input": "deposit 500\nwithdraw 200\nbalance", "output": "Deposited: 500.0\nWithdrew: 200.0\nBalance: 300.0"},
            {"input": "deposit 100\nwithdraw 500\nbalance", "output": "Deposited: 100.0\nInsufficient funds\nBalance: 100.0"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class BankAccount {\n    private double balance;\n\n    public BankAccount(double initialBalance) {\n        // your code here\n    }\n\n    public void deposit(double amount) {\n        // your code here\n    }\n\n    public boolean withdraw(double amount) {\n        // your code here\n        return false;\n    }\n\n    public double getBalance() {\n        // your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        BankAccount account = new BankAccount(0);\n        Scanner sc = new Scanner(System.in);\n        // read and process 3 commands\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class BankAccount {\n"
            "    private double balance;\n\n"
            "    public BankAccount(double initialBalance) {\n"
            "        this.balance = initialBalance;\n"
            "    }\n\n"
            "    public void deposit(double amount) {\n"
            "        balance += amount;\n"
            "    }\n\n"
            "    public boolean withdraw(double amount) {\n"
            "        if (amount > balance) return false;\n"
            "        balance -= amount;\n"
            "        return true;\n"
            "    }\n\n"
            "    public double getBalance() {\n"
            "        return balance;\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        BankAccount account = new BankAccount(0);\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        for (int i = 0; i < 3; i++) {\n"
            "            String cmd = sc.next();\n"
            "            if (cmd.equals(\"deposit\")) {\n"
            "                double amt = sc.nextDouble();\n"
            "                account.deposit(amt);\n"
            "                System.out.println(\"Deposited: \" + amt);\n"
            "            } else if (cmd.equals(\"withdraw\")) {\n"
            "                double amt = sc.nextDouble();\n"
            "                if (account.withdraw(amt)) System.out.println(\"Withdrew: \" + amt);\n"
            "                else System.out.println(\"Insufficient funds\");\n"
            "            } else {\n"
            "                System.out.println(\"Balance: \" + account.getBalance());\n"
            "            }\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "OBJECT ORIENTED PROGRAMMING",
    },
    # ── Advanced Topics ───────────────────────────────────────
    "00012": {
        "id": "00012",
        "title": "Fibonacci Sequence (Recursive)",
        "instructions": (
            "<strong>[Advanced]</strong> Write a Java program that reads a non-negative integer "
            "<code>N</code> from standard input and prints the <code>N</code>th Fibonacci number.<br><br>"
            "<strong>Requirements:</strong><br>"
            "<ul>"
            "<li>Implement a <strong>recursive</strong> method <code>fib(int n)</code></li>"
            "<li><code>fib(0) = 0</code>, <code>fib(1) = 1</code></li>"
            "<li>Then, implement a second version using <strong>memoization</strong> "
            "(store results in an array to avoid redundant computation)</li>"
            "<li>Print both results on separate lines prefixed with <code>Recursive:</code> "
            "and <code>Memoized:</code></li>"
            "</ul>"
            "Your class should be named <strong>Fibonacci</strong>."
        ),
        "sample_runs": [
            {"input": "10", "output": "Recursive: 55\nMemoized: 55"},
            {"input": "0", "output": "Recursive: 0\nMemoized: 0"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class Fibonacci {\n\n    public static long fib(int n) {\n        // recursive — your code here\n        return 0;\n    }\n\n    public static long fibMemo(int n, long[] memo) {\n        // memoized — your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        long[] memo = new long[n + 1];\n        System.out.println(\"Recursive: \" + fib(n));\n        System.out.println(\"Memoized: \" + fibMemo(n, memo));\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class Fibonacci {\n\n"
            "    public static long fib(int n) {\n"
            "        if (n <= 1) return n;\n"
            "        return fib(n - 1) + fib(n - 2);\n"
            "    }\n\n"
            "    public static long fibMemo(int n, long[] memo) {\n"
            "        if (n <= 1) return n;\n"
            "        if (memo[n] != 0) return memo[n];\n"
            "        memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);\n"
            "        return memo[n];\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        long[] memo = new long[n + 1];\n"
            "        System.out.println(\"Recursive: \" + fib(n));\n"
            "        System.out.println(\"Memoized: \" + fibMemo(n, memo));\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "ADVANCED TOPICS",
    },
    "00013": {
        "id": "00013",
        "title": "Stack Implementation",
        "instructions": (
            "<strong>[Advanced]</strong> Implement a generic <strong>stack</strong> using an array "
            "(without using <code>java.util.Stack</code> or <code>Deque</code>).<br><br>"
            "Create a class named <strong>MyStack</strong> with a fixed capacity of 100 that supports:<br>"
            "<ul>"
            "<li><code>void push(int val)</code> — push value onto the stack; print "
            "<code>Stack overflow</code> if full</li>"
            "<li><code>int pop()</code> — remove and return top value; print "
            "<code>Stack underflow</code> and return <code>-1</code> if empty</li>"
            "<li><code>int peek()</code> — return top value without removing; print "
            "<code>Stack is empty</code> and return <code>-1</code> if empty</li>"
            "<li><code>boolean isEmpty()</code></li>"
            "</ul>"
            "In <code>main</code>, read commands until end of input: "
            "<code>push &lt;val&gt;</code>, <code>pop</code>, or <code>peek</code>. "
            "For <code>pop</code> and <code>peek</code>, print the returned value (if not an error)."
        ),
        "sample_runs": [
            {"input": "push 5\npush 10\npeek\npop\npop\npop", "output": "10\n10\n5\nStack underflow"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class MyStack {\n    private int[] data = new int[100];\n    private int top = -1;\n\n    public void push(int val) {\n        // your code here\n    }\n\n    public int pop() {\n        // your code here\n        return -1;\n    }\n\n    public int peek() {\n        // your code here\n        return -1;\n    }\n\n    public boolean isEmpty() {\n        return top == -1;\n    }\n\n    public static void main(String[] args) {\n        MyStack stack = new MyStack();\n        Scanner sc = new Scanner(System.in);\n        // read and process commands\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class MyStack {\n"
            "    private int[] data = new int[100];\n"
            "    private int top = -1;\n\n"
            "    public void push(int val) {\n"
            "        if (top == data.length - 1) { System.out.println(\"Stack overflow\"); return; }\n"
            "        data[++top] = val;\n"
            "    }\n\n"
            "    public int pop() {\n"
            "        if (isEmpty()) { System.out.println(\"Stack underflow\"); return -1; }\n"
            "        return data[top--];\n"
            "    }\n\n"
            "    public int peek() {\n"
            "        if (isEmpty()) { System.out.println(\"Stack is empty\"); return -1; }\n"
            "        return data[top];\n"
            "    }\n\n"
            "    public boolean isEmpty() { return top == -1; }\n\n"
            "    public static void main(String[] args) {\n"
            "        MyStack stack = new MyStack();\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        while (sc.hasNextLine()) {\n"
            "            String line = sc.nextLine().trim();\n"
            "            if (line.startsWith(\"push\")) {\n"
            "                stack.push(Integer.parseInt(line.split(\" \")[1]));\n"
            "            } else if (line.equals(\"pop\")) {\n"
            "                int v = stack.pop();\n"
            "                if (v != -1) System.out.println(v);\n"
            "            } else if (line.equals(\"peek\")) {\n"
            "                int v = stack.peek();\n"
            "                if (v != -1) System.out.println(v);\n"
            "            }\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "ADVANCED TOPICS",
    },
    "00014": {
        "id": "00014",
        "title": "Generic Pair Class",
        "instructions": (
            "<strong>[Advanced — Generics]</strong> Create a generic class named "
            "<strong>Pair&lt;A, B&gt;</strong> that holds two values of potentially "
            "different types.<br><br>"
            "<strong>Requirements:</strong><br>"
            "<ul>"
            "<li>Constructor: <code>Pair(A first, B second)</code></li>"
            "<li>Getters: <code>getFirst()</code> and <code>getSecond()</code></li>"
            "<li>Override <code>toString()</code> to return "
            "<code>(first, second)</code></li>"
            "<li>Add a static method <code>swap(Pair&lt;A,B&gt; p)</code> that returns a new "
            "<code>Pair&lt;B,A&gt;</code> with the values swapped</li>"
            "</ul>"
            "In <code>main</code>, create a <code>Pair&lt;String, Integer&gt;</code> from two "
            "lines of input (a word and a number), print it, then print the swapped pair."
        ),
        "sample_runs": [
            {"input": "hello\n42", "output": "(hello, 42)\n(42, hello)"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class Pair<A, B> {\n\n    // fields here\n\n    public Pair(A first, B second) {\n        // your code here\n    }\n\n    public A getFirst() { return null; }\n    public B getSecond() { return null; }\n\n    @Override\n    public String toString() {\n        // your code here\n        return \"\";\n    }\n\n    public static <A, B> Pair<B, A> swap(Pair<A, B> p) {\n        // your code here\n        return null;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class Pair<A, B> {\n"
            "    private A first;\n"
            "    private B second;\n\n"
            "    public Pair(A first, B second) {\n"
            "        this.first = first;\n"
            "        this.second = second;\n"
            "    }\n\n"
            "    public A getFirst() { return first; }\n"
            "    public B getSecond() { return second; }\n\n"
            "    @Override\n"
            "    public String toString() {\n"
            "        return \"(\" + first + \", \" + second + \")\";\n"
            "    }\n\n"
            "    public static <A, B> Pair<B, A> swap(Pair<A, B> p) {\n"
            "        return new Pair<>(p.getSecond(), p.getFirst());\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String word = sc.nextLine();\n"
            "        int num = Integer.parseInt(sc.nextLine());\n"
            "        Pair<String, Integer> p = new Pair<>(word, num);\n"
            "        System.out.println(p);\n"
            "        System.out.println(swap(p));\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "ADVANCED TOPICS",
    },
    # ── Additional Intermediate Exercises ──────────────────────
    "20517": {
        "id": "20517",
        "title": "Reference Variable from Input",
        "instructions": (
            "Read a word from standard input. Declare a <code>String</code> "
            "reference variable named <code>word</code> and assign the input to it.<br><br>"
            "Print the <strong>length</strong> of <code>word</code> on the first line, "
            "then print <code>word</code> itself on the second line.<br><br>"
            "Your class should be named <strong>RefInput</strong>."
        ),
        "sample_runs": [
            {"input": "hello", "output": "5\nhello"},
            {"input": "Java", "output": "4\nJava"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class RefInput {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        // declare String reference variable 'word' and assign input to it\n\n"
            "        // print its length, then the word itself\n\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RefInput {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String word = sc.nextLine();\n"
            "        System.out.println(word.length());\n"
            "        System.out.println(word);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "20518": {
        "id": "20518",
        "title": "String Reference Variable",
        "instructions": (
            "Declare a <strong>reference variable</strong> of type <code>String</code> "
            "named <code>text</code> and assign it the string literal <code>\"Java\"</code>.<br><br>"
            "Print <code>text</code>.<br><br>"
            "Your class should be named <strong>StringRef</strong>."
        ),
        "sample_runs": [
            {"input": "", "output": "Java"},
        ],
        "starter_code": (
            "public class StringRef {\n"
            "    public static void main(String[] args) {\n"
            "        // declare a String reference variable named 'text' and assign \"Java\" to it\n\n"
            "        System.out.println(text);\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "public class StringRef {\n"
            "    public static void main(String[] args) {\n"
            "        String text = \"Java\";\n"
            "        System.out.println(text);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21051": {
        "id": "21051",
        "title": "Reference Aliasing",
        "instructions": (
            "Create a <code>StringBuilder</code> object and assign it to a reference variable "
            "named <code>a</code>. Declare a second reference variable <code>b</code> and assign "
            "<code>a</code> to it — both now point to the <strong>same</strong> object.<br><br>"
            "Append <code>\"Hello\"</code> using <code>a</code> and <code>\" World\"</code> using "
            "<code>b</code>. Print the result using <code>a.toString()</code>.<br><br>"
            "Your class should be named <strong>RefAlias</strong>."
        ),
        "sample_runs": [
            {"input": "", "output": "Hello World"},
        ],
        "starter_code": (
            "public class RefAlias {\n"
            "    public static void main(String[] args) {\n"
            "        StringBuilder a = new StringBuilder();\n"
            "        // declare 'b' and point it to the same object as 'a'\n\n"
            "        a.append(\"Hello\");\n"
            "        // append \" World\" using b\n\n"
            "        System.out.println(a.toString());\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "public class RefAlias {\n"
            "    public static void main(String[] args) {\n"
            "        StringBuilder a = new StringBuilder();\n"
            "        StringBuilder b = a;\n"
            "        a.append(\"Hello\");\n"
            "        b.append(\" World\");\n"
            "        System.out.println(a.toString());\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    # ── Advanced Exercises ─────────────────────────────────────
    "21055": {
        "id": "21055",
        "title": "Null Reference Check",
        "instructions": (
            "Read a line from standard input. Declare a <code>String</code> reference variable "
            "named <code>ref</code>.<br><br>"
            "If the input equals <code>\"null\"</code>, assign <code>null</code> to <code>ref</code>; "
            "otherwise assign the input string to <code>ref</code>.<br><br>"
            "If <code>ref</code> is <code>null</code>, print <code>\"empty\"</code>. "
            "Otherwise print <code>ref + \" has length \" + ref.length()</code>.<br><br>"
            "Your class should be named <strong>NullCheck</strong>."
        ),
        "sample_runs": [
            {"input": "hello", "output": "hello has length 5"},
            {"input": "null", "output": "empty"},
            {"input": "Java", "output": "Java has length 4"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class NullCheck {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String input = sc.nextLine();\n"
            "        String ref;\n"
            "        // assign null to ref if input equals \"null\", else assign input\n\n"
            "        // print \"empty\" if ref is null, else print ref + \" has length \" + ref.length()\n\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class NullCheck {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String input = sc.nextLine();\n"
            "        String ref;\n"
            "        if (input.equals(\"null\")) {\n"
            "            ref = null;\n"
            "        } else {\n"
            "            ref = input;\n"
            "        }\n"
            "        if (ref == null) {\n"
            "            System.out.println(\"empty\");\n"
            "        } else {\n"
            "            System.out.println(ref + \" has length \" + ref.length());\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21059": {
        "id": "21059",
        "title": "Linked Node Chain",
        "instructions": (
            "Create a static inner class <code>Node</code> with an <code>int value</code> field "
            "and a <code>Node next</code> reference variable (initially <code>null</code>).<br><br>"
            "In <code>main</code>, read an integer <code>n</code>, then read <code>n</code> integers. "
            "Build a linked chain: each node's <code>next</code> reference points to the next node "
            "in sequence. Use a <code>head</code> and a <code>tail</code> reference variable to "
            "build the chain efficiently.<br><br>"
            "Traverse from <code>head</code> using a <code>current</code> reference variable and "
            "print each node's value on its own line.<br><br>"
            "Your class should be named <strong>NodeChain</strong>."
        ),
        "sample_runs": [
            {"input": "3\n10\n20\n30", "output": "10\n20\n30"},
            {"input": "4\n5\n1\n7\n3", "output": "5\n1\n7\n3"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class NodeChain {\n"
            "    static class Node {\n"
            "        int value;\n"
            "        Node next;\n"
            "        Node(int value) { this.value = value; this.next = null; }\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        // build a chain of n nodes\n"
            "        // hint: use a 'head' reference and a 'tail' reference\n\n"
            "        // traverse from head and print each node's value\n\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class NodeChain {\n"
            "    static class Node {\n"
            "        int value;\n"
            "        Node next;\n"
            "        Node(int value) { this.value = value; this.next = null; }\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        Node head = null;\n"
            "        Node tail = null;\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            Node newNode = new Node(sc.nextInt());\n"
            "            if (head == null) {\n"
            "                head = newNode;\n"
            "                tail = newNode;\n"
            "            } else {\n"
            "                tail.next = newNode;\n"
            "                tail = newNode;\n"
            "            }\n"
            "        }\n"
            "        Node current = head;\n"
            "        while (current != null) {\n"
            "            System.out.println(current.value);\n"
            "            current = current.next;\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21056": {
        "id": "21056",
        "title": "ArrayList Sorting",
        "instructions": (
            "<strong>[Intermediate — Collections]</strong> Read an integer <code>n</code>, "
            "then read <code>n</code> integers and store them in an <code>ArrayList&lt;Integer&gt;</code>.<br><br>"
            "Sort the list in ascending order and print all elements separated by spaces.<br><br>"
            "Your class should be named <strong>SortList</strong>."
        ),
        "sample_runs": [
            {"input": "5\n3\n1\n4\n1\n5", "output": "1 1 3 4 5"},
            {"input": "3\n9\n2\n7", "output": "2 7 9"},
        ],
        "starter_code": "import java.util.ArrayList;\nimport java.util.Collections;\nimport java.util.Scanner;\n\npublic class SortList {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        ArrayList<Integer> list = new ArrayList<>();\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.ArrayList;\nimport java.util.Collections;\nimport java.util.Scanner;\n\n"
            "public class SortList {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        ArrayList<Integer> list = new ArrayList<>();\n"
            "        int n = sc.nextInt();\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            list.add(sc.nextInt());\n"
            "        }\n"
            "        Collections.sort(list);\n"
            "        for (int i = 0; i < list.size(); i++) {\n"
            "            if (i > 0) System.out.print(\" \");\n"
            "            System.out.print(list.get(i));\n"
            "        }\n"
            "        System.out.println();\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "REFERENCES and OBJECTS",
    },
    "21052": {
        "id": "21052",
        "title": "HashMap Word Count",
        "instructions": (
            "<strong>[Intermediate — Collections]</strong> Read lines of text until an empty line.<br><br>"
            "Count the frequency of each word (case-insensitive) using a <code>HashMap&lt;String, Integer&gt;</code>.<br><br>"
            "Print each unique word and its count, one per line, in the order they first appear.<br><br>"
            "Your class should be named <strong>WordCounter</strong>."
        ),
        "sample_runs": [
            {"input": "hello world\nhello\nworld world\n", "output": "hello 2\nworld 3"},
            {"input": "Java is fun\njava is great\n", "output": "java 2\nis 2\nfun 1\ngreat 1"},
        ],
        "starter_code": "import java.util.HashMap;\nimport java.util.Scanner;\n\npublic class WordCounter {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        HashMap<String, Integer> wordCount = new HashMap<>();\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.HashMap;\nimport java.util.LinkedHashMap;\nimport java.util.Scanner;\n\n"
            "public class WordCounter {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        LinkedHashMap<String, Integer> wordCount = new LinkedHashMap<>();\n"
            "        while (sc.hasNextLine()) {\n"
            "            String line = sc.nextLine().trim();\n"
            "            if (line.isEmpty()) break;\n"
            "            String[] words = line.split(\"\\\\s+\");\n"
            "            for (String word : words) {\n"
            "                String lowerWord = word.toLowerCase();\n"
            "                wordCount.put(lowerWord, wordCount.getOrDefault(lowerWord, 0) + 1);\n"
            "            }\n"
            "        }\n"
            "        for (String word : wordCount.keySet()) {\n"
            "            System.out.println(word + \" \" + wordCount.get(word));\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "REFERENCES and OBJECTS",
    },
    "21063": {
        "id": "21063",
        "title": "Reference as Method Parameter",
        "instructions": (
            "Write a static method <code>fill(String[] arr, String value)</code> that assigns "
            "<code>value</code> to every element of <code>arr</code>.<br><br>"
            "In <code>main</code>, read an integer <code>n</code> and a string <code>value</code>. "
            "Create a <code>String[]</code> of size <code>n</code>, call <code>fill</code>, "
            "then print each element on its own line.<br><br>"
            "Passing the array reference to the method lets the method modify the original array.<br><br>"
            "Your class should be named <strong>RefParam</strong>."
        ),
        "sample_runs": [
            {"input": "3\nhello", "output": "hello\nhello\nhello"},
            {"input": "2\nJava", "output": "Java\nJava"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class RefParam {\n"
            "    static void fill(String[] arr, String value) {\n"
            "        // assign value to every element of arr\n\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = Integer.parseInt(sc.nextLine());\n"
            "        String value = sc.nextLine();\n"
            "        String[] arr = new String[n];\n"
            "        fill(arr, value);\n"
            "        for (String s : arr) {\n"
            "            System.out.println(s);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RefParam {\n"
            "    static void fill(String[] arr, String value) {\n"
            "        for (int i = 0; i < arr.length; i++) {\n"
            "            arr[i] = value;\n"
            "        }\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = Integer.parseInt(sc.nextLine());\n"
            "        String value = sc.nextLine();\n"
            "        String[] arr = new String[n];\n"
            "        fill(arr, value);\n"
            "        for (String s : arr) {\n"
            "            System.out.println(s);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21064": {
        "id": "21064",
        "title": "Binary Search Implementation",
        "instructions": (
            "<strong>[Advanced — Algorithms]</strong> Implement binary search on a sorted array.<br><br>"
            "Read an integer <code>n</code>, then read <code>n</code> sorted integers, then read a target value.<br><br>"
            "Implement a <code>binarySearch</code> method that returns the index of the target or -1 if not found.<br><br>"
            "Print the result.<br><br>"
            "Your class should be named <strong>BinarySearch</strong>."
        ),
        "sample_runs": [
            {"input": "5\n1\n3\n5\n7\n9\n5", "output": "2"},
            {"input": "4\n2\n4\n6\n8\n3", "output": "-1"},
        ],
        "starter_code": "import java.util.Scanner;\n\npublic class BinarySearch {\n    public static int binarySearch(int[] arr, int target) {\n        // your code here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class BinarySearch {\n"
            "    public static int binarySearch(int[] arr, int target) {\n"
            "        int left = 0;\n"
            "        int right = arr.length - 1;\n"
            "        while (left <= right) {\n"
            "            int mid = left + (right - left) / 2;\n"
            "            if (arr[mid] == target) {\n"
            "                return mid;\n"
            "            } else if (arr[mid] < target) {\n"
            "                left = mid + 1;\n"
            "            } else {\n"
            "                right = mid - 1;\n"
            "            }\n"
            "        }\n"
            "        return -1;\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        int[] arr = new int[n];\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            arr[i] = sc.nextInt();\n"
            "        }\n"
            "        int target = sc.nextInt();\n"
            "        System.out.println(binarySearch(arr, target));\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "REFERENCES and OBJECTS",
    },
    "21067": {
        "id": "21067",
        "title": "Polymorphic Reference",
        "instructions": (
            "A reference variable can hold any object of a compatible subtype.<br><br>"
            "Create a class <code>Shape</code> with a method <code>String describe()</code> "
            "returning <code>\"I am a Shape\"</code>.<br><br>"
            "Create a subclass <code>Circle</code> that overrides <code>describe()</code> "
            "to return <code>\"I am a Circle\"</code>.<br><br>"
            "In <code>main</code>, declare a <code>Shape</code> reference variable <code>s</code>. "
            "Read a string: if it equals <code>\"circle\"</code>, assign <code>new Circle()</code> "
            "to <code>s</code>; otherwise assign <code>new Shape()</code>. Print <code>s.describe()</code>.<br><br>"
            "Your main class should be named <strong>PolyRef</strong>."
        ),
        "sample_runs": [
            {"input": "circle", "output": "I am a Circle"},
            {"input": "shape", "output": "I am a Shape"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "class Shape {\n"
            "    public String describe() {\n"
            "        return \"I am a Shape\";\n"
            "    }\n"
            "}\n\n"
            "class Circle extends Shape {\n"
            "    // override describe() to return \"I am a Circle\"\n"
            "}\n\n"
            "public class PolyRef {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String input = sc.nextLine();\n"
            "        Shape s;\n"
            "        // assign new Circle() if input is \"circle\", else new Shape()\n\n"
            "        System.out.println(s.describe());\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "class Shape {\n"
            "    public String describe() {\n"
            "        return \"I am a Shape\";\n"
            "    }\n"
            "}\n\n"
            "class Circle extends Shape {\n"
            "    @Override\n"
            "    public String describe() {\n"
            "        return \"I am a Circle\";\n"
            "    }\n"
            "}\n\n"
            "public class PolyRef {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String input = sc.nextLine();\n"
            "        Shape s;\n"
            "        if (input.equals(\"circle\")) {\n"
            "            s = new Circle();\n"
            "        } else {\n"
            "            s = new Shape();\n"
            "        }\n"
            "        System.out.println(s.describe());\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21071": {
        "id": "21071",
        "title": "Reference Returned from Method",
        "instructions": (
            "Write a static method <code>String repeat(String s, int times)</code> that returns "
            "<code>s</code> concatenated <code>times</code> times.<br><br>"
            "In <code>main</code>, read a word and an integer <code>times</code>. "
            "Declare a <code>String</code> reference variable <code>result</code> and assign it "
            "the return value of <code>repeat(word, times)</code>. Print <code>result</code>.<br><br>"
            "Your class should be named <strong>RefReturn</strong>."
        ),
        "sample_runs": [
            {"input": "ab\n3", "output": "ababab"},
            {"input": "ha\n4", "output": "hahahaha"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class RefReturn {\n"
            "    static String repeat(String s, int times) {\n"
            "        // return s repeated 'times' times\n"
            "        return \"\";\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String s = sc.nextLine();\n"
            "        int times = Integer.parseInt(sc.nextLine());\n"
            "        // declare a String reference 'result' and assign it repeat(s, times)\n\n"
            "        System.out.println(result);\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RefReturn {\n"
            "    static String repeat(String s, int times) {\n"
            "        StringBuilder sb = new StringBuilder();\n"
            "        for (int i = 0; i < times; i++) {\n"
            "            sb.append(s);\n"
            "        }\n"
            "        return sb.toString();\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String s = sc.nextLine();\n"
            "        int times = Integer.parseInt(sc.nextLine());\n"
            "        String result = repeat(s, times);\n"
            "        System.out.println(result);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21075": {
        "id": "21075",
        "title": "Array of Reference Variables",
        "instructions": (
            "Declare a <code>String[]</code> array named <code>words</code> — an array of "
            "reference variables.<br><br>"
            "Read an integer <code>n</code>, then read <code>n</code> words into the array. "
            "Reverse the order of the words <strong>in-place</strong> by swapping reference "
            "variables (do not use any built-in reverse method). Print each word on its own line.<br><br>"
            "Your class should be named <strong>RefArray</strong>."
        ),
        "sample_runs": [
            {"input": "3\napple\nbanana\ncherry", "output": "cherry\nbanana\napple"},
            {"input": "2\nhello\nworld", "output": "world\nhello"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class RefArray {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = Integer.parseInt(sc.nextLine());\n"
            "        String[] words = new String[n];\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            words[i] = sc.nextLine();\n"
            "        }\n"
            "        // reverse the array in-place by swapping references\n\n"
            "        for (String w : words) {\n"
            "            System.out.println(w);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RefArray {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = Integer.parseInt(sc.nextLine());\n"
            "        String[] words = new String[n];\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            words[i] = sc.nextLine();\n"
            "        }\n"
            "        for (int i = 0, j = n - 1; i < j; i++, j--) {\n"
            "            String temp = words[i];\n"
            "            words[i] = words[j];\n"
            "            words[j] = temp;\n"
            "        }\n"
            "        for (String w : words) {\n"
            "            System.out.println(w);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21079": {
        "id": "21079",
        "title": "Reference Reassignment",
        "instructions": (
            "Declare a <code>String</code> reference variable <code>s</code> and assign "
            "<code>\"initial\"</code> to it. Print <code>s</code>.<br><br>"
            "Read a word from standard input. Reassign <code>s</code> to point to the new word. "
            "Print <code>s</code> again.<br><br>"
            "Your class should be named <strong>RefReassign</strong>."
        ),
        "sample_runs": [
            {"input": "updated", "output": "initial\nupdated"},
            {"input": "changed", "output": "initial\nchanged"},
        ],
        "starter_code": (
            "import java.util.Scanner;\n\n"
            "public class RefReassign {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String s = \"initial\";\n"
            "        System.out.println(s);\n"
            "        String newValue = sc.nextLine();\n"
            "        // reassign s to newValue\n\n"
            "        System.out.println(s);\n"
            "    }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.Scanner;\n\n"
            "public class RefReassign {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String s = \"initial\";\n"
            "        System.out.println(s);\n"
            "        String newValue = sc.nextLine();\n"
            "        s = newValue;\n"
            "        System.out.println(s);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "reference variable declaration",
    },
    "21080": {
        "id": "21080",
        "title": "Lambda Expressions",
        "instructions": (
            "<strong>[Advanced — Functional Programming]</strong> Use lambda expressions to:<br><br>"
            "Read 5 integers into a list, then:<br>"
            "<ul><li>Print even numbers</li><li>Print numbers greater than 10</li><li>Calculate sum</li></ul>"
            "Use streams and lambda expressions.<br><br>"
            "Your class should be named <strong>LambdaDemo</strong>."
        ),
        "sample_runs": [
            {"input": "5\n12\n7\n15\n3\n20", "output": "Even: 12 20\nGreater than 10: 12 15 20\nSum: 57"},
        ],
        "starter_code": "import java.util.ArrayList;\nimport java.util.List;\nimport java.util.Scanner;\n\npublic class LambdaDemo {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        List<Integer> numbers = new ArrayList<>();\n        // your code here\n    }\n}\n",
        "solution_code": (
            "import java.util.ArrayList;\nimport java.util.List;\nimport java.util.Scanner;\n\n"
            "public class LambdaDemo {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        List<Integer> numbers = new ArrayList<>();\n"
            "        int n = sc.nextInt();\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            numbers.add(sc.nextInt());\n"
            "        }\n"
            "        \n"
            "        System.out.print(\"Even: \");\n"
            "        numbers.stream().filter(x -> x % 2 == 0).forEach(x -> System.out.print(x + \" \"));\n"
            "        System.out.println();\n"
            "        \n"
            "        System.out.print(\"Greater than 10: \");\n"
            "        numbers.stream().filter(x -> x > 10).forEach(x -> System.out.print(x + \" \"));\n"
            "        System.out.println();\n"
            "        \n"
            "        int sum = numbers.stream().mapToInt(Integer::intValue).sum();\n"
            "        System.out.println(\"Sum: \" + sum);\n"
            "    }\n"
            "}\n"
        ),
        "course_id": "59094",
        "topic": "REFERENCES and OBJECTS",
    },
}

# ── Submissions (in-memory store) ─────────────────────────────
SUBMISSIONS: list[dict] = []
_submission_counter = 0


def next_submission_id() -> int:
    global _submission_counter
    _submission_counter += 1
    return _submission_counter


# ── Exercise ID counter ───────────────────────────────────────
_exercise_counter = 14  # last used ID is 00014


def next_exercise_id() -> str:
    global _exercise_counter
    _exercise_counter += 1
    return str(_exercise_counter).zfill(5)


def add_exercise_to_course(course_id: str, exercise_id: str, label: str) -> None:
    """Append a new exercise ref to the NEW EXERCISES node of a course tree."""
    lab = LAB_STRUCTURES.get(course_id)
    if not lab:
        return
    for node in lab["tree"]:
        if node["id"] == "new-exercises":
            node["exercises"].append({"id": exercise_id, "label": label, "status": "blank"})
            return
    # Fallback: prepend a new-exercises node
    lab["tree"].insert(0, {
        "id": "new-exercises",
        "label": "NEW EXERCISES",
        "children": [],
        "exercises": [{"id": exercise_id, "label": label, "status": "blank"}],
    })


def get_user_by_email(email: str) -> dict | None:
    for u in USERS:
        if u["email"].lower() == email.lower():
            return u
    return None


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
