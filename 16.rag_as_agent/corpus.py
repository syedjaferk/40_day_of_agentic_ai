"""A tiny academy handbook: 12 short notes. Small enough to read, big enough to show retrieval trade-offs."""

from langchain_core.documents import Document

NOTES = [
    (
        "refunds",
        "Refund policy: a student can cancel within 7 days of enrolment for a full refund. "
        "After 7 days no refund is given. Refund requests go through form RF-204.",
    ),
    (
        "certificates",
        "Certificates are issued to students who complete 80 percent of the sessions "
        "and pass the final assessment with at least 60 percent.",
    ),
    (
        "live-classes",
        "Live classes run Monday to Friday at 7 PM IST on Google Meet. "
        "Recordings are uploaded to YouTube within 24 hours.",
    ),
    (
        "fees",
        "The Agentic AI course costs 4,999 rupees. Students from rural colleges get a 50 percent scholarship.",
    ),
    (
        "laptop",
        "You need a laptop with 8 GB RAM, Python 3.10 or newer and a free Groq API key. A GPU is not required.",
    ),
    (
        "mentoring",
        "Every student is assigned a mentor. Mentors hold doubt-clearing sessions on Saturdays "
        "from 10 AM to 12 PM.",
    ),
    (
        "placement",
        "The placement cell shares job openings every Friday and reviews resumes for enrolled students.",
    ),
    (
        "errors",
        "Error PRT-5012 on the portal means your payment succeeded but enrolment is still pending. "
        "Wait 30 minutes; if it persists, mail support.",
    ),
    (
        "community",
        "The Parottasalna WhatsApp community is open to all. Be respectful and do not post promotions.",
    ),
    (
        "quizzes",
        "Each session ends with a quiz. Quizzes can be retaken unlimited times and the best score counts.",
    ),
    (
        "missed-class",
        "If you miss a live class, watch the recording and submit the session exercise by Sunday midnight.",
    ),
    (
        "internships",
        "Top performers are offered a 3-month remote internship after the capstone project.",
    ),
]

DOCS = [Document(page_content=text, metadata={"source": name}) for name, text in NOTES]
