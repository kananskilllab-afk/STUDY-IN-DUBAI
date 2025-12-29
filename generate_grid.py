
universities = [
    ("ADU", "Abu Dhabi University"),
    ("AMITY", "Amity University Dubai"),
    ("BITS", "BITS Pilani Dubai"),
    ("BIUC", "Britts Imperial University College"),
    ("CUD", "Canadian University Dubai"),
    ("CURTIN", "Curtin University Dubai"),
    ("DMU", "De Montfort University"),
    ("DEMONT", "DeMont Institute of Management"),
    ("EM", "EM Normandie Business School"),
    ("EAU", "Emirates Aviation University"),
    ("HULT", "Hult International Business School"),
    ("JNU", "Jaipur National University"),
    ("MANIPAL", "Manipal University Dubai"),
    ("MDX", "Middlesex University Dubai"),
    ("NEST", "Nest Academy of Management"),
    ("SPJ", "SP Jain School of Global Management"),
    ("SIU", "Symbiosis International University"),
    ("UOB", "University of Bolton"),
    ("UD", "University of Dubai"),
    ("UE", "University of Europe for Applied Sciences"),
    ("STIRLING", "University of Stirling"),
    ("UWL", "University of West London"),
    ("UOW", "University of Wollongong"),
    ("WESTFORD", "Westford University College"),
    ("MURDOCH", "Murdoch University"),
    ("REGENT", "Regent Middle East"),
    ("HERTFORD", "University of Hertfordshire (Success Point)"),
    ("RIT", "Rochester Institute of Technology"),
    ("ICCA", "ICCA Dubai"),
    ("WOOLWICH", "The Woolwich Institute"),
    ("DIDI", "Dubai Institute of Design (DIDI)"),
    ("UKCBC", "UK College of Business & Computing"),
    ("VIBE", "Vibe Education"),
    ("HWU", "Heriot-Watt University"),
    ("BIRMINGHAM", "University of Birmingham"),
    ("FAD", "FAD Institute of Luxury Fashion")
]

print('<div class="universities-logo-grid">')
for i, (abbr, name) in enumerate(universities):
    img_name = f"logo_{i}.png" # Check if jpg exists for logo 0-35? My script output showed mostly pngs but I should be careful.
    # Actually my script output showed: logo_0.png (RGB) ... logo_35.png (RGB). All PNGs.
    
    # Check manual overrides if any? No, assuming 1-1 mapping.
    
    print(f'''    <!-- {i+1}. {name} -->
    <div class="uni-logo-card">
        <!-- <div class="uni-abbr">{abbr}</div> -->
        <img src="images/logos/{img_name}" alt="{name} Logo" class="uni-logo-img">
        <h4>{name}</h4>
    </div>''')
print('</div>')
