from fastapi import APIRouter,File, UploadFile
import shutil
import os
from pathlib import Path
from fastapi.responses import FileResponse

router=APIRouter(
    prefix='/file',
    tags=['file']
)

@router.post('/file')
def get_file(file: bytes= File(...)):
    content=file.decode('utf-8')
    lines=content.split('\r\n')

    return {'lines': lines}

@router.post('/filetext')
def get_file(file: UploadFile = File(...)):
    os.makedirs("files", exist_ok=True)

    # Sanitize filename
    filename = Path(file.filename).name
    file_path = f"files/{filename}"

    # Save the uploaded file
    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    # Read and process the file content
    file.file.seek(0)  # reset pointer after read
    content = file.file.read().decode('utf-8')
    lines = content.split('\r\n')

    return {
        'lines': lines,
        'static_url': f"/files/{filename}"
    }

@router.post('/uploadfile')
def get_uploadfile(upload_file: UploadFile= File(...)):

    path=f"files/{upload_file.filename}"

    with open(path,'w+b') as buffer:
        shutil.copyfileobj(upload_file.file,buffer)

    return {'filename': path,
            'type':upload_file.content_type}

@router.get('/download/{name}',response_class=FileResponse)
def get_file(name: str):
    path=f'files/{name}'
    return path