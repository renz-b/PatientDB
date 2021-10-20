from flask_assets import Bundle

bundles = {
    "index_css": Bundle(
        "scss/style.scss",
        filters="libsass",
        depends="scss/*.scss",
        output="gen/index.%(version)s.css"
    )
}

# rename bundle to base index about to be specific
# change output= depending on the name of the bundle
# i think this should be base_css