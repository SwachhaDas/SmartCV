from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_resume_pdf(user, profile, educations, experiences, skills, projects, social_links):
    """Generate a professional PDF resume and return as BytesIO buffer."""

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#0d6efd'),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#555555'),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#0d6efd'),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
    )

    story = []

    # ============ HEADER ============
    story.append(Paragraph(user.username, title_style))

    contact_parts = []
    if user.email:
        contact_parts.append(user.email)
    if profile.phone:
        contact_parts.append(profile.phone)
    if contact_parts:
        story.append(Paragraph(' | '.join(contact_parts), subtitle_style))

    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#0d6efd')))
    story.append(Spacer(1, 10))

    # ============ BIO ============
    if profile.bio:
        story.append(Paragraph('About Me', section_style))
        story.append(Paragraph(profile.bio, body_style))
        story.append(Spacer(1, 6))

    # ============ EDUCATION ============
    if educations:
        story.append(Paragraph('Education', section_style))
        edu_data = [['Degree', 'Institute', 'Year', 'CGPA']]
        for edu in educations:
            edu_data.append([
                edu.degree,
                edu.institute,
                str(edu.passing_year),
                str(edu.cgpa) if edu.cgpa else '—'
            ])
        edu_table = Table(edu_data, colWidths=[2*inch, 2.5*inch, 1*inch, 1*inch])
        edu_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(edu_table)
        story.append(Spacer(1, 6))

    # ============ EXPERIENCE ============
    if experiences:
        story.append(Paragraph('Work Experience', section_style))
        for exp in experiences:
            end = exp.end_date.strftime('%b %Y') if exp.end_date else 'Present'
            start = exp.start_date.strftime('%b %Y')
            title = f"<b>{exp.designation}</b> — {exp.company}"
            story.append(Paragraph(title, body_style))
            story.append(Paragraph(f"<i>{start} – {end}</i>", body_style))
            if exp.description:
                story.append(Paragraph(exp.description, body_style))
            story.append(Spacer(1, 6))

    # ============ SKILLS ============
    if skills:
        story.append(Paragraph('Skills', section_style))
        skill_text = ', '.join([f"{s.skill_name} ({s.get_level_display()})" for s in skills])
        story.append(Paragraph(skill_text, body_style))
        story.append(Spacer(1, 6))

    # ============ PROJECTS ============
    if projects:
        story.append(Paragraph('Projects', section_style))
        for proj in projects:
            title = f"<b>{proj.project_name}</b>"
            story.append(Paragraph(title, body_style))
            story.append(Paragraph(proj.description, body_style))
            if proj.live_link:
                story.append(Paragraph(f'<link href="{proj.live_link}">{proj.live_link}</link>', body_style))
            story.append(Spacer(1, 6))

    # ============ SOCIAL LINKS ============
    if social_links:
        story.append(Paragraph('Social Links', section_style))
        for link in social_links:
            story.append(Paragraph(f"<b>{link.platform}:</b> {link.url}", body_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer