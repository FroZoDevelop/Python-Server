from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from contentTypeModule import getContentType
from parseURLModule import parseURL

IP = '0.0.0.0'
PORT = 80
siteFolder = 'site/'

def printConnectInfo( requestType, connectInfo, requestURL = None ):
  print( '[{}] New request'.format( requestType.upper() ) )
  print( '  Address: {}:{}'.format( connectInfo[0], connectInfo[1] ) )
  
  if requestURL != None: print( "  Request URL: '{}'".format( requestURL ) )
  
  print()

def getResponse( event, message ):
  return { 'event' : event, 'message' : message }

class CRequestHandler( BaseHTTPRequestHandler ):
  # GET запрос
  def do_GET( self ):
    self.send_response( 200 )
    
    parsedURL = parseURL( self.path )
    contentType = getContentType( parsedURL[ 'fileExtension' ] )
    self.send_header( 'Content-type', contentType )
    
    self.end_headers()
    
    print( contentType )
    
    fileName = parsedURL[ 'fileName' ]
    
    if parsedURL[ 'fileExtension' ] != '': fileName += parsedURL[ 'fileExtension' ]
    
    if fileName == '': filePath = 'index.html'
    elif fileName == 'favicon.ico': pass
    else: filePath = parsedURL[ 'filePath' ] + fileName
    
    printConnectInfo( 'get', self.client_address, self.path )
    
    if fileName != 'favicon.ico':
      try:
        response = open( siteFolder + filePath, 'rb' ).read()
      except:
        try:
          response = open( siteFolder + 'badPage.html', 'rb' ).read()
        except:
          response = bytes( 'Bad page', 'utf8' )
      
      self.wfile.write( response )
  
  # POST запрос
  def do_POST( self ):
    self.send_response( 200 )
    
    # self.send_header( 'Access-Control-Allow-Origin', self.headers[ 'Origin' ] )
    # self.send_header( 'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE' )
    # self.send_header( 'Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept' )
    
    self.end_headers()
    
    data = self.rfile.read( int( self.headers[ 'Content-Length' ] ) ).decode( 'utf8' )
    
    if data != '': data = json.loads( data )
    if not 'dict' in str( type( data ) ): data = {}
    
    printConnectInfo( 'post', self.client_address )
    self.wfile.write( bytes( json.dumps( response ), 'utf8' ) )
  
  # def do_OPTIONS( self ):
  #   self.send_response( 200 )
    
  #   self.send_header( 'Access-Control-Allow-Origin', self.headers[ 'Origin' ] )
  #   self.send_header( 'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE' )
  #   self.send_header( 'Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept' )
    
  #   self.end_headers()

server = HTTPServer( ( IP, PORT ), CRequestHandler )
print( 'Server started\n  IP: http://{}:{}'.format( IP, PORT ) )
server.serve_forever()