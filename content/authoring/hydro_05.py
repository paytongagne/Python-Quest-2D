def clean_tags(tags):
    return [tag.strip().upper() for tag in tags if tag.strip()]
