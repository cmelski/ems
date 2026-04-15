🧾 Executor Estate Manager

A web application designed to help executors manage the process of settling an estate. It provides a centralized place to track tasks, assets, expenses, and progress, making a complex workflow easier to organize and follow.

🚀 Overview

Managing an estate involves coordinating legal, financial, and administrative tasks—often across many moving parts. This application was built to simplify that process by providing:

Task tracking with status updates

Asset and expense management

Inline editing for quick updates

A clear view of overall progress

The goal is a straightforward, practical tool that reduces friction and keeps everything in one place.

🧾 Receipt Storage & Access (AWS S3)

Receipts uploaded against expenses are stored securely in AWS S3 rather than on the application server. This avoids reliance on local file systems and ensures files remain accessible across environments (including cloud deployments).

Each receipt is uploaded with a unique identifier and linked to its corresponding expense record. The system supports both in-app viewing (via modal preview) and external access through downloadable Excel reports.

For reporting and sharing, receipt links are included in exports:

In-app: receipts are rendered directly from their stored URL
Excel exports: receipts are accessible via hyperlinks
Share scenarios: links can be generated with controlled access (e.g. time-limited URLs)

This approach keeps storage scalable and environment-independent while allowing flexibility between secure access and easy sharing with external stakeholders (e.g. beneficiaries, legal representatives).

🛠️ Tech Stack

Backend

Python with Flask

RESTful API design

PostgreSQL for data storage

Frontend

HTML, CSS, and vanilla JavaScript

Dynamic tables and inline editing

Lightweight, responsive UI

Testing

pytest for backend/API tests

Playwright for UI and end-to-end coverage

✨ Features

Task Management

Create, edit, and delete tasks

Status tracking (e.g., pending, in-progress, done)

Inline updates directly in the table

Financial Tracking

Record assets and expenses

Manage Contacts and Notes

View totals and summaries

Interactive UI

Editable fields (text, dropdowns, dates)

Immediate updates without full page reloads

API-Driven

Clean separation between frontend and backend

Supports future integrations or extensions

Automated Testing

API validation and regression coverage

End-to-end UI testing for critical workflows
)

📁 Project Structure


📌 Future Improvements

User authentication / multi-user support

File/document management

Reporting and export features

Notifications and reminders

🧑‍💻 Author

Built as a full-stack project to combine backend development, frontend interactivity, and test automation in a single application.