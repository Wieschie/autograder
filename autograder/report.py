from mailmerge import MailMerge


with MailMerge("/home/wieschie/Documents/senior_design/sample_projects/mailmerge.docx") as doc:
    print(doc.get_merge_fields())
