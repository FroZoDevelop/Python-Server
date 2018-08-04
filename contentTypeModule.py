def getContentType( fileType ):
  fileTypes = {
    '.js' : 'text/javascript',
    '.css' : 'text/css',
    '.png' : 'image/png',
    '.jpg' : 'image/jpeg',
    '.mp4' : 'video/mp4'
  }
  
  try:
    contentType = fileTypes[ fileType ]
  except:
    contentType = 'text/html'
  
  return contentType