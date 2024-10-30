def clean_subject_data(data):
    subject_name = ' '.join(data.get('subject_name').upper().split())
    experience_code = int(data.get('experience_code'))
    dedication_code = int(data.get('dedication_code'))
    return subject_name, experience_code, dedication_code