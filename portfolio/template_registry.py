PORTFOLIO_TEMPLATES = [
    {"slug": "classic",  "name": "Classic",  "tagline": "Clean and timeless", "desc": "Single-column layout. Best for traditional job applications and maximum ATS compatibility.", "html": "portfolio/portfolio_classic.html", "image": "bi-file-earmark-text", "pdf_style": "classic"},
    {"slug": "modern",   "name": "Modern",   "tagline": "Gradient and bold",  "desc": "Features a beautiful blue sidebar for skills and contact info. Perfect for tech and creative roles.", "html": "portfolio/portfolio_modern.html",  "image": "bi-window-stack",  "pdf_style": "modern"},
    {"slug": "dark",     "name": "Neon Dark", "tagline": "Developer favorite", "desc": "Dark background with neon blue accents. Looks stunning on screens and is loved by developers.", "html": "portfolio/portfolio_dark.html",    "image": "bi-moon-stars-fill",    "pdf_style": "dark"},
    {"slug": "timeline", "name": "Timeline", "tagline": "Story of your career", "desc": "Displays your experience in a beautiful vertical timeline. Great for showing career growth.", "html": "portfolio/portfolio_timeline.html", "image": "bi-clock-history", "pdf_style": "modern"},
    {"slug": "minimal",  "name": "Minimal",  "tagline": "Less is more",       "desc": "Lots of white space and crisp typography. Lets your content speak for itself.", "html": "portfolio/portfolio_minimal.html", "image": "bi-justify",  "pdf_style": "classic"},
    {"slug": "colorful", "name": "Colorful", "tagline": "Vibrant and creative","desc": "A vibrant gradient background with card-based layout. Great for designers and artists.", "html": "portfolio/portfolio_colorful.html", "image": "bi-palette", "pdf_style": "modern"},
    {"slug": "card",     "name": "Card Layout", "tagline": "Modular design",  "desc": "Organizes your skills and experience into distinct cards. Highly readable and clean.", "html": "portfolio/portfolio_card.html",    "image": "bi-grid-3x3",     "pdf_style": "modern"},
    {"slug": "sidebar",  "name": "Sidebar",  "tagline": "Classic split",      "desc": "Dark left sidebar with a bright right column. Professional and space-efficient.", "html": "portfolio/portfolio_sidebar.html", "image": "bi-layout-sidebar",  "pdf_style": "modern"},
    {"slug": "academic", "name": "Academic", "tagline": "For researchers",    "desc": "Formal, text-heavy layout designed for academic CVs, research papers, and faculty applications.", "html": "portfolio/portfolio_academic.html", "image": "bi-book", "pdf_style": "classic"},
    {"slug": "elegant",  "name": "Elegant",  "tagline": "Serif and premium",  "desc": "A classic serif font layout that feels premium and sophisticated. Great for senior roles.", "html": "portfolio/portfolio_elegant.html", "image": "bi-type-italic",  "pdf_style": "classic"},
]

DEFAULT_SLUG = "classic"
_BY_SLUG = {t["slug"]: t for t in PORTFOLIO_TEMPLATES}

def get_template(slug):
    return _BY_SLUG.get(slug) or _BY_SLUG[DEFAULT_SLUG]

def is_valid_slug(slug):
    return slug in _BY_SLUG

def django_choices():
    return [(t["slug"], t["name"]) for t in PORTFOLIO_TEMPLATES]