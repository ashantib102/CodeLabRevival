# CodeLabRevival
“Rebuild. Recode. Revive.”

CodeLab Revival is a next-generation, fully web-based coding education platform designed to modernize programming education through improved usability, intelligent feedback, and data-driven instruction.

This project focuses on rebuilding the user experience from the ground up while improving reliability, scalability, and educational outcomes for both students and instructors.

🚀 Project Vision

CodeLab Revival aims to:

Deliver a fully web-based coding platform for modern programming education.

Provide a user-centric redesign that removes technical barriers and improves learning outcomes.

Offer intelligent feedback tools that help students understand errors instead of memorizing solutions.

Equip instructors with analytics dashboards for actionable insights into student performance.

✨ Core Features
👨‍🎓 Student Experience

Modern UI/UX with responsive dashboards and streamlined navigation (React/Vue-based).

Integrated coding environment with real-time execution.

Intelligent feedback system that categorizes:

Syntax errors

Logic errors

Runtime errors

👩‍🏫 Instructor Tools

Performance dashboards displaying submission analytics and trends.

Data visualization using tools like Chart.js or D3.js.

Exportable reports (PDF/CSV).

⚙️ Infrastructure & Reliability

CI/CD pipelines using GitHub Actions or Jenkins.

Cloud hosting with secure environments.

Real-time monitoring via Sentry.

🧰 Tech Stack & Tools

Planned development tools include:

React.js + Node.js — core platform implementation

VS Code — development environment

Figma — UI/UX mockups

Git/GitHub — version control & collaboration

Languages supported:

Java

Python

C++

🏗️ System Architecture Overview

The system includes three primary components (see diagram on page 7):

1️⃣ Student Workflow

Dashboard → Assignment → Code Editor → Execution Engine

Feedback engine detects and categorizes errors

Progress stored in database

2️⃣ Instructor Analytics

Query database (PostgreSQL/MongoDB)

Aggregate metrics

Generate visualization dashboards

3️⃣ DevOps & Reliability

CI/CD pipeline

Automated testing

Deployment to cloud

Monitoring + alerts

📊 Data Source Strategy

The primary data source comes from internal platform analytics (page 8), including:

Submission frequency

Completion rates

Error distribution

Student interaction data

These insights guide improvements to exercises and platform design.

🔍 Use Cases
✅ Use Case 1 — Intelligent Debug Assistance (Student)

Students receive contextual hints when errors occur. Example:

numbers = [1,2,3]
print(numbers[5])

System detects runtime error → suggests checking list length → student fixes issue.

✅ Use Case 2 — Assignment Completion (Student)

Flow:

Login

Select assignment

Write code

Receive real-time feedback

Submit

Backend validates & stores submission

Example feedback: missing parenthesis detection for:

print("Hello World"

✅ Use Case 3 — Instructor Performance Monitoring

Professors view aggregated insights such as:

40% Syntax Errors

35% Logic Errors

25% Runtime Errors

These insights help guide lecture adjustments.

🗓️ Development Timeline
Phase 1 — Foundation & Design (Weeks 1–4)

UX research

Figma mockups

Tech stack finalized

Phase 2 — Core Development

IDE + authentication system

Phase 3 — Intelligent Features

Secure execution engine

Smart feedback system

Phase 4 — Analytics & Instructor Tools

Analytics dashboard

Exercise library integration

Phase 5 — Launch

CI/CD integration

Monitoring setup

Production deployment

👥 Contributors

Patrick Haye — Student

Ashanti Benons — Student

Daphne Gray — Student

David Arnow — Professor
