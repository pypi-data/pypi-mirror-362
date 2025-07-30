
MODULE_PAGE_PERMISSIONS = [
    'create',
    'view',
    'edit',
    'delete',
]

MODULE_PAGE_PERMISSIONS_EXT = [
    'print',
    'import',
    'export',
    'upload', 
    'download',
    'activate',
    'deactivate',
]

MODULE_NODE_CHOICES = (
    ("dashboard", "Dashboard"),
    ("modules", "Modules"),
    ("account", "Account"),
    ("system", "System"),
)

SKIN_COLOUR_CHOICES = (
    ("behance", "Behance"),
    ("blue", "Blue"),
    ("css3", "CSS3"),
    ("dribbble", "Dribbble"),
    ("dropbox", "DropBox"),
    ("facebook", "Facebook"),
    ("flickr", "FlickR"),
    ("foursquare", "FourSquare"),
    ("github", "GitHub"),
    ("google-plus", "Google+"),
    ("green", "Green"),
    ("html5", "HTML5"),
    ("indigo", "Indigo"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("nkunyim", "Nkunyim"),
    ("openid", "OpenID"),
    ("orange", "Orange"),
    ("pink", "Pink"),
    ("pinterest", "Pinterest"),
    ("purple", "Purple"),
    ("red", "Red"),
    ("reddit", "Reddit"),
    ("spotify", "Spotify"),
    ("stack-overflow", "StackOverflow"),
    ("teal", "Teal"),
    ("tumblr", "Tumblr"),
    ("twitter", "Twitter"),
    ("vimeo", "Vimeo"),
    ("vine", "Vine"),
    ("vk", "Vk"),
    ("xing", "Xing"),
    ("yahoo", "Yahoo"),
    ("yellow", "Yellow"),
)

APPLICATION_MODE_CHOICES = (
    ("web", "Web"),
    ("mob", "Mobile"),
    ("api", "Service"),
    ("cli", "Console"),
)

PROJECT_LICENSE_CHOICES = (
    ("personal", "Personal"),
    ("family", "Family"),
    ("business", "Business"),
    ("public", "Public"),
)

ENTITY_TYPE_CHOICES = (
    ("personal", "Personal"),
    ("business", "Business"),
)

RESPONSE_TYPE_CHOICES = (
    ('code', 'Code'),
    ('token', 'Token'),
)

OTP_TYPE_CHOICES = (
    ('sms', 'SMS'),
    ('email', 'Email'),
    ('push', 'Push'),
    ('totp', 'TOTP'),
)

PERSON_TITLE_CHOICES = (
    ("Mr", "Mr."),
    ("Ms", "Ms."),
    ("Mrs", "Mrs."),
    ("Miss", "Miss."),
    ("Dr", "Dr."),
    ("Rev", "Rev."),
    ("Na", "NA"),
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("N", "NA"),
)

MARITAL_CHOICES = (
    ("S", "Single"),
    ("M", "Married"),
    ("D", "Divorced"),
    ("W", "Widow(er)"),
    ("O", "Other"),
    ("N", "NA"),
)

ADDRESS_NAME_CHOICES = [
    ('email', 'Email Address'),
    ('phone', 'Phone Number'),
    ('digital', 'Digital Address'),
    ('postal', 'Postal Address'),
    ('website', 'Website URL'),
    ('social', 'Social Media ID'),
    ('geoloc', 'Geo Location'),
    ('other', 'Other Contact'),
]

IDENTITY_NAME_CHOICES = [
    ('national', 'National ID'),
    ('passport', 'Passport'),
    ('driving', 'Driving License'),
    ('student', 'Student ID'),
    ('other', 'Other Identity'),
]
