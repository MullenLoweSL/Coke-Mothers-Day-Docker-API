from .converter import convert_to_mp4

def extract(request):
    # 1 - decode request body to doc and convert to docx with libreoffice, if error return
    # 2 - convert docx to text with docx.api and docx2txt, if error return
    # 3 - parse text and extract Fact Find data, if error return
    # 4 - process and return extracted Fact Find data (WIP)

    # 1 - decode request body to doc and convert to docx with libreoffice, if error return
    error, mp4_filepath = convert_to_mp4(request=request)
    if error is not None:
        return {"message": error}
    else:
        return {"result": mp4_filepath}